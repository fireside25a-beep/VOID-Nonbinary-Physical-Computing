#!/usr/bin/env python3
"""Independent source/BOM electrical invariant checker for the VOID 2x4 contact carrier.

No generated SPICE, synthetic instrument samples, parts substitutions, or test stubs.
Reads authoritative material source and separately generated flattened K06 inventory.
Writes exact source-backed wiring and placement-role CSVs for a low-cost carrier.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import csv, hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE/VOID_PRIMITIVE_MATERIAL_INTERFACE.lib'
EXPANDED=ROOT/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY/K06_HIERARCHICAL_EXPANDED_BOM.csv'
OUT=ROOT/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY/03_BUILD_REFERENCE'
PADS=[f'{r}{c}' for r in (1,2) for c in (1,2,3,4)]


def ref_source():
    result={}
    for lineno,line in enumerate(SOURCE.read_text().splitlines(),1):
        item=line.strip().split()
        if not item or not item[0].startswith('R_'):continue
        if len(item)!=4:raise ValueError(f'invalid source resistor declaration line {lineno}')
        name,a,b,value=item
        if name in result:raise ValueError('duplicate resistor '+name)
        result[name]=(a,b,value,lineno)
    return result


def main():
    source=ref_source()
    flat=list(csv.DictReader(EXPANDED.open(newline='')))
    by_name={r['name']:r for r in flat}
    if len(by_name)!=len(flat):raise ValueError('non-unique flattened primitive names')
    if len(flat)!=175:raise ValueError(f'expected 175 flattened primitive devices; got {len(flat)}')
    if len(PADS)!=8 or len(set(PADS))!=8:raise ValueError('invalid grid definition')
    carrier=[];wire=[];roles=Counter()
    for pad in PADS:
        ref_act='R_ACT_'+pad; ref_guard='R_ACT_GUARD_'+pad
        exact=[(ref_act,'VREF','PAD_'+pad,'10meg','8_nominal_contact_devices_measure_actual_resistance_or_use_FSR'),
               (ref_guard,'PAD_'+pad,'F_'+pad,'1k','fixed_1k_series_contact_protection_resistor'),
               ('R_NODE_RET_'+pad,'F_'+pad,'RET','220k','physical_component')]
        for name,a,b,value,role in exact:
            if name not in source:raise ValueError('missing source '+name)
            if source[name][:3]!=(a,b,value):raise ValueError(f'wrong source topology/value {name} {source[name][:3]}')
            if name not in by_name:raise ValueError('missing flatten '+name)
            r=by_name[name]
            if (r['value'],r['assembly_role'],r['source_line'],r['source_file'])!=(value,role,str(source[name][3]),SOURCE.name):
                raise ValueError(f'flatten role/value/line mismatch {name}')
            nets=r['physical_nets'].split(';')
            wanted=[('UI_1V8' if a=='VREF' else '0' if a=='RET' else 'X_MATERIAL/'+a),
                    ('UI_1V8' if b=='VREF' else '0' if b=='RET' else 'X_MATERIAL/'+b)]
            if nets!=wanted:raise ValueError(f'flatten pin mapping mismatch {name}: {nets} vs {wanted}')
            if name.startswith('R_ACT_GUARD_') and '0' in nets:raise ValueError('grounded series resistor '+name)
            roles[role]+=1
            wire.append([name,value,a,b,netsto_str(nets),'X_MATERIAL',SOURCE.name,source[name][3],role])
        carrier.append([pad,'PAD_'+pad,'F_'+pad,ref_act,'10meg',ref_guard,'1k','R_NODE_RET_'+pad,'220k','separate swappable contact and fixed series resistor'])
    # The complete two-row, four-column sheet geometry is a direct source constraint.
    edges=[]
    for row in (1,2):
        for col in (1,2,3):edges.append(('H',f'{row}{col}',f'{row}{col+1}'))
    for col in (1,2,3,4):edges.append(('V',f'1{col}',f'2{col}'))
    for axis,a,b in edges:
        name=f'R_SHEET_{axis}_{a}'
        if name not in source or source[name][:3]!=(f'F_{a}',f'F_{b}','22k'):
            raise ValueError('source sheet topological inconsistency '+name)
        r=by_name.get(name)
        if r is None or r['value']!='22k' or r['physical_nets'].split(';')!=['X_MATERIAL/F_'+a,'X_MATERIAL/F_'+b]:
            raise ValueError('flatten sheet mismatch '+name)
        wire.append([name,'22k','F_'+a,'F_'+b,r['physical_nets'],'X_MATERIAL',SOURCE.name,source[name][3],'sheet_spatial_coupling'])
    actual_sheet={n for n in source if n.startswith(('R_SHEET_H_','R_SHEET_V_'))}
    if actual_sheet!={f'R_SHEET_{axis}_{left}' for axis,left,right in edges}:
        # The name construction above uses the contact at the left/top of each edge.
        raise ValueError('unexpected sheet link count or orientation')
    if roles['fixed_1k_series_contact_protection_resistor']!=8 or roles['8_nominal_contact_devices_measure_actual_resistance_or_use_FSR']!=8:
        raise ValueError('contact/series count mismatch')
    # Reject a fictitious grounded guarding ring, or any claim that the two roles are one part.
    OUT.mkdir(exist_ok=True)
    with (OUT/'MATERIAL_CONTACT_PLACEMENT_AND_ROLES.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['grid_position','external_pad','internal_sheet_node','replaceable_contact_ref','nominal_released_value','fixed_series_ref','series_ohms','node_to_return_ref','return_ohms','installation_rule']);w.writerows(carrier)
    with (OUT/'MATERIAL_CONTACT_NET_CONNECTIONS.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['reference','value','source_node_1','source_node_2','flattened_K06_nets','subcircuit','source_file','source_line','electrical_role']);w.writerows(wire)
    report={
      'status':'PASS','source_file':SOURCE.name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
      'k06_flat_bom_sha256':hashlib.sha256(EXPANDED.read_bytes()).hexdigest(),
      'grid':'2x4','contact_count':8,'fixed_1k_series_resistor_count':8,'sheet_horizontal_links':6,
      'sheet_vertical_links':4,'sheet_link_ohms':'22k','node_to_return_resistors':8,
      'physical_wiring_references':len(wire),
      'no_grounded_1k_perimeter_guard':True,
      'conditions':['contact resistance is nominal 10meg in source, measure actual parts',
        '1k series resistors connect PAD_xy to F_xy and never directly to ground',
        'external power and metering loads are not extra material-carrier components',
        'physical continuity and source orientation require independent bench validation']}
    (OUT/'MATERIAL_CONTACT_INDEPENDENT_SOURCE_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('MATERIAL_CARRIER_SOURCE_PASS',json.dumps({k:report[k] for k in ('contact_count','fixed_1k_series_resistor_count','sheet_horizontal_links','sheet_vertical_links','physical_wiring_references')}))

def netsto_str(nodes):return ';'.join(nodes)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:
        print('MATERIAL_CARRIER_SOURCE_REFUSED:',str(e),file=sys.stderr)
        sys.exit(1)
