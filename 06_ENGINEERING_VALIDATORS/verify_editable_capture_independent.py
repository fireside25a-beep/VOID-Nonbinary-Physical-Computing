#!/usr/bin/env python3
"""Independent KiCad-vs-SPICE connectivity audit.  Does not invoke the generator.
Checks actual sheet pin origins, wires, label endpoints, source references and hashes.
Source-capture validation only; a KiCad CLI/ERC run is separately required.
"""
import csv, hashlib, json, re, sys
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
K=R/'01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS'
OUT=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY/KICAD_INDEPENDENT_CONNECTIVITY_VALIDATION.json'
TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')
def parse(t):
    stack=[];roots=[]
    for m in TOKEN.finditer(t):
        tok=m.group()
        if tok=='(':
            obj=[]
            if stack:stack[-1].append(obj)
            else:roots.append(obj)
            stack.append(obj)
        elif tok==')':
            if not stack:raise ValueError('extra closing parenthesis')
            stack.pop()
        else:
            if tok[0]=='"':tok=json.loads(tok)
            if not stack:raise ValueError('bare token outside expression')
            stack[-1].append(tok)
    if stack or len(roots)!=1:raise ValueError('unbalanced or multiple S-expressions')
    return roots[0]
def children(obj,tag):return [x for x in obj if isinstance(x,list) and x and x[0]==tag]
def one(obj,tag):
    got=children(obj,tag)
    if len(got)!=1:raise ValueError(f'{tag} expected once, got {len(got)}')
    return got[0]
def prop(obj,key):
    got=[x for x in children(obj,'property') if x[1]==key]
    if len(got)!=1:raise ValueError(f'missing/duplicate property {key}')
    return got[0][2]
def pos(seq):return tuple(round(float(v),3) for v in seq[1:3])
def norm(x):return 'SPICE_GND' if x=='0' else x.upper()
def deck_cards(path):
    cards=[];first=True
    for line_no,raw in enumerate(path.read_text().splitlines(),1):
        txt=raw.strip()
        if not txt or txt.startswith(('*',';')):continue
        words=txt.split();tag=words[0].upper()
        if first:
            first=False
            if not tag.startswith('.'):continue
        if tag.startswith('.'):continue
        typ=tag[0]
        if typ not in 'RCLVDQXI':raise ValueError(f'unsupported element at {path}:{line_no}')
        count=(len(words)-2 if typ=='X' else 3 if typ=='Q' else 2)
        if len(words)<count+2:raise ValueError('bad card')
        cards.append((words[0],words[1:1+count],path.name,line_no,txt))
    return cards

def verify(path):
    root=parse(path.read_text())
    if root[0]!='kicad_sch':raise ValueError('wrong file root')
    lib=one(root,'lib_symbols')
    defs={x[1]:x for x in children(lib,'symbol')}
    records=deck_cards(S/(path.stem+('.lib' if (S/(path.stem+'.lib')).exists() else '.cir')))
    items=children(root,'symbol');labels=children(root,'global_label');wires=children(root,'wire')
    if len(items)!=len(records):raise ValueError(f'{path}: device count {len(items)} != {len(records)}')
    label_ends=Counter((pos(one(l,'at')),l[1]) for l in labels)
    segments=Counter()
    for w in wires:
        coords=children(one(w,'pts'),'xy')
        if len(coords)!=2:raise ValueError('nonsegment wire')
        segments[(pos(coords[0]),pos(coords[1]))]+=1
    reference={prop(x,'SPICE_Ref') if children(x,'property') and any(z[1]=='SPICE_Ref' for z in children(x,'property')) else prop(x,'Reference'):x for x in items}
    if len(reference)!=len(items):raise ValueError('duplicate source reference')
    checked=0
    for designator,nets,src,lineno,raw in records:
        sym=reference.get(designator)
        if sym is None:raise ValueError(f'uncaptured {designator}')
        if prop(sym,'SPICE_source')!=f'{src}:{lineno}' or prop(sym,'SPICE_source_tokens')!=raw:
            raise ValueError(f'broken provenance {designator}')
        origin=pos(one(sym,'at'))
        libid=one(sym,'lib_id')[1];definition=defs.get(libid)
        if definition is None:raise ValueError(f'library missing {libid}')
        pin_defs=[]
        for sub in children(definition,'symbol'):
            pin_defs.extend(children(sub,'pin'))
        pind={one(p,'number')[1]:pos(one(p,'at')) for p in pin_defs}
        if len(pind)!=len(nets):raise ValueError(f'{designator} pin count')
        uuid_pins=children(sym,'pin')
        if sorted(int(p[1]) for p in uuid_pins)!=list(range(1,len(nets)+1)):
            raise ValueError(f'{designator} instance pin set')
        for i,net in enumerate(nets,1):
            dx,dy=pind[str(i)]
            pin=(round(origin[0]+dx,3),round(origin[1]-dy,3))
            touching=[(a,b) for a,b in segments if a==pin or b==pin]
            matches=0
            for a,b in touching:
                far=b if a==pin else a
                matches+=label_ends[(far,norm(net))]
            if matches!=1:raise ValueError(f'{designator} pin {i} ({net}) not wired to exactly one intended global net label, got {matches}')
            checked+=1
    if len(labels)!=checked or len(wires)!=checked:raise ValueError('stray wires/labels detected')
    return {'source':path.stem,'devices':len(records),'tested_pin_net_connections':checked,
            'source_sha256':hashlib.sha256((S/(path.stem+('.lib' if (S/(path.stem+'.lib')).exists() else '.cir'))).read_bytes()).hexdigest(),
            'schematic_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    outputs=[]
    try:
        for path in sorted(K.glob('*.kicad_sch')):
            outputs.append(verify(path))
        if len(outputs)!=9 or sum(x['devices'] for x in outputs)!=216 or sum(x['tested_pin_net_connections'] for x in outputs)!=459:
            raise ValueError('incomplete source capture coverage')
        data={'status':'PASS','verifier':'independent_reader_spice_and_kicad_ast_v1',
              'total_devices':sum(x['devices'] for x in outputs),
              'total_pin_net_connections':sum(x['tested_pin_net_connections'] for x in outputs),
              'files':outputs,'scope':'source capture connectivity; not ERC/DRC nor fabrication'}
    except Exception as e:
        data={'status':'FAIL','error':repr(e),'files_completed':outputs}
    OUT.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='files'},indent=2))
    return 0 if data['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
