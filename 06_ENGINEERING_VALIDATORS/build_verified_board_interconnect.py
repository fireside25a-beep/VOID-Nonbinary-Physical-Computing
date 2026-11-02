#!/usr/bin/env python3
"""Create four electrically connected KiCad 9 interconnect sheets from K06 source-expanded pinmap.
No fabricated active AFE/ADC/DAC components, guessed footprints, or physical measurement results.
Checks the independently extracted 175-element circuit against every connector net.
"""
from __future__ import annotations
import csv, hashlib, json, re, subprocess, uuid
from collections import Counter, defaultdict
from pathlib import Path

R=Path(__file__).resolve().parents[1]
H=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY'
DEST=H/'04_VERIFIED_BOARD_INTERCONNECT'
K=H/'K06_PROTOTYPE_CONNECTOR_PINOUT.csv'
BOM=H/'K06_HIERARCHICAL_EXPANDED_BOM.csv'
SRC=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
NS=uuid.UUID('252d4a55-afb6-47de-8746-525461cd71b9')
MODULES={
 'P1_BENCH_POWER_AND_K05_BIAS':('P1_POWER','K05_WEIGHTED'),
 'P2_MEASUREMENT_AND_CORE_TEST':('P2_ACQUISITION','K06_CORE'),
 'P3_PROTECTED_STIMULUS_PORTS':('P3_CONTROL',),
 'P4_2x4_MATERIAL_AND_AXES':('P4_CONTACT_CARRIER',),
}
def uid(*p):return str(uuid.uuid5(NS,'/'.join(map(str,p))))
def quoted(s):return json.dumps(str(s),ensure_ascii=True)
def fl(x):return f'{x:.3f}'.rstrip('0').rstrip('.')
def netname(s):return 'SPICE_GND' if s=='0' else s.upper()
def records(path=K):
    rows=list(csv.DictReader(path.open(newline='')))
    if not rows:raise ValueError('no connector records')
    keys=Counter((r['connector'],r['pin']) for r in rows)
    dup=[k for k,v in keys.items() if v!=1]
    if dup:raise ValueError('duplicate connector pin: '+str(dup))
    try: pin_ok=all(0<int(r['pin'])<100 and r['source_net'] and r['proposed_owner_board'] for r in rows)
    except ValueError:pin_ok=False
    if not pin_ok:raise ValueError('invalid connector pin or source net')
    groups=defaultdict(list)
    for r in rows:groups[r['connector']].append(r)
    for name,pins in groups.items():
        numbers=sorted(int(x['pin']) for x in pins)
        if numbers!=list(range(1,len(numbers)+1)):raise ValueError('connector hole '+name)
    allnets={v for r in csv.DictReader(BOM.open(newline='')) for v in r['physical_nets'].split(';')}
    bad=sorted({r['source_net'] for r in rows}-allnets)
    if bad:raise ValueError('connector pin points outside K06 native netlist: '+str(bad))
    actual_groups={r['proposed_owner_board'] for r in rows}
    required={g for groups in MODULES.values() for g in groups}
    if actual_groups!=required:raise ValueError('unmapped or unknown board group '+str(actual_groups^required))
    if len(rows)!=78 or len(groups)!=15:raise ValueError('regression in actual K06 connector contract')
    return rows,groups

def library_symbol(n):
    key=f'VOID_K06_CON_{n}'
    yt=(n-1)*1.27
    body=[f'    (symbol {quoted("VOID:"+key)}',
          '      (pin_numbers (hide yes)) (pin_names (offset 0.508))',
          '      (in_bom yes) (on_board yes)',
          f'      (property "Reference" "J" (at 0 {fl(yt+5)} 0) (effects (font (size 1 1))))',
          f'      (property "Value" {quoted(key)} (at 0 {fl(-yt-5)} 0) (effects (font (size 1 1))))',
          f'      (symbol {quoted(key+"_0_1")}',
          f'        (rectangle (start -9.5 {fl(yt+3.81)}) (end 9.5 {fl(-yt-3.81)}) (stroke (width 0.254) (type default)) (fill (type background)))',
          '      )',f'      (symbol {quoted(key+"_1_1")}']
    for i in range(1,n+1):
        y=(n+1-2*i)*1.27
        body.append(f'        (pin passive line (at -12.7 {fl(y)} 180) (length 3.2)'
                    f' (name {quoted(str(i))} (effects (font (size 0.85 0.85))))'
                    f' (number {quoted(str(i))} (effects (font (size 0.85 0.85)))))')
    body += ['      )','    )']
    return '\n'.join(body)

def schematic(name,connector_map):
    grouped=sorted(connector_map.items())
    sid=uid('root',name)
    types=sorted({len(v) for _,v in grouped})
    out=['(kicad_sch','  (version 20250114)','  (generator "void_verified_interconnect")',
         '  (generator_version "9.0")',f'  (uuid {quoted(sid)})',
         '  (paper "A1")',f'  (title_block (title {quoted("VOID K06 verified: "+name)}) (rev "R08 electrical interface"))',
         '  (lib_symbols']
    out += [library_symbol(n) for n in types]
    out.append('  )')
    for j,(conn,pins) in enumerate(grouped):
        n=len(pins); x=72+(j%3)*175; y=67+(j//3)*95
        symid=uid(name,conn,'symbol')
        out += [f'  (symbol (lib_id {quoted("VOID:VOID_K06_CON_"+str(n))}) (at {fl(x)} {fl(y)} 0)'
                ' (unit 1) (in_bom yes) (on_board yes) (dnp no)',
                f'    (uuid {quoted(symid)})',
                f'    (property "Reference" {quoted("J"+str(j+1))} (at {fl(x)} {fl(y-35)} 0) (effects (font (size 1.4 1.4))))',
                f'    (property "Value" {quoted(conn)} (at {fl(x)} {fl(y+35)} 0) (effects (font (size 1.2 1.2))))',
                f'    (property "K06_connector" {quoted(conn)} (at 0 0 0) (effects (font (size 1 1)) (hide yes)))',
                f'    (property "K06_source" {quoted("K06 R08 flat source, 175 primitives")} (at 0 0 0) (effects (font (size 1 1)) (hide yes)))']
        by={int(r['pin']):r for r in pins}
        for i in range(1,n+1):out.append(f'    (pin {quoted(str(i))} (uuid {quoted(uid(name,conn,i,"pin"))}))')
        out += [f'    (instances (project {quoted(name)} (path {quoted("/"+sid)} (reference {quoted("J"+str(j+1))}) (unit 1))))','  )']
        for i in range(1,n+1):
            py=y-(n+1-2*i)*1.27; px=x-12.7; ex=px-5.08
            net=netname(by[i]['source_net'])
            out.append(f'  (wire (pts (xy {fl(px)} {fl(py)}) (xy {fl(ex)} {fl(py)}))'
                       f' (stroke (width 0) (type default)) (uuid {quoted(uid(name,conn,i,"wire"))}))')
            out.append(f'  (global_label {quoted(net)} (shape input) (at {fl(ex)} {fl(py)} 180)'
                       f' (fields_autoplaced) (effects (font (size 1 1)) (justify right))'
                       f' (uuid {quoted(uid(name,conn,i,"label"))}))')
    out.append(')')
    return '\n'.join(out)+'\n'

def dot_sheet(name,connector_map):
    out=['graph G {','graph [rankdir=LR,fontname="DejaVu Sans",bgcolor="white",pad="0.3",ranksep="0.6",nodesep="0.35",label='+quoted('VOID / R08  '+name+'\nSOURCE-MAPPED INTERCONNECT ONLY')+',labelloc=t,fontsize=22];',
         'node [fontname="DejaVu Sans",fontsize=10,shape=record,style="filled",fillcolor="#f2f7f9",color="#355065"];','edge [color="#7a8c9c",penwidth=1];']
    for idx,(conn,pins) in enumerate(sorted(connector_map.items())):
        fields=[]
        for p in sorted(pins,key=lambda v:int(v['pin'])):
            fields.append(f'{p["pin"]}: {p["source_net"]}'.replace('"',''))
        label='{'+conn+'|'+ ' | '.join(fields)+'}'
        out.append(f'j{idx} [label={quoted(label)}];')
    out += ['}']
    return '\n'.join(out)+'\n'

def main():
    rows,grp=records()
    DEST.mkdir(parents=True,exist_ok=True)
    result=[]
    for name,owners in MODULES.items():
        use={k:v for k,v in grp.items() if v[0]['proposed_owner_board'] in owners}
        sheet=DEST/(name+'.kicad_sch'); sheet.write_text(schematic(name,use))
        dot=DEST/(name+'.dot');dot.write_text(dot_sheet(name,use))
        svg=DEST/(name+'.svg')
        p=subprocess.run(['dot','-Tsvg',str(dot),'-o',str(svg)],capture_output=True,text=True)
        if p.returncode:raise RuntimeError('SVG render failure '+p.stderr)
        result.append({'module':name,'schematic':sheet.name,'svg':svg.name,'connectors':len(use),
                       'pins':sum(len(a) for a in use.values()),'sha256':hashlib.sha256(sheet.read_bytes()).hexdigest()})
    assert len(result)==4 and sum(x['pins'] for x in result)==78 and sum(x['connectors'] for x in result)==15
    manifest={'schema':'VOID_K06_R08_FOUR_MODULE_INTERCONNECT_V1','source_file':SRC.name,
      'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),
      'expanded_bom_sha256':hashlib.sha256(BOM.read_bytes()).hexdigest(),
      'connector_map_sha256':hashlib.sha256(K.read_bytes()).hexdigest(),
      'modules':result,'connector_count':15,'pin_count':78,
      'engineering_scope':'Electrical interface/pin-net schematics, not an op-amp/DAC/ADC circuit implementation; no footprint/ERC/DRC/manufacturing acceptance'}
    (DEST/'FOUR_MODULE_INTERCONNECT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('MODULE_SHEETS_PASS',len(result),'modules',sum(x['connectors'] for x in result),'connectors',sum(x['pins'] for x in result),'exact pins')
if __name__=='__main__':main()
