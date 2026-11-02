#!/usr/bin/env python3
"""Run the ONE cumulative VOID/HX89 native machine test suite repeatedly.

No simulation of analog measurements, no erased failures, no autonomous chat
watchdog. These are real native programs and a physically *unproved* CPU-material
candidate, with negative controls and independent source-evidence checks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTROL=ROOT/'00_CONTROL'
LOGROOT=ROOT/'04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS'
ORIGINAL=ROOT/'01_SOURCES_VERIFIED/00_ORIGINAL_USER_UPLOADS'
FILES=(
    'VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip',
    'EntropyAVXEngine-source-trace-and-bootstrap(3).zip',
    'AC_DC_Passive_AI_Proof(2)(1).zip',
    'VOID_COMPLETE_VOLUME_PART_01_OF_02.zip.001',
    'VOID_COMPLETE_VOLUME_PART_02_OF_02.zip.002'
)

def sha(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def accepted_after(before):
    candidates=[p for p in (ROOT/'04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART').glob('WHOLE_MACHINE_ACCEPTANCE_*.json') if p.stat().st_mtime_ns>before]
    if not candidates:raise RuntimeError('Whole-run process generated no new acceptance receipt')
    p=max(candidates,key=lambda v:v.stat().st_mtime_ns)
    r=json.loads(p.read_text())
    if r['tested_stages']!=r['passed']+r['failed']:raise ValueError('Incomplete acceptance rows')
    return p,r

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repeat',type=int,default=2)
    ap.add_argument('--cycles',type=int,default=4)
    ap.add_argument('--material-blocks',type=int,default=8)
    ap.add_argument('--dual-physical',action='store_true',help='include simultaneous A/B/A+B measured CPU response in complete VOID/HX89 runner')
    ap.add_argument('--dual-blocks',type=int,default=16)
    a=ap.parse_args()
    if not 1<=a.repeat<=4 or not 4<=a.cycles<=32 or not 1<=a.material_blocks<=24 or not 2<=a.dual_blocks<=24:
        raise SystemExit('Out-of-bounds test parameters (repeat 1..4, cycles 4..32, blocks 1..24)')
    if not all((ORIGINAL/f).is_file() for f in FILES):
        raise RuntimeError('Historical originals missing; refusal to substitute test data')

    LOGROOT.mkdir(parents=True,exist_ok=True)
    session=f'canonical_{time.time_ns()}'
    sessiondir=LOGROOT/session
    sessiondir.mkdir()
    before={name:sha(ORIGINAL/name) for name in FILES}
    env=os.environ.copy()
    env.update(PYTHONHASHSEED='0',PYTHONNOUSERSITE='1')
    receipts=[]
    repair=[sys.executable,'-S',str(CONTROL/'repair_restored_native_build.py')]
    with (sessiondir/'00_native_build_repair.log').open('x') as f:
        fix=subprocess.run(repair,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=120)
    if fix.returncode:
        raise RuntimeError('Native repair/build failed; retained original log. No test PASS claimed.')
    for run in range(1,a.repeat+1):
        cmd=[sys.executable,'-S',str(CONTROL/'run_whole_machine.py'),
             '--cycles',str(a.cycles),'--cache-causal','--history-causal',
             '--material-history','--material-blocks',str(a.material_blocks)]
        if a.dual_physical:cmd += ['--dual-physical','--dual-blocks',str(a.dual_blocks)]
        old=time.time_ns()
        logfile=sessiondir/f'{run:02d}_complete_machine.log'
        started=time.monotonic()
        with logfile.open('x') as f:
            try:
                p=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=950)
                exit_code=p.returncode
            except subprocess.TimeoutExpired:
                exit_code=124
        elapsed=time.monotonic()-started
        outcome={'index':run,'exit_code':exit_code,'elapsed_s':round(elapsed,3),
                 'command':cmd,'log_path':str(logfile.relative_to(ROOT)),'log_sha256':sha(logfile)}
        try:
            accept,r=accepted_after(old)
            outcome.update(acceptance_path=str(accept.relative_to(ROOT)),acceptance_sha256=sha(accept),
                           stages=r['tested_stages'],passed=r['passed'],failed=r['failed'],
                           physical_nonbinary_cpu_substrate_verified=r['physical_nonbinary_cpu_substrate_verified'])
            needed=27 if a.dual_physical else 23
            native_pass=(r['failed']==0 and r['tested_stages']>=needed and exit_code==0
                and bool(r.get('simultaneous_two_input_cpu_candidate_inside_machine',False))==a.dual_physical)
            outcome['native_gates_passed']=native_pass
            if native_pass:
                outcome['classification']=('NATIVE_FULL_STACK_DUAL_INPUT_PASS_PHYSICAL_GATE_UNVERIFIED'
                    if a.dual_physical else 'NATIVE_FULL_STACK_PASS_PHYSICAL_GATE_UNVERIFIED')
            else:
                outcome['classification']='EXECUTION_FAILURE_OR_INCOMPLETE'
        except Exception as exc:
            outcome['classification']='MISSING_OR_INVALID_RECEIPT'
            outcome['error']=str(exc)
        receipts.append(outcome)
        with (sessiondir/'APPEND_ONLY_EXECUTIONS.jsonl').open('a') as f:
            f.write(json.dumps(outcome,sort_keys=True)+'\n')
        print(json.dumps({'run':run,'status':outcome['classification'],
                          'pass':outcome.get('passed'),'fail':outcome.get('failed')}),flush=True)
    after={name:sha(ORIGINAL/name) for name in FILES}
    result={'schema':'VOID_HX89_CANONICAL_REPEATED_FULL_NATIVE_V2' if a.dual_physical else 'VOID_HX89_CANONICAL_REPEATED_FULL_NATIVE_V1',
            'suite_session':session,'repeat':a.repeat,'cycles':a.cycles,
            'material_blocks':a.material_blocks, 'simultaneous_dual_cpu_gate_requested':a.dual_physical, 'dual_factorial_blocks':a.dual_blocks if a.dual_physical else 0, 'deterministic_software_inputs':True,
            'physical_measurement_bitwise_determinism_claimed':False,
            'original_source_archive_hashes':before,
            'original_hashes_unchanged':before==after,'executions':receipts,
            'all_native_execution_suites_passed':all(x.get('native_gates_passed') is True for x in receipts),
            'independently_verified_physical_nonbinary_material_machine':False}
    with (sessiondir/'REPEATED_MACHINE_RESULT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'summary':str(sessiondir/'REPEATED_MACHINE_RESULT.json'),
                      'native_pass':result['all_native_execution_suites_passed'],
                      'originals_unchanged':result['original_hashes_unchanged'],
                      'physical_nonbinary_gate':'NOT_ESTABLISHED'},indent=2),flush=True)
    return 0 if result['all_native_execution_suites_passed'] and result['original_hashes_unchanged'] else 1

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:
        print('FAIL-CLOSED CANONICAL TEST RUNNER:',e,file=sys.stderr);sys.exit(2)
