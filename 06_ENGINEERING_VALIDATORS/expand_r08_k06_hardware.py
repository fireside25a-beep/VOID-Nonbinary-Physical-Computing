#!/usr/bin/env python3
"""Flatten real K06 SPICE elements and produce assembly inventory and pin/wiring provenance.
Subcircuit terminal mappings retain all external and internal electrical nodes.
No external vendor assignments or physical results are inferred.
"""
import csv,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
OUT=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY'
sub={};top=[];first=True
for source in sorted(P.iterdir()):
    lines=source.read_text().splitlines();scope=None;first=True
    for line_no,raw in enumerate(lines,1):
        line=raw.strip()
        if not line or line.startswith(('*',';')):continue
        toks=line.split();cmd=toks[0].upper()
        if first:
            first=False
            if cmd[0]!='.':continue
        if cmd=='.SUBCKT':
            scope=cmd if scope is None else None
            assert scope is not None
            sub[toks[1].upper()]={'ports':toks[2:],'records':[],'source':source.name}
            current=toks[1].upper();continue
        if cmd=='.ENDS':scope=None;continue
        if cmd.startswith('.'):continue
        typ=cmd[0]
        n=(len(toks)-2 if typ=='X' else 3 if typ=='Q' else 2)
        assert typ in 'RCLVDQXI' and len(toks)>=n+2
        rec={'name':toks[0],'type':typ,'nodes':toks[1:1+n],
             'value':' '.join(toks[1+n:]),'source_file':source.name,'source_line':line_no}
        if scope:sub[current]['records'].append(rec)
        elif source.name=='VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir':top.append(rec)

def expand(records,prefix='',mapping=None):
    mapping=mapping or {}
    for item in records:
        rec=item.copy();rec['instance_path']=prefix+rec['name']
        rec['physical_nets']=[mapping.get(x,x if x=='0' or not prefix else prefix+x) for x in rec['nodes']]
        if rec['type']=='X':
            name=rec['value'].upper()
            if name not in sub:raise ValueError('undefined subcircuit '+name)
            ports=sub[name]['ports']
            assert len(ports)==len(rec['physical_nets'])
            scoped={p:net for p,net in zip(ports,rec['physical_nets'])}
            scoped['0']='0'
            yield from expand(sub[name]['records'],rec['instance_path']+'/',scoped)
        else:yield rec

hard=list(expand(top))
# There are 3 top-level X instances; K06 primitives = 106-3 + 12+12+48 = 175.
assert len(hard)==175,(len(hard),Counter(x['type'] for x in hard))
# Voltage cards and meter-equivalent loads are NOT procurement resistors.
def role(rec):
    name=rec['name']
    if rec['type'] in ('V','I'):return 'power_or_input_source_in_spice_only'
    if name.startswith(('R_METER','R_MEM_METER','R_DMM','R_XY_INSTR')):return 'instrument_equivalent_no_second_parallel_load'
    if name in ('R_PA','R_PB','C_PA','C_PB'):return 'instrument_probe_model_replace_with_measured_probe'
    if name.startswith('R_ACT_GUARD_'):return 'fixed_1k_series_contact_protection_resistor'
    if name.startswith('R_ACT_'):return '8_nominal_contact_devices_measure_actual_resistance_or_use_FSR'
    if name.startswith(('R_AXIS_A_','R_AXIS_B_')):return 'axis_potentiometer_equivalent_two_5k_halves_measure_physical_wiper'
    if name.startswith('C_MECH_PIEZO_'):return 'piezo_ceramic_nominal_15n_load_model_not_measured_acoustic_result'
    if rec['type']=='D' and name.startswith('D_LED_'):return 'emitter_LED_part_selection_required'
    if rec['type']=='Q':return 'real_NPN_part_model_nominal'
    if rec['type']=='D':return 'real_diode_part_model_nominal'
    return 'physical_component'
for rec in hard:rec['assembly_role']=role(rec)
OUT.mkdir(exist_ok=True)
cols=['instance_path','name','type','value','assembly_role','physical_nets','source_file','source_line']
with (OUT/'K06_HIERARCHICAL_EXPANDED_BOM.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(cols)
    for r in hard:w.writerow([r[k] if k!='physical_nets' else ';'.join(r[k]) for k in cols])
portnames=['SUPPLY','SHUNT_TOP','JCT','INPUT','PROBE_A','PROBE_B','CHARGE_A','CHARGE_B','CHARGE_C','WRITE_A','WRITE_B','BOUNDARY_A','BOUNDARY_B','UI_1V8','UI_SRC','DISPLAY_3V3','FIELD_A','FIELD_B','AXIS_A','AXIS_B','DISPLAY_X','DISPLAY_Y','DISPLAY_Z','0']
connections=defaultdict(list)
for r in hard:
    for i,node in enumerate(r['physical_nets'],1):connections[node].append(f'{r["instance_path"]}:pin{i}')
with (OUT/'K06_NODE_AND_TEST_POINT_PORTS.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['net','member_count','primitive_pin_references','proposed_connector_role'])
    for net in sorted(connections):
        role='external_measurement_or_IO_review' if net in portnames else 'internal_node'
        w.writerow([net,len(connections[net]),';'.join(connections[net]),role])
report={'source':'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir','source_sha256':hashlib.sha256((P/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir').read_bytes()).hexdigest(),
'flat_primitive_count':len(hard),'primitive_by_type':dict(Counter(x['type'] for x in hard)),
'role_counts':dict(Counter(x['assembly_role'] for x in hard)),'distinct_electrical_nets':len(connections),
'guarded_critical_nets':{n:len(connections.get(n,[])) for n in portnames},
'interpretation':'flattened connectivity, NOT a tested PCB, Gerber, human meter or full nonlinear SPICE operating point'}
(OUT/'K06_EXPANSION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','flat_primitive_count':len(hard),'nodes':len(connections),'primitive_by_type':report['primitive_by_type']}))
