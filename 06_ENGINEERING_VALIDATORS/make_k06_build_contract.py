#!/usr/bin/env python3
"""Generate actual-net-based prototype connector and grouped assembly contracts.
Every connector net must occur in the expanded K06 source. This is proposed
board partition wiring, not an already routed/manufactured PCB.
"""
from collections import Counter, defaultdict
import csv, json, hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
B=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY'
S=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
parts=list(csv.DictReader((B/'K06_HIERARCHICAL_EXPANDED_BOM.csv').open(newline='')))
nodetable=list(csv.DictReader((B/'K06_NODE_AND_TEST_POINT_PORTS.csv').open(newline='')))
lookup={x['net']:x for x in nodetable}
assert len(parts)==175 and len(lookup)==74
partrefs={p['instance_path']:p for p in parts}
assert len(partrefs)==len(parts)
contacts=('11','12','13','14','21','22','23','24')
for i in contacts:
    touch=partrefs['X_MATERIAL/R_ACT_'+i]
    guard=partrefs['X_MATERIAL/R_ACT_GUARD_'+i]
    assert touch['physical_nets']==f'UI_1V8;X_MATERIAL/PAD_{i}'
    assert guard['physical_nets']==f'X_MATERIAL/PAD_{i};X_MATERIAL/F_{i}'
    assert touch['assembly_role']=='8_nominal_contact_devices_measure_actual_resistance_or_use_FSR'
    assert guard['assembly_role']=='fixed_1k_series_contact_protection_resistor'
connectors={
    'PWR_01':('P1_POWER','power','SUPPLY','0','UI_SRC','0','DISPLAY_3V3','0'),
    'CORE_TEST_01':('K06_CORE','high_impedance_measure','SHUNT_TOP','0','JCT','0','PROBE_A','0','PROBE_B','0','CHARGE_A','0','CHARGE_B','0','CHARGE_C','0'),
    'IO_STIM_01':('P3_CONTROL','protected_low_voltage_stimulus','WRITE_A','0','WRITE_B','0','BOUNDARY_A','0','BOUNDARY_B','0'),
    'OBS_01':('P2_ACQUISITION','high_impedance_measure','FIELD_A','0','FIELD_B','0','AXIS_A','0','AXIS_B','0','DISPLAY_X','0','DISPLAY_Y','0','DISPLAY_Z','0'),
    'K05_BIAS_01':('K05_WEIGHTED','external_bipolar_bias','xp1','0','xm1','0','xp2','0','xm2','0','xp3','0','y0','0','y1','0'),
}
for i in contacts:
    connectors[f'MAT_{i}']=('P4_CONTACT_CARRIER','swappable_material_contact','UI_1V8',f'X_MATERIAL/PAD_{i}')
connectors['AXIS_POT_A']=('P4_CONTACT_CARRIER','actual_10k_track_wiper','UI_1V8','0','AXIS_A')
connectors['AXIS_POT_B']=('P4_CONTACT_CARRIER','actual_10k_track_wiper','UI_1V8','0','AXIS_B')
rows=[]
for ref,entry in connectors.items():
    board,role,*nets=entry
    for pin,net in enumerate(nets,1):
        if net not in lookup:raise ValueError(f'connector {ref} pin {pin} ungrounded in source: {net}')
        rows.append({'connector':ref,'proposed_owner_board':board,'pin':pin,'source_net':net,
                     'signal_class':role,'source_element_pin_count':lookup[net]['member_count'],
                     'physical_footprint':'UNASSIGNED_NOT_FABRICATION_READY',
                     'source_path':'K06_R08_flattened_175_primitives'})
with (B/'K06_PROTOTYPE_CONNECTOR_PINOUT.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Procurement counts are groups, not price/availability claims. Each K06 primitive
# enters exactly one group, including its source load models and virtual V cards.
def route(p):
    role=p['assembly_role']
    if role=='power_or_input_source_in_spice_only':return 'EXTERNAL_SUPPLY_OR_BIAS_NO_PART'
    if role in ('instrument_equivalent_no_second_parallel_load','instrument_probe_model_replace_with_measured_probe'):
        return 'ONE_INSTRUMENT_LOAD_OR_SOURCE_EQUIVALENT_NOT_BOTH'
    if role=='8_nominal_contact_devices_measure_actual_resistance_or_use_FSR':return 'SWAPPABLE_MATERIAL_CONTACT_8'
    if role=='axis_potentiometer_equivalent_two_5k_halves_measure_physical_wiper':return 'ONE_10K_POT_TRACK_FOR_EACH_AXIS'
    if role=='piezo_ceramic_nominal_15n_load_model_not_measured_acoustic_result':return 'PIEZO_CERAMIC_OR_ELECTRICAL_15N_TEST_LOAD'
    if p['name'].startswith(('R_ACT_GUARD_','R_NODE_RET_','R_SHEET_')):return 'P4_CONTACT_CARRIER_PASSIVE'
    if p['name'].startswith('R_CURRENT_LIMIT') or p['name'] in ('R_KELVIN','R_UI_CURRENT'):return 'P1_POWER_MONITOR'
    if p['name'].startswith(('D_LED_','Q_LIGHT_','R_LED_','R_BIAS_','R_PULL_','R_SENSE_')):return 'CORE_LED_OUTPUT'
    if p['name'].startswith(('D_WRITE_','R_WRITE_','C_WRITE_','D_BOUNDARY_','R_BOUNDARY_')):return 'CORE_PROTECTED_STIMULUS'
    return 'CORE_PASSIVE_AND_JUNCTION'
all_parts=defaultdict(list)
for p in parts:
    group=route(p)
    # Two 5k halves per axis are a single 10k physical potentiometer only if
    # mounted and wired as a true track, never count as 4 pot parts.
    if group=='ONE_10K_POT_TRACK_FOR_EACH_AXIS':key=(group,'potentiometer_10k_track',p['type'])
    else:key=(group,p['value'],p['type'])
    all_parts[key].append(p['instance_path'])
with (B/'K06_GROUPED_ASSEMBLY_AND_LOAD_POLICY.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['module','nominal_spice_value','source_device_type','source_primitive_count','original_instance_paths','assembly_rule'])
    for (group,value,kind),refs in sorted(all_parts.items()):
        rule=('DO_NOT_ORDER_V_SOURCE_CARD' if group=='EXTERNAL_SUPPLY_OR_BIAS_NO_PART' else
              'ONE_PHYSICAL_POT_PER_AXIS_NOT_FOUR_FIXED_5K_RESISTORS' if group=='ONE_10K_POT_TRACK_FOR_EACH_AXIS' else
              'DO_NOT_DOUBLE_LOAD_MEASUREMENT_PORT' if group=='ONE_INSTRUMENT_LOAD_OR_SOURCE_EQUIVALENT_NOT_BOTH' else
              'SOURCE_VALUE_NOMINAL_VERIFY_COMPONENT_AND_PINOUT')
        w.writerow([group,value,kind,len(refs),';'.join(refs),rule])
assert sum(len(x) for x in all_parts.values())==175
report={'schema':'VOID_R08_K06_CONNECTOR_AND_ASSEMBLY_V1','active_source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),
        'primitive_count':len(parts),'distinct_net_count':len(lookup),
        'proposed_connector_count':len(connectors),'proposed_connector_pins':len(rows),
        'source_contact_count':len(contacts),'fixed_material_series_resistor_count':len(contacts),
        'axis_potentiometer_source_resistor_halves':4,
        'grouped_source_roles':dict(sorted(Counter(route(p) for p in parts).items())),
        'statement':'Physical connectors and board assignment derived from source nets; footprints, ratings, datasheets, actual power/bench measurements and fabrication not claimed'}
(B/'K06_BUILD_CONTRACT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'PASS':'K06 net-backed prototype interface','connectors':len(connectors),'pins':len(rows),'primitives':len(parts)}))
