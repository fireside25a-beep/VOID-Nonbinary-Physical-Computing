#!/usr/bin/env python3
"""Canonical, executable source-and-native acceptance for VOID/HX89.
All modes invoke real native HX89 and native AC/DC, BVH and CPU sources.
No substitute binary, synthetic hardware input, or physical measurement claim.
"""
import csv, hashlib, json, math, os, subprocess, sys, tempfile, shutil, time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
U=R/'05_HX89_K06_BRIDGE/03_UNIFIED_NATIVE_CLOSED_LOOP'
P=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
H=R/'05_HX89_K06_BRIDGE/01_ORIGINAL_BRIDGE_BOUNDED_RC_COSIM/03_HX89_BINARY_ONLY/hx89'
D=R/'07_FRESH_TEST_EVIDENCE/UNIFIED_CANONICAL_ACCEPTANCE_20261102'
D.mkdir(parents=True,exist_ok=True)
results=[]
MODES=['integrated','integrated-control','integrated-no-cpu','integrated-no-acdc','integrated-no-entropy','legacy']
CASES=['closed_loop','closed_loop_repeat','open_write_a','no_excitation','forced_a','inverted_action','open_write_b']
def record(name,condition,details):
    results.append({'name':name,'pass':bool(condition),'details':details})
    print(('PASS ' if condition else 'FAIL ')+name,flush=True)
    if not condition:raise AssertionError(name+' : '+str(details))
def run(name,command,cwd=None,negative=False,contains=None,timeout=180):
    p=subprocess.run([str(x) for x in command],cwd=cwd,text=True,capture_output=True,errors='replace',timeout=timeout)
    (D/(name+'.stdout.log')).write_text(p.stdout)
    (D/(name+'.stderr.log')).write_text(p.stderr)
    ok=(p.returncode!=0 if negative else p.returncode==0) and (contains is None or contains in (p.stdout+p.stderr))
    record(name,ok,{'exit_code':p.returncode,'needle':contains,'expected_failure':negative,'argv':[str(x) for x in command]})
    return p
def rows(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))
def hashfile(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
try:
    record('original_hx89_binary_sha256',hashfile(H)=='50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451',hashfile(H))
    run('build_canonical_unified_native',['make','-B','all'],cwd=U,timeout=240)
    run('contract_native_driver_compile',['make','build/native_driver_contract'],cwd=U)
    run('contract_native_driver',[U/'build/native_driver_contract',H])
    run('contract_cpu_state_compile',['make','build/native_cpu_state_contract'],cwd=U)
    run('contract_cpu_state',[U/'build/native_cpu_state_contract'])
    run('source_structure_all_R08_circuits',[sys.executable,R/'06_ENGINEERING_VALIDATORS/validate_r08_source.py'])
    exe=U/'build/void_unified'
    for mode in MODES:
        folder=D/mode;folder.mkdir(exist_ok=True)
        run('native_run_'+mode,[exe,P,H,folder,mode],contains='NATIVE_PASS_'+mode+' closed_loop',timeout=240)
        summaries=rows(folder/'native_summary.csv')
        record('native_scenarios_'+mode,len(summaries)==7 and all(int(x['steps'])==96 and x['mode']==mode for x in summaries),{'scenarios':len(summaries),'decisions':sum(int(x['steps']) for x in summaries)})
        for case in CASES:
            nr=rows(folder/(case+'_native.csv'))
            tr=rows(folder/(case+'_trajectory.csv'))
            record('row_counts_'+mode+'_'+case,len(nr)==96 and len(tr)==1152,{'native':len(nr),'trajectory':len(tr)})
            for line in nr:
                a=int(line['hx_input_a']) if mode!='legacy' else int(line['adc_a'])
                b=int(line['hx_input_b']) if mode!='legacy' else int(line['adc_b'])
                assert int(line['native_sum'])==a+b and int(line['native_bit'])==max(a,b)
                assert int(line['cpu_cycle_tsc_ticks'])>0 and int(line['cpu_feedback_tsc_ticks'])>0
                if mode!='legacy':
                    assert abs(float(line['acdc_max_residual']))<1e-12
                    assert all(math.isfinite(float(line[key])) for key in ['acdc_dc_0','acdc_dc_1','entropy_min_y','entropy_max_y'])
                    assert int(line['cpu_batch_work_ticks'])>0 and int(line['cpu_batch_cache_ticks'])>0
            if case=='no_excitation':
                assert all(abs(float(t['charge_a_v']))<1e-14 and abs(float(t['charge_b_v']))<1e-14 for t in tr)
    # Repetition and independent subsystem ablation: source-derived controller
    # MUST produce changed HX89 inputs and decisions when a dependency is removed.
    baseline=rows(D/'integrated/closed_loop_native.csv')
    repeat=rows(D/'integrated/closed_loop_repeat_native.csv')
    ignore={'cpu_cycle_tsc_ticks','cpu_feedback_tsc_ticks','cpu_migrated','cpu_batch_work_ticks','cpu_batch_cache_ticks','rdrand_ok','rdseed_ok'}
    check=lambda a,b:{k:v for k,v in a.items() if k not in ignore}=={k:v for k,v in b.items() if k not in ignore}
    record('closed_loop_deterministic_native_work_state',all(check(a,b) for a,b in zip(baseline,repeat)),{'compared_rows':96,'excluded_only_nondeterministic_instruction_telemetry':sorted(ignore)})
    record('closed_loop_deterministic_voltage_trajectory',(D/'integrated/closed_loop_trajectory.csv').read_bytes()==(D/'integrated/closed_loop_repeat_trajectory.csv').read_bytes(),{'samples':1152})
    for mode in MODES[1:5]:
        other=rows(D/mode/'closed_loop_native.csv')
        inputs=sum((a['hx_input_a'],a['hx_input_b'])!=(b['hx_input_a'],b['hx_input_b']) for a,b in zip(baseline,other))
        decisions=sum(a['native_bit']!=b['native_bit'] for a,b in zip(baseline,other))
        record('causal_ablation_'+mode,inputs>0 and decisions>0,{'different_hx_inputs':inputs,'different_hx_decisions':decisions})
    # Fresh causal verification: previous native work hash is the EXACT next
    # CPU bit source (the relevant bit is checked against C/Fortran expression).
    bit_mismatch=0
    for idx,r in enumerate(baseline):
        if idx==0:prev_cpu=prev_batch=prev_feedback=0
        else:
            p=baseline[idx-1]
            prev_cpu=int(p['cpu_cycle_digest']);prev_batch=int(p['cpu_batch_digest']);prev_feedback=int(p['cpu_feedback_checksum'])
        expected=((prev_cpu^prev_batch^prev_feedback)>>(idx%63))&1
        # Original gate also mixes AC/DC sign and BVH sign. Check final XOR.
        ac_bit=int(float(r['acdc_dc_0'])>=0.)
        geo_bit=int(float(r['entropy_min_y'])>=0.)
        expected_feedback=expected^ac_bit^geo_bit
        if expected_feedback!=int(r['feedback_input']):bit_mismatch+=1
    record('native_previous_cpu_and_batch_digest_to_next_hx89',bit_mismatch==0,{'checked':96,'mismatches':bit_mismatch})
    # Negative tests MUST fail closed on original circuit and binary mutations.
    with tempfile.TemporaryDirectory(prefix='void_unified_negative_') as tmp:
        t=Path(tmp); source=t/'source';source.mkdir();shutil.copy2(P/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir',source)
        shutil.copy2(P/'VOID_K_MESH_V1.lib',source)
        (source/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir').write_bytes((source/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir').read_bytes().replace(b'R_INTEG_A',b'R_INTEG_X',1))
        (t/'negative_source').mkdir()
        run('reject_modified_K06',[exe,source,H,t/'negative_source','integrated'],negative=True,contains='K06 sha256 mismatch')
        binary=t/'hx89';shutil.copy2(H,binary)
        with binary.open('ab') as f:f.write(b'INTENTIONAL_SHA256_CORRUPTION')
        (t/'negative_binary').mkdir()
        run('reject_modified_HX89',[exe,P,binary,t/'negative_binary','integrated'],negative=True,contains='native HX89 execution failed')
        run('reject_invalid_mode',[exe,P,H,t/'negative_binary','unsupported'],negative=True,contains='invalid integration mode')
    record('unified_native_gate_complete',True,{'modes':len(MODES),'scenarios_per_mode':len(CASES),'native_hx89_invocations':len(MODES)*len(CASES)*96})
except Exception as e:
    print('CANONICAL_GATE_FAIL',repr(e),file=sys.stderr)
    results.append({'name':'exception','pass':False,'details':repr(e)})
finally:
    report={'schema':'VOID_UNIFIED_NATIVE_ACCEPTANCE_V1','tested_source':'05_HX89_K06_BRIDGE/03_UNIFIED_NATIVE_CLOSED_LOOP','passed':sum(x['pass'] for x in results),'failed':sum(not x['pass'] for x in results),'results':results,'physics_note':'Native RC subgraph and native source-derived algorithmic calculations. No bench telemetry supplied.','timestamp_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}
    (D/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CANONICAL_GATE_RESULT',report['passed'],'passed',report['failed'],'failed')
    if report['failed']:sys.exit(1)
