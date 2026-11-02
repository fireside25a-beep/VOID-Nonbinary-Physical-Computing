#!/usr/bin/env python3
"""Independently assert physical connector pin-to-K06-net connections in KiCad S-expressions.
Negative-case mutation tests ensure the verifier detects actual wiring corruption.
"""
from __future__ import annotations
import csv, hashlib, json, sys
from collections import Counter,defaultdict
from pathlib import Path
from verify_editable_capture_independent import parse,children,one,prop,pos
R=Path(__file__).resolve().parents[1]
H=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY'
G=H/'04_VERIFIED_BOARD_INTERCONNECT'
CSV=H/'K06_PROTOTYPE_CONNECTOR_PINOUT.csv'
MODULES={
 'P1_BENCH_POWER_AND_K05_BIAS':('P1_POWER','K05_WEIGHTED'),
 'P2_MEASUREMENT_AND_CORE_TEST':('P2_ACQUISITION','K06_CORE'),
 'P3_PROTECTED_STIMULUS_PORTS':('P3_CONTROL',),
 'P4_2x4_MATERIAL_AND_AXES':('P4_CONTACT_CARRIER',),
}
def norm(s):return 'SPICE_GND' if s=='0' else s.upper()
def validate_sheet(name,raw,rows):
    root=parse(raw)
    if root[0]!='kicad_sch':raise ValueError('invalid kicad_sch root')
    defs={x[1]:x for x in children(one(root,'lib_symbols'),'symbol')}
    instances=children(root,'symbol')
    labels=Counter((pos(one(l,'at')),l[1]) for l in children(root,'global_label'))
    wires=Counter()
    for wire in children(root,'wire'):
        ends=children(one(wire,'pts'),'xy')
        if len(ends)!=2:raise ValueError('invalid wire')
        wires[(pos(ends[0]),pos(ends[1]))]+=1
    expected=defaultdict(dict)
    for r in rows:
        if r['proposed_owner_board'] in MODULES[name]:
            n=int(r['pin']); key=r['connector']
            if n in expected[key]:raise ValueError('duplicate CSV connector pin')
            expected[key][n]=r['source_net']
    found=set();tested=0
    for inst in instances:
        conn=prop(inst,'K06_connector')
        if conn not in expected or conn in found:raise ValueError('unexpected/duplicate connector '+conn)
        found.add(conn)
        origin=pos(one(inst,'at'))
        defn=defs[one(inst,'lib_id')[1]]
        pin_defs={int(one(p,'number')[1]):pos(one(p,'at')) for x in children(defn,'symbol') for p in children(x,'pin')}
        pins=expected[conn]
        if set(pin_defs)!=set(pins):raise ValueError('wrong pins for '+conn)
        if {int(p[1]) for p in children(inst,'pin')}!=set(pins):raise ValueError('pin-instance missing '+conn)
        for number,net in pins.items():
            x,y=pin_defs[number];px=round(origin[0]+x,3);py=round(origin[1]-y,3)
            touches=[(a,b) for a,b in wires if a==(px,py) or b==(px,py)]
            matches=sum(labels[(b if a==(px,py) else a,norm(net))] for a,b in touches)
            if matches!=1:raise ValueError(f'wrong wire/label {conn} pin {number}: {net} matches {matches}')
            tested+=1
    if found!=set(expected):raise ValueError('missing connector '+str(set(expected)-found))
    if sum(labels.values())!=tested or sum(wires.values())!=tested:raise ValueError('extra labels/wires')
    return len(found),tested

def check():
    rows=list(csv.DictReader(CSV.open(newline='')))
    report=[]
    for name in MODULES:
        p=G/(name+'.kicad_sch')
        conn,pin=validate_sheet(name,p.read_text(),rows)
        report.append({'module':name,'connectors':conn,'pins':pin,'schematic_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    if sum(x['connectors'] for x in report)!=15 or sum(x['pins'] for x in report)!=78:
        raise ValueError('module counts regress')
    # True failing mutations, not dummy test assertions.
    baseline=(G/'P3_PROTECTED_STIMULUS_PORTS.kicad_sch').read_text()
    try:validate_sheet('P3_PROTECTED_STIMULUS_PORTS',baseline.replace('"WRITE_A"','"MALFORMED_NET"',1),rows)
    except ValueError:pass
    else:raise ValueError('corrupt net-label mutation was accepted')
    try:validate_sheet('P3_PROTECTED_STIMULUS_PORTS',baseline.replace('  (wire ', '  (corrupt_wire ',1),rows)
    except ValueError:pass
    else:raise ValueError('broken wire mutation was accepted')
    corrupt=[dict(x) for x in rows];corrupt[0]['source_net']='ABSENT_FROM_K06'
    try:validate_sheet('P1_BENCH_POWER_AND_K05_BIAS',(G/'P1_BENCH_POWER_AND_K05_BIAS.kicad_sch').read_text(),corrupt)
    except ValueError:pass
    else:raise ValueError('source-net mutation was accepted')
    out={'schema':'VOID_FOUR_MODULE_INDEPENDENT_PIN_NET_AUDIT_V1','status':'PASS',
         'connected_pins':78,'connectors':15,'modules':report,
         'negative_corruption_tests_passed':3,
         'scope':'KiCad electrical connector mapping; no ERC/DRC, component footprints or physical measurements'}
    (G/'INDEPENDENT_PIN_NET_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print('INDEPENDENT_FOUR_MODULE_PASS 78 pins 15 connectors 3 corruption refusals')

if __name__=='__main__':
    try:check()
    except Exception as exc:
        print('INTERCONNECT_GATE_FAIL',repr(exc),file=sys.stderr);sys.exit(1)
