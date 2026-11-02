#!/usr/bin/env python3
"""Physical-source and physical-acquisition PRE-FLIGHT (not a fabricated bench test).
Compile actual native ingestion code, source-recapture and strict negative tests.
No synthesized positive telemetry, hardware impostors or simulator benchmarks.
"""
from pathlib import Path
import csv,json,subprocess,tempfile,hashlib,sys,re
R=Path(__file__).resolve().parents[1]
H=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY'
S=R/'01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS'
P=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
D=R/'07_FRESH_TEST_EVIDENCE/PHYSICAL_PREFLIGHT_20261102';D.mkdir(parents=True,exist_ok=True)
results=[]
def gate(name,ok,context):
    results.append({'name':name,'pass':bool(ok),'details':context})
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)
    if not ok:raise RuntimeError(name+' '+str(context))
def run(args,expected=0):
    r=subprocess.run([str(x) for x in args],capture_output=True,text=True,timeout=90)
    return r,(r.returncode==expected if expected>=0 else r.returncode!=0)
try:
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/generate_editable_spice_schematics.py'])
    gate('recapture_original_nine_spice_sources',ok and '"elements": 216' in r.stdout,{'stdout':r.stdout,'stderr':r.stderr,'exit':r.returncode})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/expand_r08_k06_hardware.py'])
    gate('flatten_K06_175_real_source_primitives',ok and '"flat_primitive_count": 175' in r.stdout,{'stdout':r.stdout,'stderr':r.stderr,'exit':r.returncode})
    report=json.loads((S/'CAPTURE_VALIDATION.json').read_text())
    members=list(csv.DictReader((S/'COMPONENT_PORT_MAP.csv').open()))
    bom=list(csv.DictReader((H/'K06_HIERARCHICAL_EXPANDED_BOM.csv').open()))
    gate('spice_216_elements_459_pin_labels',len(report['decks'])==9 and report['element_count']==216 and len(members)==459,{'mapped':len(members)})
    gate('k06_175_expanded_devices',len(bom)==175,{'parts':len(bom)})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/verify_material_contact_carrier.py'])
    gate('source_exact_2x4_contacts_and_series_resistors',ok and 'MATERIAL_CARRIER_SOURCE_PASS' in r.stdout,{'stdout':r.stdout,'stderr':r.stderr})
    carrier=json.loads((H/'03_BUILD_REFERENCE/MATERIAL_CONTACT_INDEPENDENT_SOURCE_VERIFICATION.json').read_text())
    gate('no_false_ground_guard_and_real_sheet_connectivity',
         carrier['status']=='PASS' and carrier['contact_count']==8 and
         carrier['fixed_1k_series_resistor_count']==8 and
         carrier['sheet_horizontal_links']==6 and carrier['sheet_vertical_links']==4 and
         carrier['no_grounded_1k_perimeter_guard'] is True,
         {key:carrier[key] for key in ('contact_count','fixed_1k_series_resistor_count','sheet_horizontal_links','sheet_vertical_links')})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/render_material_carrier_circuit_sheets.py'])
    gate('render_actual_source_material_sheets',ok and 'MATERIAL_CARRIER_VECTOR_PASS' in r.stdout,{'stdout':r.stdout,'stderr':r.stderr})
    import xml.etree.ElementTree as ET
    vector=json.loads((H/'03_BUILD_REFERENCE/MATERIAL_CARRIER_VECTOR_CAPTURE.json').read_text())
    pages=[ET.parse(H/'03_BUILD_REFERENCE'/name).getroot() for name in vector['svg_files']]
    svgtext=[' '.join((e.text or '') for e in page.iter()) for page in pages]
    expected_a=[f'R_ACT_{n}' for n in ('11','12','13','14','21','22','23','24')]+[f'R_ACT_GUARD_{n}' for n in ('11','12','13','14','21','22','23','24')]+[f'R_SHEET_H_{r}{c}' for r in (1,2) for c in (1,2,3)]+[f'R_SHEET_V_1{c}' for c in (1,2,3,4)]
    expected_b=[f'R_NODE_RET_{n}' for n in ('11','12','13','14','21','22','23','24')]
    gate('rendered_source_refs_26_plus_8',len(expected_a)==26 and len(expected_b)==8 and vector['source_cards_shown']==34 and
         all('R_ACT_'+n in svgtext[0] for n in ('11','12','13','14','21','22','23','24')) and
         all(e in svgtext[0] for e in expected_a) and all(e in svgtext[1] for e in expected_b),
         {'page_A':len(expected_a),'page_B':len(expected_b),'source_sha256':vector['sha256']})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/verify_editable_capture_independent.py'])
    independent=json.loads((H/'KICAD_INDEPENDENT_CONNECTIVITY_VALIDATION.json').read_text())
    gate('independent_kicad_ast_pin_net_check_459',ok and independent['status']=='PASS' and independent['total_pin_net_connections']==459,{'stderr':r.stderr,'result':independent['status']})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/make_k06_build_contract.py'])
    board=json.loads((H/'K06_BUILD_CONTRACT_VALIDATION.json').read_text())
    gate('k06_source_backed_board_connector_and_bom_contract',ok and board['primitive_count']==175 and board['proposed_connector_pins']==78 and board['source_contact_count']==8 and board['fixed_material_series_resistor_count']==8,{'connectors':board['proposed_connector_count'],'pins':board['proposed_connector_pins'],'stdout':r.stdout})
    # Four actual source-net connector sheets, separately verified from schematic AST.
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/build_verified_board_interconnect.py'])
    gate('generate_four_source_exact_external_interconnect_schematics',ok and 'MODULE_SHEETS_PASS' in r.stdout,
         {'stdout':r.stdout,'stderr':r.stderr})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/verify_board_interconnect_independent.py'])
    inter=json.loads((H/'04_VERIFIED_BOARD_INTERCONNECT/INDEPENDENT_PIN_NET_VALIDATION.json').read_text())
    gate('independent_board_pin_net_connections_and_corruption_refusal',ok and inter['status']=='PASS'
         and inter['connected_pins']==78 and inter['connectors']==15 and inter['negative_corruption_tests_passed']==3,
         {'stdout':r.stdout,'stderr':r.stderr,'result':inter['status']})
    r,ok=run([sys.executable,R/'06_ENGINEERING_VALIDATORS/build_probe_loading_budget.py'])
    budget=json.loads((H/'04_VERIFIED_BOARD_INTERCONNECT/K06_PROBE_LOADING_CALCULATIONS.json').read_text())
    gate('source_accurate_charge_probe_loading_and_power_budget',ok and budget['status']=='PASS'
         and budget['verified_source_cards']==32 and budget['local_scenarios']==9
         and abs(budget['R_CURRENT_LIMIT_worst_case_W_at_24V']-24*24/3300)<1e-12,
         {'stdout':r.stdout,'stderr':r.stderr,'source_cards':budget['verified_source_cards']})
    for rec in report['decks']:
        name=rec['deck'];orig=P/name;schem=S/rec['schematic'];ss=schem.read_text()
        md=hashlib.sha256(orig.read_bytes()).hexdigest()
        expected=[row for row in members if row['source']==name]
        found=sum(bool(re.search(r'\(property "SPICE_source_tokens"',line)) for line in ss.splitlines())
        pins=sum(1 for line in ss.splitlines() if re.search(r'\(global_label ',line))
        gate('exact_source_capture_'+name,md==rec['sha256'] and found==rec['element_count'] and pins==len(expected) and '(generator "void_source_capture")' in ss,{'source_hash':md,'devices':found,'pins':pins})
    r,ok=run(['make','-B','-C',H/'native_bench_ingestion'])
    gate('compile_real_native_bench_ingestion',ok,{'stdout':r.stdout,'stderr':r.stderr})
    exe=H/'native_bench_ingestion/void_bench_ingest'
    hdr='sample_index,time_ns,instrument_serial,calibration_id,charge_a_v,charge_b_v,charge_c_v,probe_a_v,probe_b_v,write_a_v,write_b_v\n'
    bads={
        'header_only':hdr,
        'nonfinite':hdr+'0,100,SERIAL_1,CAL_1,nan,0,0,0,0,0,0\n',
        'duplicate_timestamp':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,0,0,0,0\n1,100,SERIAL_1,CAL_1,0,0,0,0,0,0,0\n',
        'overvoltage_write':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,0,0,3.3,0\n1,200,SERIAL_1,CAL_1,0,0,0,0,0,3.3,0\n',
        'changed_calibration':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,0,0,0,0\n1,200,SERIAL_1,CAL_2,0,0,0,0,0,0,0\n',
        'index_gap':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,0,0,0,0\n2,200,SERIAL_1,CAL_1,0,0,0,0,0,0,0\n',
        'empty_field':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,0,0,0,\n',
        'out_of_bounds_probe':hdr+'0,100,SERIAL_1,CAL_1,0,0,0,100,0,0,0\n1,200,SERIAL_1,CAL_1,0,0,0,100,0,0,0\n',
    }
    with tempfile.TemporaryDirectory(prefix='void_physical_reject_') as t:
        t=Path(t)
        for key,payload in bads.items():
            f=t/(key+'.csv');f.write_text(payload)
            r,ok=run([exe,f,t/(key+'.txt')],expected=-1)
            gate('fail_closed_'+key,ok and 'REFUSE' in r.stderr,{'returncode':r.returncode,'diagnostic':r.stderr.strip()[:140]})
        r,ok=run([exe,t/'missing_real_instrument_session.csv',t/'missing.txt'],expected=-1)
        gate('fail_closed_missing_instrument_data',ok and 'REFUSE' in r.stderr,{'returncode':r.returncode})
    # Exact original ZIP fragments, not assumptions that absent 04/06 inputs vanished.
    m=json.loads((R/'91_EXACT_UPLOADED_INPUTS/ORIGINAL_INPUTS_RECONSTRUCTION_MANIFEST.json').read_text())
    failures=[];counts=0
    for item in m['files']:
        h=hashlib.sha256();length=0
        for fragment in item['fragments']:
            path=R/'91_EXACT_UPLOADED_INPUTS'/fragment['path']
            if not path.is_file():failures.append(('missing',str(path)));continue
            blob=path.read_bytes();counts+=1;length+=len(blob);h.update(blob)
            if len(blob)!=fragment['size'] or hashlib.sha256(blob).hexdigest()!=fragment['sha256']:
                failures.append(('bad_fragment',str(path)))
        if length!=item['size'] or h.hexdigest()!=item['sha256']:failures.append(('bad_whole',item['original_name']))
    gate('exact_eight_uploaded_originals_reconstruct_bytewise',not failures and len(m['files'])==8,{'archive_count':len(m['files']),'fragment_count':counts,'failures':failures})
except Exception as exc:
    print('PHYSICAL_PREFLIGHT_FAILURE',repr(exc),file=sys.stderr)
    results.append({'name':'preflight_exception','pass':False,'details':repr(exc)})
finally:
    summary={'schema':'VOID_PHYSICAL_PREFLIGHT_V1','passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results),'checks':results,
             'status':'SOURCE_AND_SOFTWARE_QUALITY_ONLY_NO_PHYSICAL_BENCH_SESSION'}
    (D/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('PHYSICAL_PREFLIGHT_RESULT',summary['passed'],'passed',summary['failed'],'failed')
    if summary['failed']:sys.exit(1)
