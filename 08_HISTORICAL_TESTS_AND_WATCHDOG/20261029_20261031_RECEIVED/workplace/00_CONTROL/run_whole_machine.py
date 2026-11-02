#!/usr/bin/env python3
"""Cumulative REAL native verification of the existing VOID/HX89 worktrees.

No synthetic analog data, no claim of access to on-die gate bias or physical K06
wiring. Reject unverified machine claims; preserve failed attempts and transcripts.
This is independent verification software, not a VOID material computing runtime.
"""
from __future__ import annotations
import argparse
import os
import csv
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT/'03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE'
AVX = ROOT/'03_NATIVE_TOOLCHAIN/EntropyAVX'
LOG = ROOT/'04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART'
sys.path.insert(0,str(ROOT/'00_CONTROL'))
import run_workplace_watchdog as wd
import execution_guard
sys.path.insert(0,str(BATCH))
import batch_bridge as bridge


def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def inspect_batch(path, n):
    r=json.loads((path/'BIDIRECTIONAL_EXECUTION.json').read_text())
    if r['cycles'] != n or r['cpu_native_trials'] != n*4:
        raise RuntimeError('Executed cycle/trial counts mismatch')
    if r['physical_nonbinary_material_computation_verified'] is not False:
        raise RuntimeError('Unproven physical operation was incorrectly certified')
    feedback=r['feedback']
    if len(feedback)!=n or r['command_changed_cycles']<1:
        raise RuntimeError('Incomplete or inactive feedback loop')
    for i, row in enumerate(feedback):
        if row['cycle']!=i:
            raise RuntimeError('Non-contiguous cycle sequence')
        base=path/f'round_{i:03d}'
        if digest(base.with_suffix('.native.jsonl'))!=row['native_trial_sha256']:
            raise RuntimeError('Native execution trace altered: '+str(i))
        if digest(base.with_suffix('.hx89.stdout.txt'))!=row['hx89_stdout_sha256']:
            raise RuntimeError('HX89 native trace altered: '+str(i))
        if i>0 and feedback[i-1]['next_cpu_control_from_executed_hx89']!=row['requested_cpu_control']:
            raise RuntimeError('Native CPU control chain broken: '+str(i))
        if len(row['observed_cpu_modes_in_order'])!=4:
            raise RuntimeError('Incomplete native work schedule')
    return {'cycles':n,'real_native_interventions':n*4,'hx89_search_transitions':n,
            'changing_cpu_commands':r['command_changed_cycles'],
            'feedback_sha256':digest(path/'BIDIRECTIONAL_EXECUTION.json')}


def verify_milestones():
    a=bridge.check_master()
    with (ROOT/'00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv').open(newline='') as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    if len(rows)!=116 or any(r['physical_nonbinary_completion']!='NOT_VERIFIED' for r in rows):
        raise RuntimeError('Missing milestones or unproved physical promotion')
    return a


_EXCLUSIVE_FD = None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--cycles',type=int,default=32)
    ap.add_argument('--cache-causal',action='store_true',help='Run physical cache intervention inside the complete live CPU/HX89 feedback path')
    ap.add_argument('--history-causal',action='store_true',help='Run real randomized 3-intensity native history within full HX89 feedback cycle')
    ap.add_argument('--material-history',action='store_true',help='Extend full HX89 machine with actual cross-core 3-intensity stimulus and memory retention falsification')
    ap.add_argument('--material-blocks',type=int,default=8,help='Real CPU crossover blocks per hold condition, bounded 1..24')
    ap.add_argument('--dual-physical',action='store_true',help='Run REAL two-core simultaneous physical-response experiment through complete HX89 machine')
    ap.add_argument('--dual-blocks',type=int,default=16,help='Counterbalanced real A/B/A+B factorial blocks per hold, 2..24')
    a=ap.parse_args()
    if not 4<=a.cycles<=64:
        raise SystemExit('Cycle bounds: 4..64')
    if not 1<=a.material_blocks<=24:
        raise SystemExit('Material crossover blocks: 1..24')
    if not 2<=a.dual_blocks<=24:
        raise SystemExit('Real two-core factorial blocks: 2..24')
    LOG.mkdir(parents=True,exist_ok=True)
    rid=str(time.time_ns())
    entry=[]
    orig={p.name:digest(p) for p,_ in wd.PARTS}
    orig.update({p.name:digest(p) for _,p,_,_ in wd.SOURCES})
    def record(name,status,detail):
        e={'run_id':rid,'sequence':len(entry),'stage':name,'status':status,'detail':detail}
        entry.append(e)
        with (LOG/'WHOLE_MACHINE_APPEND_ONLY_EVENTS.jsonl').open('a') as f:
            f.write(json.dumps(e,sort_keys=True)+'\n')
        print(json.dumps({'stage':name,'status':status,'detail':detail}),flush=True)
    def direct(name,func):
        try:record(name,'PASS',func())
        except Exception as e:record(name,'FAIL',{'error':str(e)})
    def command(name,cmd,cwd,timeout):
        fn=LOG/f'{name}.{rid}.log'
        try:
            with fn.open('x') as f:
                extra = {}
                if name == "existing_full_watchdog_11_gates":
                    if _EXCLUSIVE_FD is None: raise RuntimeError("Missing exclusive-run guard")
                    env = os.environ.copy()
                    env["VOID_MACHINE_LOCK_FD"] = str(_EXCLUSIVE_FD)
                    extra = {"env": env, "pass_fds": (_EXCLUSIVE_FD,)}
                p=subprocess.run(cmd,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,**extra)
            if p.returncode:record(name,'FAIL',{'exit_status':p.returncode,'log':str(fn),'sha256':digest(fn)})
            else:record(name,'PASS',{'log':str(fn),'sha256':digest(fn)})
        except Exception as e:record(name,'FAIL',{'error':str(e),'log':str(fn)})
    direct('historical_116_and_current_physical_claims',verify_milestones)
    direct('original_archive_crc_sha256',wd.source_gate)
    direct('K01_K06_real_netlist_source_integrity',wd.netlist_gate)
    command('existing_full_watchdog_11_gates',[sys.executable,str(ROOT/'00_CONTROL/run_workplace_watchdog.py'),'--runs','1'],ROOT,240)
    command('native_negative_and_real_tests',[sys.executable,'-m','unittest','-v','test_bridge','test_closed_native_cycle'],BATCH,70)
    path=LOG/f'FULL_MACHINE_CYCLE_{rid}'
    command('native_cpu_hx89_cpu_closed_cycle',[sys.executable,str(BATCH/'closed_native_cycle.py'),
        '--rounds',str(a.cycles),'--base-work','4','--out',str(path)],BATCH,200)
    if (path/'BIDIRECTIONAL_EXECUTION.json').exists():
        direct('closed_cycle_bytewise_trace_and_causality',lambda:inspect_batch(path,a.cycles))
    else:
        record('closed_cycle_bytewise_trace_and_causality','FAIL',{'reason':'No complete execution manifest'})
    # Full HX89 lateral paths + reversible gas-model Polyform -> next native CPU.
    command('new_full_stack_adversarial_tests',[sys.executable,'-m','unittest','-v','test_full_stack'],BATCH,75)
    stackpath=LOG/f'FULL_STACK_CYCLE_{rid}'
    command('full_stack_native_hx89_gas_native',[sys.executable,str(BATCH/'full_stack_cycle.py'),
        '--rounds',str(a.cycles),'--base-work','4','--out',str(stackpath)],BATCH,120)
    if (stackpath/'FULL_STACK_EXECUTION.json').exists():
        try:
            sys.path.insert(0,str(BATCH))
            import verify_full_stack
            direct('full_stack_trace_validation',lambda:verify_full_stack.assert_verified(stackpath))
        except Exception as ex:
            record('full_stack_trace_validation','FAIL',{'error':str(ex)})
    else:
        record('full_stack_trace_validation','FAIL',{'reason':'No complete full-stack execution'})
    if a.cache_causal:
        command('material_cache_real_native_adversarial_tests',
                [sys.executable,'-m','unittest','-v','test_material_causal'],BATCH,70)
        cachepath=LOG/f'MATERIAL_CACHE_FULL_STACK_{rid}'
        command('material_cache_inside_full_hx89_cycle',
                [sys.executable,str(BATCH/'full_stack_cycle.py'), '--rounds',str(a.cycles),
                 '--base-work','4','--cache-probe','--out',str(cachepath)],BATCH,190)
        if (cachepath/'FULL_STACK_EXECUTION.json').is_file():
            try:
                import verify_full_stack
                direct('material_cache_independent_causal_trace_validation',
                       lambda:verify_full_stack.assert_verified(cachepath))
            except Exception as exc:
                record('material_cache_independent_causal_trace_validation','FAIL',{'error':str(exc)})
        else:
            record('material_cache_independent_causal_trace_validation','FAIL',
                   {'reason':'Measured full-stack evidence missing'})
    if a.cache_causal:
        command('power_timing_adversarial_real_HX89_tests',
                [sys.executable,'-m','unittest','-v','test_power_into_hx89'],BATCH,90)
        powerpath=LOG/f'POWER_HX89_CYCLE_{rid}'
        command('real_CPU_power_candidate_into_HX89_into_CPU',
                [sys.executable,str(BATCH/'power_into_hx89.py'), '--trials','80','--out',str(powerpath)],BATCH,75)
        if (powerpath/'POWER_HX89_EXECUTION.json').is_file():
            try:
                import power_into_hx89
                direct('independent_real_power_timing_chain_verification',
                       lambda:power_into_hx89.verify(powerpath))
            except Exception as exc:
                record('independent_real_power_timing_chain_verification','FAIL',{'error':str(exc)})
        else:
            record('independent_real_power_timing_chain_verification','FAIL',{'reason':'No completed acquisition'})
    if a.history_causal:
        command('three_intensity_real_hx89_adversarial_tests',
                [sys.executable,'-m','unittest','-v','test_history_causal'],BATCH,90)
        histpath=LOG/f'HX89_THREE_INTENSITY_HISTORY_{rid}'
        command('real_three_intensity_inside_full_hx89_machine',
                [sys.executable,str(BATCH/'full_stack_cycle.py'), '--rounds',str(a.cycles),
                 '--base-work','4','--history-probe','--out',str(histpath)],BATCH,190)
        if (histpath/'FULL_STACK_EXECUTION.json').is_file():
            try:
                import verify_full_stack
                direct('independent_three_intensity_live_feedback_verification',
                       lambda:verify_full_stack.assert_verified(histpath))
            except Exception as exc:
                record('independent_three_intensity_live_feedback_verification','FAIL',{'error':str(exc)})
        else:
            record('independent_three_intensity_live_feedback_verification','FAIL',
                   {'reason':'No complete authentic three-intensity execution report'})
    if a.material_history:
        # Always execute the material candidate THROUGH original HX89 full-stack
        # source; no separate material-state simulator or manufactured analog data.
        matpath=LOG/f'CPU_PHYSICAL_MATERIAL_GATE_{rid}'
        command('real_cross_core_inside_full_hx89_machine',
                [sys.executable,'-S',str(BATCH/'cross_core_material_gate.py'),
                 '--out',str(matpath),'--blocks',str(a.material_blocks)],
                BATCH,170)
        if (matpath/'result.json').is_file():
            try:
                import cross_core_material_gate as material
                direct('independent_cross_core_hx89_material_evidence',
                       lambda:material.verify(matpath))
                def cross_negative():
                    env=os.environ.copy()
                    env['VOID_REAL_CROSS_CORE_RUN']=str(matpath)
                    result=subprocess.run([sys.executable,'-S','-m','unittest','-v','test_cross_core_material_gate'],
                        cwd=BATCH,env=env,capture_output=True,text=True,timeout=30)
                    log=LOG/f'cross_core_adversarial_tests.{rid}.log'
                    log.write_text(result.stdout+result.stderr)
                    if result.returncode:
                        raise RuntimeError('Native material trace tests failed: '+result.stderr[-700:])
                    return {'test_cases':7,'log':str(log),'sha256':digest(log)}
                direct('adversarial_cross_core_real_trace_tests',cross_negative)
            except Exception as exc:
                record('independent_cross_core_hx89_material_evidence','FAIL',{'error':str(exc)})
        else:
            record('independent_cross_core_hx89_material_evidence','FAIL',{'reason':'No acquired physical candidate evidence'})
        command('entropyavx_real_native_frames',[sys.executable,'microkernel.py'],AVX,45)
    if a.dual_physical:
        # This experiment is a genuine multi-CPU intervention inside the existing
        # HX89 machine and it is not permitted to claim physical analog success.
        dualpath=LOG/f'DUAL_REAL_CPU_AND_HX89_{rid}'
        command('real_two_input_cpu_hx89_full_machine',
            [sys.executable,'-S',str(BATCH/'dual_reservoir_hx89.py'),
             '--out',str(dualpath),'--blocks',str(a.dual_blocks)],BATCH,145)
        if (dualpath/'ACQUIRED_FACTORIAL_HX89_RESULT.json').is_file():
            try:
                import dual_reservoir_hx89 as dual
                direct('independent_real_two_input_hx89_trace_verification',
                       lambda:dual.verify(dualpath))
                def dual_negative():
                    env=os.environ.copy()
                    env['VOID_DUAL_REAL_RUN']=str(dualpath)
                    tested=subprocess.run([sys.executable,'-S','-m','unittest','-v','test_dual_reservoir_hx89'],
                        cwd=BATCH,env=env,capture_output=True,text=True,timeout=30)
                    logfile=LOG/f'dual_physical_real_trace_negative_tests.{rid}.log'
                    logfile.write_text(tested.stdout+tested.stderr)
                    if tested.returncode:raise RuntimeError('actual two-input trace negatives failed: '+tested.stderr[-800:])
                    return {'test_cases':8,'log':str(logfile),'sha256':digest(logfile)}
                direct('real_two_input_cpu_adversarial_integrity_tests',dual_negative)
            except Exception as exc:
                record('real_two_input_cpu_independent_evidence','FAIL',{'error':str(exc)})
        else:
            record('independent_real_two_input_hx89_trace_verification','FAIL',
                   {'reason':'No complete real dual-input hardware acquisition'})
    after={p.name:digest(p) for p,_ in wd.PARTS}
    after.update({p.name:digest(p) for _,p,_,_ in wd.SOURCES})
    direct('all_original_uploads_unchanged',lambda:{'five_original_hashes_unchanged': True} if after==orig else (_ for _ in ()).throw(RuntimeError('Original archive changed')))
    result={'schema':'VOID_HX89_CUMULATIVE_WHOLE_MACHINE_ACCEPTANCE_V1',
            'run_id':rid,'stages':entry,'tested_stages':len(entry),'passed':sum(e['status']=='PASS' for e in entry),
            'failed':sum(e['status']=='FAIL' for e in entry),
            'native_architecture_execution_verified':all(e['status']=='PASS' for e in entry),
            'physical_nonbinary_cpu_substrate_verified':False,
            'cache_causality_live_integration_attempted':bool(a.cache_causal),
            'three_intensity_real_history_inside_full_machine':bool(a.history_causal),
            'cross_core_material_candidate_inside_machine':bool(a.material_history),
            'simultaneous_two_input_cpu_candidate_inside_machine':bool(a.dual_physical),
            'two_input_factorial_blocks':a.dual_blocks if a.dual_physical else 0,
            'material_crossover_blocks':a.material_blocks if a.material_history else 0,
            'K06_physical_injection_measurement_verified':False,
            'actual_hardware_weak_inversion_control_verified':False,
            'actual_physical_collective_charge_network_verified':False,
            'original_upload_sha256':after,
            'scope':'REAL CPU instruction execution, real HX89, real EntropyAVX; physical analog substrate NOT demonstrated'}
    dest=LOG/f'WHOLE_MACHINE_ACCEPTANCE_{rid}.json'
    with dest.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'acceptance':str(dest),'passed':result['passed'],'failed':result['failed'],
                      'physical_nonbinary_cpu_substrate_verified':False},indent=2))
    return int(result['failed']!=0)

if __name__=='__main__':
    try:
        with execution_guard.exclusive() as fd:
            _EXCLUSIVE_FD = fd
            sys.exit(main())
    except RuntimeError as exc:
        print("FAIL-CLOSED NATIVE RUN:",exc,file=sys.stderr)
        sys.exit(2)
