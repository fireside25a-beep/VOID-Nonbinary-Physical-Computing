#!/usr/bin/env python3
"""Deterministic source-to-svg electrical connectivity drawings; never infer unseen wires.

Treat the first SPICE record as a title; source element order, node names, pin order,
models, component values and file+line citations remain literal. Dot adds a full
bipartite net/terminal topology per source file, including hierarchical X instances.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from xml.sax.saxutils import escape
import csv,hashlib,json,subprocess,sys,re

SRC=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else SRC.parent/'07_SOURCE_RENDERED_CIRCUITS'
OUT.mkdir(exist_ok=True,parents=True)
SUPPORTED={'R':2,'C':2,'L':2,'D':2,'V':2,'I':2,'Q':3,'X':None}


def read_spice(p):
    elements=[]; subs=[]; includes=[]; context='TOP';title=''
    rows=p.read_text(encoding='utf-8',errors='strict').splitlines()
    for ln,raw in enumerate(rows,1):
        text=raw.strip()
        if ln==1: title=text;continue  # SPICE title record, even if it begins with V.
        if not text or text[0] in '*;':continue
        # Reject continuation statements rather than silently guessing a component's pins.
        if text.startswith('+'):raise ValueError(f'{p.name}:{ln}: continuation not supported: {text}')
        text=text.split(';',1)[0].strip()
        words=text.split()
        if not words:continue
        u=words[0].upper()
        if u=='.INCLUDE':
            assert len(words)==2,(p.name,ln,text)
            includes.append(words[1].strip('"\''));continue
        if u=='.SUBCKT':
            assert context=='TOP' and len(words)>=3,(p.name,ln,text)
            context=words[1];subs.append({'name':context,'pins':words[2:],'line':ln});continue
        if u=='.ENDS':
            assert context!='TOP' and (len(words)==1 or words[1].upper()==context.upper()),(p.name,ln,text)
            context='TOP';continue
        if u.startswith('.'):
            assert u in ('.MODEL','.TRAN','.AC','.DC','.OP','.END','.OPTIONS','.PARAM','.CONTROL','.ENDC','.PRINT','.SAVE','.MEAS'),(p.name,ln,text)
            continue
        typ=u[0]
        if typ not in SUPPORTED:raise ValueError(f'Unsupported source element {p.name}:{ln}: {text}')
        pin_count=SUPPORTED[typ]
        if typ=='X':pin_count=len(words)-2
        if pin_count is None or pin_count<2 or len(words)<pin_count+2:
            raise ValueError(f'Invalid pin count {p.name}:{ln}: {text}')
        pins=words[1:1+pin_count]
        value=' '.join(words[1+pin_count:])
        if not value:raise ValueError(f'Missing component value/model {p.name}:{ln}: {text}')
        elements.append({'file':p.name,'line':ln,'group':context,'designator':words[0],
                         'kind':typ,'pins':pins,'value_or_model':value,'source_text':text})
    assert context=='TOP',f'unterminated .SUBCKT in {p.name}'
    return title,elements,subs,includes

def attr(s): return escape(str(s), {'"':'&quot;'})
def svg_text(x,y,s,size=15,color='#1d2f42',weight='normal',anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(s))}</text>'

def schematic_svg(stem,title,rows,page,count,sha):
    # Each element is an *electrically exact net-labelled connection*, not a placement or PCB drawing.
    width=1450;h=180+len(rows)*68+65;res=[]
    res.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}">')
    res+=['<rect width="100%" height="100%" fill="#ffffff"/>', '<rect x="0" y="0" width="100%" height="12" fill="#16405e"/>']
    res.append(svg_text(40,56,stem+' — source-connected elements',25,'#123954','bold'))
    res.append(svg_text(40,86,f'Source title: {title[:125]}',13,'#54697b'))
    res.append(svg_text(40,113,f'Sheet {page}/{count} | source SHA-256 {sha[:24]}… | terminals use exact .cir/.lib node labels',12,'#54697b'))
    res.append(svg_text(40,145,'IDENTIFIER / SOURCE LINE',12,'#52677b','bold'))
    res.append(svg_text(320,145,'TERMINALS & SYMBOL',12,'#52677b','bold'))
    res.append(svg_text(1000,145,'VALUE / MODEL / EXTRA PINS',12,'#52677b','bold'))
    for j,r in enumerate(rows):
        y=182+j*68
        if j%2==0:res.append(f'<rect x="25" y="{y-27}" width="1400" height="60" fill="#f5f8fb"/>')
        res.append(svg_text(40,y,r['designator'],14,'#0c344e','bold'))
        res.append(svg_text(40,y+20,f"{r['file']}:{r['line']}  [{r['group']}]",10,'#6d7c8d'))
        pin=r['pins'];typ=r['kind'];sx=646;ey=y-6
        res.append(f'<path d="M470 {ey} L{sx-45} {ey} M{sx+45} {ey} L850 {ey}" fill="none" stroke="#234e62" stroke-width="2"/>')
        res.append(svg_text(465,ey-10,pin[0],12,'#0b5270',anchor='end'))
        res.append(svg_text(858,ey-10,pin[1],12,'#0b5270'))
        if typ=='R':
            zig=[(sx-43,ey),(sx-31,ey-11),(sx-18,ey+11),(sx-5,ey-11),(sx+8,ey+11),(sx+21,ey-11),(sx+34,ey+11),(sx+43,ey)]
            res.append('<polyline points="'+ ' '.join(f'{a},{b}' for a,b in zig)+'" fill="none" stroke="#153c58" stroke-width="2.2"/>')
        elif typ=='C':
            res.append(f'<path d="M{sx-7} {ey-20}v40 M{sx+7} {ey-20}v40" stroke="#153c58" stroke-width="3"/>')
        elif typ=='L':
            res.append(''.join(f'<path d="M{sx-40+k*20} {ey} a10 11 0 0 1 20 0" fill="none" stroke="#153c58" stroke-width="2"/>' for k in range(4)))
        elif typ=='D':
            res.append(f'<polygon points="{sx-22},{ey-16} {sx-22},{ey+16} {sx+14},{ey}" fill="none" stroke="#153c58" stroke-width="2"/><path d="M{sx+14} {ey-19}v38" stroke="#153c58" stroke-width="3"/>')
        elif typ in ('V','I'):
            res.append(f'<circle cx="{sx}" cy="{ey}" r="25" fill="white" stroke="#153c58" stroke-width="2"/>')
            res.append(svg_text(sx,ey+6,typ,19,'#153c58','bold','middle'))
        elif typ in ('Q','X'):
            res.append(f'<rect x="{sx-36}" y="{ey-24}" width="72" height="48" rx="3" fill="white" stroke="#153c58" stroke-width="2"/>')
            res.append(svg_text(sx,ey+6,typ,19,'#153c58','bold','middle'))
        rest='; '.join(f'pin{i+1}={z}' for i,z in enumerate(pin[2:],2))
        value=r['value_or_model']
        res.append(svg_text(1000,y,value[:58],14,'#142d47','bold'))
        if len(value)>58:res.append(svg_text(1000,y+18,value[58:116],11,'#516879'))
        if rest:res.append(svg_text(1000,y+22,rest[:65],11,'#52677b'))
    res.append(svg_text(40,h-32,'NET LABELS CONNECT GLOBALLY WITHIN THE SAME SPICE SCOPE. This drawing asserts no PCB pinout or physical measurement.',12,'#52677b'))
    res.append('</svg>')
    return '\n'.join(res)+'\n'

def dot_quote(s):return '"'+s.replace('\\','\\\\').replace('"','\\"')+'"'

def dot_graph(stem,rows):
    nodes=defaultdict(list)
    for el in rows:
        for pi,name in enumerate(el['pins']):nodes[name].append((el['designator'],pi+1))
    lines=['graph VOID_SOURCE {','  graph [overlap=false,splines=true,rankdir=LR,fontsize=18,labelloc=t,label='+dot_quote(stem+' — literal electrical connection graph')+'];','  node [fontname="Arial",fontsize=9];']
    for r in rows:
        key='comp_'+str(r['line']);lines.append('  '+dot_quote(key)+' [shape=box,style=rounded,label='+dot_quote(r['designator']+'\\n'+r['value_or_model'][:60])+'];')
        for pin,name in enumerate(r['pins'],1):
            nk='net_'+r['group']+'_'+name
            lines.append('  '+dot_quote(key)+' -- '+dot_quote(nk)+' [label='+dot_quote(str(pin))+',fontsize=8];')
    for (group,name) in {(r['group'],x) for r in rows for x in r['pins']}:
        lines.append('  '+dot_quote('net_'+group+'_'+name)+' [shape=ellipse,style=filled,fillcolor="#e5f5fc",label='+dot_quote(name)+'];')
    lines+=['}']
    return '\n'.join(lines)+'\n'

allrows=[];manifest=[];subnames={}
for p in sorted(SRC.iterdir()):
    if p.suffix.lower() not in ('.cir','.lib'):continue
    t,els,subs,inc=read_spice(p)
    for sub in subs:
        if sub['name'] in subnames:raise ValueError('Duplicated subckt '+sub['name'])
        subnames[sub['name']]=sub
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    pages=(len(els)+19)//20
    for i in range(pages):
        page=els[i*20:(i+1)*20]
        (OUT/f'{p.stem}_sheet_{i+1:02}.svg').write_text(schematic_svg(p.stem,t,page,i+1,pages,sha))
    dot=dot_graph(p.stem,els)
    (OUT/f'{p.stem}_FULL_CONNECTION_GRAPH.dot').write_text(dot)
    subprocess.run(['dot','-Tsvg','-o',str(OUT/f'{p.stem}_FULL_CONNECTION_GRAPH.svg'),str(OUT/f'{p.stem}_FULL_CONNECTION_GRAPH.dot')],check=True,timeout=35)
    manifest.append({'source':p.name,'sha256':sha,'element_count':len(els),'include_files':inc,'subcircuits':subs,'sheets':pages,'types':dict((k,sum(q['kind']==k for q in els)) for k in sorted(SUPPORTED))})
    allrows.extend(els)
# Cross-check references and X instance pin arities for the full R08 active source set.
for m in manifest:
    for inc in m['include_files']:
        if not (SRC/inc).is_file():raise ValueError('Missing included library: '+inc)
for r in allrows:
    if r['kind']=='X':
        name=r['value_or_model'].split()[0]
        if name not in subnames:raise ValueError('Undefined subckt '+name+' at '+r['file']+':'+str(r['line']))
        if len(subnames[name]['pins'])!=len(r['pins']):raise ValueError('Pin count mismatch '+name+' at '+r['file']+':'+str(r['line']))
with (OUT/'R08_ALL_SPICE_ELEMENTS.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['file','line','group','designator','kind','pins','value_or_model','source_text']);w.writeheader()
    for r in allrows:w.writerow({**r,'pins':' '.join(r['pins'])})
(OUT/'RENDER_SOURCE_MANIFEST.json').write_text(json.dumps({'schema':'VOID_R08_SOURCE_RENDER_V1','files':manifest,'validated_elements':len(allrows),'X_subckt_ports':'VERIFIED','source_path_immutable':str(SRC)},indent=2)+'\n')
(OUT/'README.md').write_text(f'''# SPICE netlist sourced electrical connectivity views

Generated from the nine actual R08 `.cir` and `.lib` sources, without visual inference.
There are {len(allrows)} electrical element statements, every one represented by an
editable SVG sheet row, a graph-node occurrence and a line-addressed CSV record.
The first line of each SPICE deck is its title, not a voltage source.

`*_sheet_XX.svg`: human-readable net-labelled component symbols, full literal pin
names and line numbers, based on actual netlist connectivity. Nets connect where
their labels match within the same SPICE scope; cross-sheet connections retain names.
`*_FULL_CONNECTION_GRAPH.svg` and matching `.dot`: full literal electrical
bipartite graphs, automatically laid out by Graphviz. These are topology drawings,
not PCB layouts and not illustrations generated by an image model.
`R08_ALL_SPICE_ELEMENTS.csv`: original element text, source line and terminal order.
`RENDER_SOURCE_MANIFEST.json`: source hash, component counts, full module port check.

Full EDA verification requires native KiCad capture/ERC; SVG is an editable vector
render of actual source-linked electrical connections, not an invented KiCad board.
All passive component values and raw SPICE sources remain in `../01_R08_ACTIVE_SPICE/`.
Run: `python3 ../../06_ENGINEERING_VALIDATORS/render_spice_source.py` with Graphviz installed.
''')
print('SOURCE_RENDER_PASS',len(manifest),'netlist files',len(allrows),'elements',sum(x['sheets'] for x in manifest),'component sheets')
