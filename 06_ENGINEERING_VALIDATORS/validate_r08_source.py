#!/usr/bin/env python3
"""Strict R08 static SPICE library/instance contract checker, no numerical solver.

Parses the specified real R08 SPICE syntax only. No synthetic circuit netlists,
node values or generated measurement results. Rejects unknown element types.
This is a source-structure check, not ngspice, ERC, or a physical bench proof.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path

R08_DEFAULT=Path(__file__).resolve().parents[1]/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
class NetlistError(ValueError): pass

def parse(deck:Path)->dict:
    all_files={}
    def read_recursive(path:Path,active:tuple[str,...]=()):
        path=path.resolve()
        if path.name in active:raise NetlistError('cyclic INCLUDE '+str(path))
        if not path.exists():raise NetlistError('missing INCLUDE '+str(path))
        if path in all_files:return
        rec=[]
        for number,raw in enumerate(path.read_text().splitlines(),1):
            line=raw.strip()
            if not line or line.startswith('*') or line.startswith(';'):continue
            if line[0]=='+':raise NetlistError(f'{path}:{number}: continuation not supported; do not silently ignore')
            parts=line.split()
            if parts[0].upper()=='.INCLUDE':
                if len(parts)!=2:raise NetlistError(f'{path}:{number}: malformed INCLUDE {line}')
                name=parts[1].strip("\"'")
                target=(path.parent/name).resolve()
                if target.parent!=path.parent:raise NetlistError('INCLUDE outside source directory '+name)
                read_recursive(target,(*active,path.name))
            else:rec.append({'line':number,'text':line,'tokens':parts})
        all_files[path]=rec
    read_recursive(deck)
    scopes={};scope_now='__TOP__';scopes[scope_now]={'pins':[],'lines':[],'models':set(),'names':set()}
    # Library first, top circuit last; disallow duplicate subcircuit definition
    for path,records in sorted(all_files.items(),key=lambda kv: kv[0]==deck.resolve()):
        is_first=True
        for entry in records:
            parts=entry['tokens'];cmd=parts[0].upper();n=entry['line'];loc=f'{path.name}:{n}'
            # Only first line in SPICE file is title (unless begins with '.')
            if is_first and not cmd.startswith('.'):
                is_first=False;continue
            is_first=False
            if cmd=='.SUBCKT':
                if scope_now!='__TOP__':raise NetlistError(f'{loc}: nested SUBCKT')
                if len(parts)<3:raise NetlistError(f'{loc}: SUBCKT requires ports')
                name=parts[1].upper()
                if name in scopes:raise NetlistError(f'{loc}: duplicate SUBCKT {name}')
                scope_now=name;scopes[name]={'pins':parts[2:],'lines':[],'models':set(),'names':set()};continue
            if cmd=='.ENDS':
                if scope_now=='__TOP__':raise NetlistError(f'{loc}: unmatched ENDS')
                if len(parts)>1 and parts[1].upper()!=scope_now:raise NetlistError(f'{loc}: mismatched ENDS')
                scope_now='__TOP__';continue
            if cmd=='.MODEL':
                if len(parts)<3:raise NetlistError(f'{loc}: malformed MODEL')
                scopes[scope_now]['models'].add(parts[1].upper());continue
            if cmd.startswith('.'):
                if cmd not in ('.END','.OP','.TRAN','.AC','.DC','.OPTIONS','.PARAM','.SAVE','.PRINT','.PROBE','.MEAS','.CONTROL','.ENDC'):
                    raise NetlistError(f'{loc}: unrecognized directive {cmd}')
                continue
            kind=cmd[0]
            if kind not in 'RCLVDQXIBEFGH':raise NetlistError(f'{loc}: unrecognized component {cmd}')
            if cmd in scopes[scope_now]['names']:raise NetlistError(f'{loc}: duplicate component {cmd} in {scope_now}')
            scopes[scope_now]['names'].add(cmd)
            scopes[scope_now]['lines'].append({'location':loc,'tokens':parts,'kind':kind})
        if scope_now!='__TOP__':raise NetlistError('unclosed SUBCKT in '+str(path))
    # Handle SPICE top and all subcircuit model references.
    n=0;refs=[];instances=[];models=set().union(*(v['models'] for v in scopes.values()))
    for scope,s in scopes.items():
        for e in s['lines']:
            tokens=e['tokens'];kind=e['kind'];n+=1
            if kind in 'RCL':
                if len(tokens)!=4:raise NetlistError(f'{e["location"]}: {kind} requires 2 pins and one value')
            elif kind=='V' or kind=='I':
                if len(tokens)<4:raise NetlistError(f'{e["location"]}: {kind} source missing pins/value')
            elif kind=='D':
                if len(tokens)!=4 or tokens[3].upper() not in models:raise NetlistError(f'{e["location"]}: undefined diode model')
            elif kind=='Q':
                if len(tokens)!=5 or tokens[4].upper() not in models:raise NetlistError(f'{e["location"]}: undefined transistor model')
            elif kind=='X':
                if len(tokens)<4:raise NetlistError(f'{e["location"]}: malformed X instance')
                target=tokens[-1].upper()
                if target not in scopes:raise NetlistError(f'{e["location"]}: undefined SUBCKT {target}')
                expected=len(scopes[target]['pins']);got=len(tokens)-2
                if got!=expected:raise NetlistError(f'{e["location"]}: {target} expects {expected} nodes, got {got}')
                instances.append({'site':e['location'],'name':tokens[0],'subckt':target,'actual_nodes':tokens[1:-1]})
            else:raise NetlistError(f'{e["location"]}: {kind} syntax unsupported: fail closed')
            refs.append(e['location'])
    return {'deck':deck.name,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in all_files},'subcircuits':{k:len(v['pins']) for k,v in scopes.items() if k!='__TOP__'},'components':n,'top_level_components':len(scopes['__TOP__']['lines']),'subcircuit_instances':instances,'models':sorted(models),'source_structure_only':True,'numerical_circuit_simulation':False,'physical_measured':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,default=R08_DEFAULT);ap.add_argument('--output',type=Path);a=ap.parse_args()
    try:
        found=[parse(f) for f in sorted(a.source_dir.glob('*.cir'))]
        if len(found)!=6:raise NetlistError(f'expected six active circuit decks, found {len(found)}')
        out={'status':'PASS','decks':found,'warnings':['Static syntax/ports/defined-model check only. No nodal KCL, transistor convergence, device availability, or physical measurements performed.']}
        print(json.dumps({'status':'PASS','decks':[{k:d[k] for k in ('deck','components','top_level_components','subcircuits')} for d in found]},indent=2))
    except (NetlistError,ValueError,OSError) as e:
        out={'status':'FAIL','error':str(e)};print('FAIL',e)
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    raise SystemExit(0 if out['status']=='PASS' else 1)
if __name__=='__main__':main()
