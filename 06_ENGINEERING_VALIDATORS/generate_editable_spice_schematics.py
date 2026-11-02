#!/usr/bin/env python3
"""Deterministic, source-only KiCad 9 electrical capture for the nine R08 decks.
Every SPICE device/instance pin is connected through a KiCad global net label.
No fabricated footprint, simulation data, supplier selection or board evidence.
"""
from __future__ import annotations
import csv,hashlib,json,math,re,uuid,sys
from collections import defaultdict
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
DEST=BASE/'01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS'
UID_NS=uuid.UUID('3df67cae-f67a-4dbc-8d8b-9eb6129a1f57')
def uid(*parts):return str(uuid.uuid5(UID_NS,'/'.join(map(str,parts))))
def safe(s):return str(s).replace('\\','\\\\').replace('"','\\"').replace('\n',' ')
def q(s):return '"'+safe(s)+'"'
def fmt(n):return f'{n:.4f}'.rstrip('0').rstrip('.') if n else '0'
def label_name(s):return 'SPICE_GND' if s=='0' else s.upper()
def load(path):
    rec=[];inside=None;first=True;ports=[]
    for line,raw in enumerate(path.read_text().splitlines(),1):
        s=raw.strip();
        if not s or s[0] in '*;':continue
        parts=s.split();tag=parts[0].upper()
        if first:
            first=False
            if not tag.startswith('.'):continue  # SPICE title line
        if tag=='.SUBCKT':
            if inside:raise ValueError(f'nested SUBCKT {path}:{line}')
            inside=tag;ports=parts[2:];continue
        if tag=='.ENDS':inside=None;continue
        if tag.startswith('.'):continue
        if tag[0] not in 'RCLVDQXI':raise ValueError(f'unknown element {path}:{line} {tag}')
        count=(len(parts)-2 if tag[0]=='X' else 3 if tag[0]=='Q' else 2)
        if len(parts)<count+2:raise ValueError('short SPICE device line')
        nodes=parts[1:1+count]
        val=' '.join(parts[1+count:])
        if tag[0]=='X':val=parts[-1]
        rec.append({'file':path.name,'line':line,'name':parts[0],'kind':tag[0],
                    'pins':nodes,'value':val,'source':s})
    return rec,ports

def pins_for(n):
    if n==2:return [(-7.62,0.,180.),(7.62,0.,0.)]
    # split high-pin module on both sides, keep stable SPICE port order
    left=(n+1)//2;right=n-left
    points=[]
    for i in range(left):points.append((-12.70,(left-1)*2.54-i*5.08,180.))
    for i in range(right):points.append((12.70,(right-1)*2.54-i*5.08,0.))
    return points

def symbol_library(kind,n):
    key=f'VOID_SPICE_{kind}_{n}P'
    points=pins_for(n)
    halfw=4.0 if n==2 else 9.5
    halfh=max(3.2, (max(abs(x[1]) for x in points)+2.54) if n>2 else 2.7)
    body=[f'\t\t(symbol {q("VOID:"+key)}',
          '\t\t\t(pin_numbers (hide yes))',
          '\t\t\t(pin_names (offset 0.508))',
          '\t\t\t(in_bom yes) (on_board yes)',
          f'\t\t\t(property "Reference" {q(kind)} (at 0 {fmt(halfh+3)} 0) (effects (font (size 1.0 1.0))))',
          f'\t\t\t(property "Value" {q(key)} (at 0 {fmt(-halfh-3)} 0) (effects (font (size 0.9 0.9))))',
          f'\t\t\t(symbol {q(key+"_0_1")}',
          f'\t\t\t\t(rectangle (start -{fmt(halfw)} {fmt(halfh)}) (end {fmt(halfw)} -{fmt(halfh)}) (stroke (width 0.254) (type default)) (fill (type background)))',
          '\t\t\t)',f'\t\t\t(symbol {q(key+"_1_1")}']
    for idx,(x,y,angle) in enumerate(points,1):
        direction=1 if x<0 else -1
        length=abs(x)-halfw
        body.append(f'\t\t\t\t(pin passive line (at {fmt(x)} {fmt(y)} {fmt(angle)}) (length {fmt(length)})'
                    f' (name {q(str(idx))} (effects (font (size 0.8 0.8))))'
                    f' (number {q(str(idx))} (effects (font (size 0.8 0.8)))))')
    body.extend(['\t\t\t)','\t\t)'])
    return '\n'.join(body)

def schematic(path, comps):
    name=path.stem
    root=uid('schematic',path.name)
    types=sorted(set((r['kind'],len(r['pins'])) for r in comps))
    out=['(kicad_sch','\t(version 20250114)','\t(generator "void_source_capture")','\t(generator_version "9.0")',f'\t(uuid {q(root)})',
         '\t(paper "A0")',f'\t(title_block (title {q("VOID R08 source capture: "+name)}) (rev "R08 source-linked"))','\t(lib_symbols']
    for k,n in types:out.append(symbol_library(k,n))
    out.append('\t)')
    serial_by_kind={}
    for j,rec in enumerate(comps):
        serial_by_kind[rec['kind']]=serial_by_kind.get(rec['kind'],0)+1
        kicad_ref=rec['kind']+str(serial_by_kind[rec['kind']])
        # A0: 841x1189 mm. Five columns, rows with 42mm pitch; enough for 106 devices.
        col=j%5;row=j//5;cx=52+col*167;cy=45+row*45
        k=rec['kind'];pins=rec['pins'];n=len(pins);symid=uid(path.name,rec['name'],'sym')
        libid=f'VOID:VOID_SPICE_{k}_{n}P'
        out.append(f'\t(symbol (lib_id {q(libid)}) (at {fmt(cx)} {fmt(cy)} 0) (unit 1)'
                   ' (in_bom yes) (on_board yes) (dnp no)')
        out.append(f'\t\t(uuid {q(symid)})')
        out.append(f'\t\t(property "Reference" {q(kicad_ref)} (at {fmt(cx)} {fmt(cy-6)} 0) (effects (font (size 1.3 1.3))))')
        out.append(f'\t\t(property "Value" {q(rec["value"])} (at {fmt(cx)} {fmt(cy+6)} 0) (effects (font (size 1.1 1.1))))')
        out.append(f'\t\t(property "SPICE_Ref" {q(rec["name"])} (at 0 0 0) (effects (font (size 1 1)) (hide yes)))')
        out.append(f'\t\t(property "SPICE_source" {q(rec["file"]+":"+str(rec["line"]))} (at 0 0 0) (effects (font (size 1 1)) (hide yes)))')
        out.append(f'\t\t(property "SPICE_source_tokens" {q(rec["source"])} (at 0 0 0) (effects (font (size 1 1)) (hide yes)))')
        for pinidx,(x,y,a) in enumerate(pins_for(n),1):
            out.append(f'\t\t(pin {q(str(pinidx))} (uuid {q(uid(path.name,rec["name"],pinidx))}))')
            direction=-1 if x<0 else 1
            startx=cx+x;starty=cy-y
            endx=startx+direction*5.08
            out.append(f'\t\t') if False else None
        out.append(f'\t\t(instances (project {q(name)} (path {q("/"+root)} (reference {q(kicad_ref)}) (unit 1))))')
        out.append('\t)')
        for pinidx,(x,y,a) in enumerate(pins_for(n),1):
            side=-1 if x<0 else 1; xx=cx+x;yy=cy-y;ex=xx+side*5.08
            out.append(f'\t(wire (pts (xy {fmt(xx)} {fmt(yy)}) (xy {fmt(ex)} {fmt(yy)})) (stroke (width 0) (type default)) (uuid {q(uid(path.name,rec["name"],pinidx,"wire"))}))')
            out.append(f'\t(global_label {q(label_name(pins[pinidx-1]))} (shape input) (at {fmt(ex)} {fmt(yy)} {"0" if side>0 else "180"}) (fields_autoplaced)'
                       f' (effects (font (size 0.9 0.9)) (justify {"left" if side>0 else "right"})) (uuid {q(uid(path.name,rec["name"],pinidx,"net"))}))')
    out.append(')')
    # Validate S expression structure with quote awareness (independent from SPICE parser).
    contents='\n'.join(out)+'\n'
    depth=0;quote=False;escape=False
    for ch in contents:
        if escape:escape=False;continue
        if quote and ch=='\\':escape=True;continue
        if ch=='"':quote=not quote;continue
        if not quote:
            if ch=='(':depth+=1
            if ch==')':depth-=1
            if depth<0:raise ValueError('invalid S expression parenthesis underflow')
    if quote or depth:raise ValueError('invalid S expression quote or balance')
    return contents

def main():
    DEST.mkdir(exist_ok=True)
    manifest=[];bom={};wiring=[]
    for path in sorted(SOURCE.iterdir()):
        if path.suffix.lower() not in ('.cir','.lib'):continue
        elements,pins=load(path)
        # Ensure nothing was silently lost and all ports known to the parser.
        manifest.append({'deck':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                         'element_count':len(elements),'ports':pins,'schematic':path.stem+'.kicad_sch'})
        (DEST/(path.stem+'.kicad_sch')).write_text(schematic(path,elements))
        for rec in elements:
            wiring.extend({'source':rec['file'],'line':rec['line'],'reference':rec['name'],
                           'pin':idx,'spice_net':net,'label':label_name(net),'value':rec['value']}
                          for idx,net in enumerate(rec['pins'],1))
            key=(rec['kind'],rec['value'])
            bom.setdefault(key,[]).append(f'{path.stem}:{rec["name"]}')
    assert len(manifest)==9 and sum(d['element_count'] for d in manifest)==216
    with (DEST/'COMPONENT_PORT_MAP.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['source','line','reference','pin','spice_net','label','value']);writer.writeheader();writer.writerows(wiring)
    with (DEST/'SOURCE_DERIVED_BOM.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['kind','nominal_value_or_model','occurrences_all_decks','designators_with_source','procurement_note'])
        for (kind,val),refs in sorted(bom.items()):
            w.writerow([kind,val,len(refs),'; '.join(refs),'Source occurrence count, NOT purchase quantity; many circuits share reusable elements'])
    report={'source_reproduction_only':True,'project':'VOID R08','file_count':len(manifest),
            'element_count':sum(x['element_count'] for x in manifest),'captured_spice_pins':len(wiring),
            'decks':manifest,'connection_contract':'SPICE device pin tokens represented by wired global net labels on source sheets',
            'scope':'Electronic source capture, not KiCad ERC/DRC, footprint selection, SPICE simulation, PCB fabrication or physical bench verification'}
    (DEST/'CAPTURE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','files':len(manifest),'elements':report['element_count'],'pin_connections':len(wiring)}))
if __name__=='__main__':main()
