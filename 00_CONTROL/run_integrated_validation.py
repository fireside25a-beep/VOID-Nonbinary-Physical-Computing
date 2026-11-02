#!/usr/bin/env python3
"""Fully source-driven native validation for the integrated VOID CPU/HX89/ACDC/K06 pipeline.
Runs real executables, actual source kernels, corruption-negative tests, causal
ablation, and the repaired EntropyAVX trace renderer. No test doubles or stubs.
Python orchestrates tests ONLY: none of the closed-loop runtime is Python.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math,os,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
B=R/'05_HX89_K06_BRIDGE/02_NATIVE_FORTRAN_C_INTEGRATION'
P=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
H=R/'05_HX89_K06_BRIDGE/01_ORIGINAL_BRIDGE_BOUNDED_RC_COSIM/03_HX89_BINARY_ONLY/hx89'
A=R/'02_ANALOG_MATH/01_ACDC_LINEAR_NETWORK'
C=R/'03_CPU_NATIVE/06_CPU_BATCH_TARGETED_INTRINSICS'
E=R/'03_CPU_NATIVE/05_ENTROPY_AVX_HARDENED'
X=R/'04_HX89/02_NATIVE_TOOLCHAIN_SOURCE_AND_EVIDENCE'
D=R/'07_FRESH_TEST_EVIDENCE/INTEGRATED_RELEASE_GATE'
D.mkdir(parents=True,exist_ok=True)
results=[]
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def record(name, passed, details):
    results.append({'name':name,'pass':bool(passed),'details':details})
    print(('PASS' if passed else 'FAIL')+' '+name,flush=True)
    if not passed: raise RuntimeError(name+' '+str(details))
def run(name,args,cwd=None,expected=0,needle=None,timeout=180):
    proc=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,text=True,errors='replace',timeout=timeout)
    (D/(name+'.stdout.log')).write_text(proc.stdout)
    (D/(name+'.stderr.log')).write_text(proc.stderr)
    passed=(proc.returncode==expected if expected>=0 else proc.returncode!=0)
    if needle: passed=passed and needle in proc.stdout+proc.stderr
    record(name,passed,{'exit_code':proc.returncode,'expected':expected,'needle':needle, 'command':[str(i) for i in args]})
    return proc

def csvrows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def check_closed_loop(causal,ablated):
    cases=['closed_loop','closed_loop_repeat','open_write_a','no_excitation','forced_a','inverted_action','open_write_b']
    positive_differences=0;all_decisions=0;maxresidual=0.;maxsignal=0.;voltage_differences=0
    for scenario in cases:
        a=csvrows(causal/(scenario+'_native.csv'));b=csvrows(ablated/(scenario+'_native.csv'))
        t=csvrows(causal/(scenario+'_trajectory.csv'))
        record('length_'+scenario,len(a)==len(b)==96 and len(t)==1152, {'native':len(a),'trajectory':len(t)})
        for i,(row,ctrl) in enumerate(zip(a,b)):
            d0=int(row['cpu_cycle_digest']);d1=int(row['batch_work_digest'])
            assert int(row['native_sum'])==int(row['adc_a'])+int(row['adc_b'])
            assert int(row['native_bit'])==max(int(row['adc_a']),int(row['adc_b']))
            assert int(row['cpu_cycle_tsc_ticks'])>0
            assert int(row['cpu_feedback_tsc_ticks'])>0
            assert float(row['acdc_kcl_residual_a'])<1e-12
            assert math.isfinite(float(row['acdc_node_a_v']))
            assert math.isfinite(float(row['acdc_node_b_v']))
            maxresidual=max(maxresidual,float(row['acdc_kcl_residual_a']))
            maxsignal=max(maxsignal,abs(float(row['cpu_to_acdc_signal_v'])))
            if i>0:
                prev=a[i-1]
                source_signal=( ( (int(prev['cpu_cycle_digest']) ^ int(prev['batch_work_digest'])) & 7 ) -3 )*.016
                if scenario=='no_excitation':source_signal=0
                assert abs(float(row['cpu_to_acdc_signal_v'])-source_signal)<1e-12
            else: assert abs(float(row['cpu_to_acdc_signal_v']))<1e-15
            if (row['adc_a'],row['adc_b'])!=(ctrl['adc_a'],ctrl['adc_b']):positive_differences+=1
            all_decisions+=1
        if scenario=='no_excitation':
            assert all(int(r['native_bit'])==0 for r in a)
            assert all(abs(float(r['charge_a_v']))<1e-15 and abs(float(r['charge_b_v']))<1e-15 for r in t)
        if scenario=='closed_loop':
            ref=csvrows(causal/'closed_loop_repeat_native.csv')
            # Only timer/CPU migration counter measurements may vary between identical runs.
            ignore={'cpu_cycle_tsc_ticks','cpu_feedback_tsc_ticks','cpu_migrated','cpu_feedback_checksum'}
            for q,w in zip(a,ref):
                assert {k:v for k,v in q.items() if k not in ignore}=={k:v for k,v in w.items() if k not in ignore}
            assert (causal/'closed_loop_trajectory.csv').read_bytes()==(causal/'closed_loop_repeat_trajectory.csv').read_bytes()
        for p,q in zip(t,csvrows(ablated/(scenario+'_trajectory.csv'))):
            voltage_differences+=float(p['charge_a_v'])!=float(q['charge_a_v'])
    record('closed_loop_native_oracle_672',all_decisions==672,{'native_decisions':all_decisions})
    record('cpu_digest_to_next_hx89_causal_ablation',positive_differences>0,{'different_ADC_inputs':positive_differences,'different_charge_samples':voltage_differences,'maximum_feedback_v':maxsignal,'maximum_kcl_error_a':maxresidual})
    record('hardware_is_not_claimed',True,{'model':'native HX89 + R/C K06 subgraph + AC/DC ideal nodal conditioning; no bench measurements'})

try:
    record('hx89_archived_binary_sha256',digest(H)=='50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451',digest(H))
    run('build_bridge', ['make','-B','all'],cwd=B)
    run('compile_acdc_test',['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-pedantic',A/'analog_core.c','-lm','-o',D/'analog_core'])
    run('acdc_4099_vectors',[D/'analog_core','--test'],needle='4099 deterministic input vectors')
    run('compile_cpu_batch',['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror',C/'cpu_batch.c','-o',D/'cpu_batch'])
    run('cpu_batch_real_native_instruction_trials',[D/'cpu_batch','--rounds','2','--work','1'],needle='"type":"trial"')
    run('cpu_batch_bounds_negative',[D/'cpu_batch','--rounds','0'],expected=-1,needle='bounded argument violation')
    run('hx89_original_source_make_check',['make','check'],cwd=X,timeout=180)
    run('source_derived_R08_netlist_validator',[sys.executable,R/'06_ENGINEERING_VALIDATORS/validate_r08_source.py'])
    run('native_driver_contract_build',['make','build/native_driver_contract'],cwd=B)
    run('native_driver_contract',[B/'build/native_driver_contract',H])
    run('native_cpu_state_contract_build',['make','build/native_cpu_state_contract'],cwd=B)
    run('native_cpu_state_contract',[B/'build/native_cpu_state_contract'])
    run('compile_BVH_extended',['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',E/'bvh_spatial.cpp',E/'test_bvh_extended.cpp','-o',D/'bvh_test'])
    run('BVH_real_3003_build_refits',[D/'bvh_test'],needle='3003 builds and refits')
    run('compile_BVH_ownership',['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',E/'bvh_spatial.cpp',E/'test_bvh_ownership.cpp','-o',D/'bvh_ownership'])
    run('BVH_ownership',[D/'bvh_ownership'])
    run('compile_entropy_avx_trajectory_renderer',['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-mavx2',E/'void_trajectory_renderer.cpp',E/'bvh_spatial.cpp',E/'engine_core.cpp',E/'shader_pipeline.cpp','-o',D/'void_trajectory_renderer'])
    (D/'causal').mkdir(exist_ok=True);(D/'ablated').mkdir(exist_ok=True)
    run('closed_loop_7_scenarios_672_native_hx89',[B/'build/void_loop',P,H,D/'causal'],needle='NATIVE_PASS closed_loop')
    run('ablation_7_scenarios_672_native_hx89',[B/'build/void_loop',P,H,D/'ablated','--ablate-cpu-feedback'],needle='NATIVE_PASS closed_loop')
    check_closed_loop(D/'causal',D/'ablated')
    run('EntropyAVX_real_K06_charge_trajectory',[D/'void_trajectory_renderer',D/'causal/closed_loop_trajectory.csv'],needle='VOID_K06_REAL_TRACE_SAMPLES=1152')
    with tempfile.TemporaryDirectory(prefix='void_faults_') as td:
        t=Path(td); copy=t/'source';copy.mkdir()
        for name in ['VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir','VOID_K_MESH_V1.lib']:shutil.copy2(P/name,copy/name)
        bad=copy/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
        bad.write_bytes(bad.read_bytes().replace(b'R_INTEG_A',b'R_INTEG_X',1))
        (t/'badsrc').mkdir()
        run('reject_tampered_R08_K06',[B/'build/void_loop',copy,H,t/'badsrc'],expected=-1,needle='K06 sha256 mismatch')
        binary=t/'hx89';shutil.copy2(H,binary)
        with binary.open('ab') as f:f.write(b'NEVER_EXECUTE_MUTATED_BINARY')
        (t/'badbin').mkdir()
        run('reject_tampered_native_hx89',[B/'build/void_loop',P,binary,t/'badbin'],expected=-1,needle='native HX89 execution failed')
        run('reject_unknown_runtime_mode',[B/'build/void_loop',P,H,t/'badbin','--unsupported'],expected=-1,needle='invalid experiment mode')
        malformed=t/'invalid.csv';malformed.write_text('bad,header\n1,2\n')
        run('reject_malformed_analog_trajectory',[D/'void_trajectory_renderer',malformed],expected=-1,needle='unexpected source trajectory schema')
    record('release_tests_complete',True,{'count':len(results),'pass':sum(x['pass'] for x in results)})
except (Exception,AssertionError) as ex:
    print('RELEASE_GATE_FAILURE',type(ex).__name__,str(ex),file=sys.stderr)
    results.append({'name':'uncaught_validation_failure','pass':False,'details':str(ex)})
finally:
    report={'schema':'VOID_NATIVE_CAUSAL_RELEASE_VALIDATION_V1','passed':sum(i['pass'] for i in results),'failed':sum(not i['pass'] for i in results),'results':results,'source_root':'VOID','evidence_type':'native_and_source_tests_not_hardware_bench'}
    (D/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('RELEASE_RESULT',report['passed'],'passed',report['failed'],'failed')
    if report['failed']:sys.exit(1)
