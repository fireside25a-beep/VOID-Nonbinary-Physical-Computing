#!/usr/bin/env python3
"""Sharp source-grounded vector circuit drawings of the 2x4 material carrier.
All actual R symbols, values, net endpoints and reference names are parsed from
VOID_PRIMITIVE_MATERIAL_INTERFACE.lib. The complete source's additional
field/axis/core connections remain in its editable KiCad capture.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from hashlib import sha256
import re, json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE/VOID_PRIMITIVE_MATERIAL_INTERFACE.lib'
DEST=ROOT/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY/03_BUILD_REFERENCE'
parts={}
for line_number,line in enumerate(SRC.read_text().splitlines(),1):
    t=line.strip().split()
    if len(t)==4 and t[0].startswith('R_'):
        name,a,b,value=t
        assert name not in parts
        parts[name]=(a,b,value,line_number)

def check(name,a,b):
    assert name in parts,(name,'missing')
    x,y,value,line=parts[name]
    assert (x,y)==(a,b),(name,'unexpected terminals',x,y,a,b)
    return value

base_style='''<style>svg{background:#fff} .node{fill:#fff;stroke:#202d40;stroke-width:2} .wire{fill:none;stroke:#263747;stroke-width:2.5;stroke-linecap:round} .res{fill:#fff;stroke:#1b344d;stroke-width:2.5} .ref{fill:#1e293b;font:13px system-ui,Arial,sans-serif} .val{fill:#475569;font:13px system-ui,Arial,sans-serif} .net{fill:#0f365c;font:bold 14px system-ui,Arial,sans-serif} .header{fill:#0f172a;font:bold 25px system-ui,Arial,sans-serif} .foot{fill:#475569;font:13px system-ui,Arial,sans-serif} .chip{fill:#ebf1f6;stroke:#577188;stroke-width:1.5} .junction{fill:#1b344d}</style>'''
def head(title,w,h):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',base_style,f'<rect width="{w}" height="{h}" fill="#ffffff"/>',f'<text class="header" x="60" y="52">{escape(title)}</text>']
def wire(out,x1,y1,x2,y2):out.append(f'<path class="wire" d="M{x1},{y1} L{x2},{y2}"/>')
def dot(out,x,y):out.append(f'<circle class="junction" cx="{x}" cy="{y}" r="4"/>')
def t(out,cls,x,y,s,anchor=None):out.append(f'<text class="{cls}" x="{x}" y="{y}"'+(f' text-anchor="{anchor}"' if anchor else '')+f'>{escape(str(s))}</text>')
def resistor_h(out,x1,x2,y,name,value):
    mid=(x1+x2)/2;wire(out,x1,y,mid-36,y);wire(out,mid+36,y,x2,y)
    out.append(f'<rect class="res" x="{mid-36}" y="{y-13}" width="72" height="26" rx="2"/>')
    t(out,'ref',mid,y-29,name,'middle');t(out,'val',mid,y+5,value,'middle')
def resistor_v(out,x,y1,y2,name,value,label_to='right'):
    mid=(y1+y2)/2;wire(out,x,y1,x,mid-23);wire(out,x,mid+23,x,y2)
    out.append(f'<rect class="res" x="{x-13}" y="{mid-23}" width="26" height="46" rx="2"/>')
    xo=x+19 if label_to=='right' else x-19
    anch='start' if label_to=='right' else 'end'
    t(out,'ref',xo,mid-5,name,anch);t(out,'val',xo,mid+13,value,anch)

def draw_carrier():
    out=head('VOID R08 • 2×4 material contacts + 22k sheet links',1560,1400)
    t(out,'foot',60,85,'Electrical connections parsed from the active .lib; VREF labels are ONE COMMON NET. Not a PCB layout.')
    xs=[205,570,935,1300]; ys=[465,910]
    # Sheet links, exactly 3 per row and 4 between rows.
    for r,y in enumerate(ys,1):
        for col in range(1,4):
            name=f'R_SHEET_H_{r}{col}';value=check(name,f'F_{r}{col}',f'F_{r}{col+1}')
            resistor_h(out,xs[col-1],xs[col],y,name,value)
    for col,x in enumerate(xs,1):
        name=f'R_SHEET_V_1{col}';value=check(name,f'F_1{col}',f'F_2{col}')
        resistor_v(out,x,ys[0],ys[1],name,value,'right' if col<4 else 'left')
    for r,y in enumerate(ys,1):
        for col,x in enumerate(xs,1):
            suf=f'{r}{col}';pad='PAD_'+suf;f='F_'+suf
            ac=check('R_ACT_'+suf,'VREF',pad)
            guard=check('R_ACT_GUARD_'+suf,pad,f)
            if r==1:
                t(out,'net',x,123,'VREF','middle')
                resistor_v(out,x,133,258,'R_ACT_'+suf,ac,'right' if col<4 else 'left')
                dot(out,x,258);t(out,'net',x,278,pad,'middle')
                resistor_v(out,x,295,y,'R_ACT_GUARD_'+suf,guard,'right' if col<4 else 'left')
            else:
                resistor_v(out,x,y,1080,'R_ACT_GUARD_'+suf,guard,'right' if col<4 else 'left')
                dot(out,x,1080);t(out,'net',x,1104,pad,'middle')
                resistor_v(out,x,1115,1240,'R_ACT_'+suf,ac,'right' if col<4 else 'left')
                t(out,'net',x,1265,'VREF','middle')
            out.append(f'<circle class="node" cx="{x}" cy="{y}" r="6"/>')
            t(out,'net',x+13,y+20,f)
    t(out,'foot',60,1330,'8 replaceable nominal 10M contact branches + 8 fixed 1k SERIES resistors + 10 spatial 22k links.')
    t(out,'foot',60,1362,'Additional 220k node returns are on the companion sheet. No grounded 1k guard ring exists in source.')
    out.append('</svg>')
    return '\n'.join(out)+'\n'

def draw_returns():
    out=head('VOID R08 • 2×4 material-sheet returns to RET',1550,960)
    t(out,'foot',60,85,'All 8 R_NODE_RET resistors are verified against the source; repeated RET labels refer to the same net.')
    for idx in range(8):
        r=idx//4+1;col=idx%4+1;suf=f'{r}{col}'
        name='R_NODE_RET_'+suf;value=check(name,'F_'+suf,'RET')
        block=idx%2;line=idx//2;x=110+block*740;y=205+line*170
        t(out,'net',x,y+5,'F_'+suf)
        wire(out,x+70,y,x+105,y)
        resistor_h(out,x+105,x+440,y,name,value)
        wire(out,x+440,y,x+510,y)
        t(out,'net',x+515,y+5,'RET')
    t(out,'foot',60,900,'These return resistors are independent of the 1k series contacts. Do not add second probe loads from the SPICE deck.')
    out.append('</svg>')
    return '\n'.join(out)+'\n'

DEST.mkdir(parents=True,exist_ok=True)
a=draw_carrier();b=draw_returns()
(DEST/'MATERIAL_CARRIER_CONTACT_AND_SHEET.svg').write_text(a)
(DEST/'MATERIAL_CARRIER_NODE_RETURNS.svg').write_text(b)
# Source identity travels with the generated vector sheets.
report={'status':'PASS','source':SRC.name,'sha256':sha256(SRC.read_bytes()).hexdigest(),
        'svg_files':['MATERIAL_CARRIER_CONTACT_AND_SHEET.svg','MATERIAL_CARRIER_NODE_RETURNS.svg'],
        'source_cards_shown':34,'sheet_A_cards':26,'sheet_B_cards':8,
        'interpretation':'exact source resistor connectivity; edit source for schematic edits, not production KiCad ERC/PCB'}
(DEST/'MATERIAL_CARRIER_VECTOR_CAPTURE.json').write_text(json.dumps(report,indent=2)+'\n')
print('MATERIAL_CARRIER_VECTOR_PASS',json.dumps(report))
