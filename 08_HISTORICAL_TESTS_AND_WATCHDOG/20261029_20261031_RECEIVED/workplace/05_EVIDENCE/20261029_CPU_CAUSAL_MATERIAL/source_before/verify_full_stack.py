#!/usr/bin/env python3
"""Independent replayless verification of ACTUAL saved CPU/HX89/gas executions.

No invented measurements and no execution on behalf of corrupt transcripts.
Does not promote finite digital lattice model results to physical experiments.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import full_stack_cycle as m


def digest(data):return hashlib.sha256(data).hexdigest()
def file_sha(path):return digest(path.read_bytes())

def assert_verified(out):
    result=json.loads((out/'FULL_STACK_EXECUTION.json').read_text())
    if result['schema']!='VOID_HX89_CPU_Q2_GAS_HX89_CPU_CLOSED_V2':raise ValueError('Invalid report schema')
    if result['physical_nonbinary_material_computation_verified'] is not False:raise ValueError('Unsupported physical claim')
    if result['actual_hardware_weak_inversion_control_verified'] is not False:raise ValueError('Unsupported on-die gate-bias claim')
    rows=result['feedback'];cycles=result['cycles']
    if cycles<4 or len(rows)!=cycles or result['native_trials']!=cycles*4:raise ValueError('Incomplete real cycles')
    if result['source_sha256']!=file_sha(HERE/'full_stack_cycle.py'):raise ValueError('Source modified since execution')
    if result['hx89_executable_sha256']!=file_sha(m.connector.HX89):raise ValueError('HX89 executable modified')
    if result['gas_executable_sha256']!=file_sha(m.GAS):raise ValueError('Gas executable modified')
    if result['native_executable_sha256']!=file_sha(m.base.EXEC):raise ValueError('CPU executable modified')
    changed=0
    for idx, row in enumerate(rows):
        if row['cycle']!=idx:raise ValueError('Cycle ordering tampered')
        pfx=out/f'round_{idx:03d}'
        native=pfx.with_suffix('.native.jsonl')
        if file_sha(native)!=row['native_trial_sha256']:raise ValueError('Native trace byte hash mismatch')
        header,trials=m.cycle.decode_real_native(native.read_text(),row['requested_cpu_control']['rotate'],row['requested_cpu_control']['work'])
        if row['observed_cpu_modes_in_order']!=[t['mode'] for t in trials]:raise ValueError('Mode observations tampered')
        if header['cpu']!=row['processor_id']:raise ValueError('Processor ID changed')
        observed=sum(t['post_ticks']+t['stimulus_ticks'] for t in trials)
        if observed!=row['cpu_instruction_tsc_total']:raise ValueError('CPU timing total inconsistent')
        q_out=pfx.with_suffix('.q2.hx89.stdout.txt')
        if file_sha(q_out)!=row['hx89_q2_stdout_sha256']:raise ValueError('Q2 native stdout hash mismatch')
        hx=m.cycle.decode_real_hx89(q_out.read_text(),observed%25)
        if hx!=row['executed_hx89_q2']:raise ValueError('Reported Q2 state mismatches execution')
        if row['hx89_q2_program_sha256']!=file_sha(m.connector.Q2PROGRAM):raise ValueError('Original Q2 program changed')
        gas=row['executed_gas_model_and_hx89']
        prefix=pfx
        picture=prefix.with_suffix('.gas.pgm')
        raw=picture.read_bytes()
        wh=16;header_pgm=b'P5\n16 16\n255\n'
        if len(raw)!=len(header_pgm)+wh*wh or not raw.startswith(header_pgm):raise ValueError('PGM bytes altered')
        pix=raw[len(header_pgm):]
        if any(b%42 for b in pix):raise ValueError('PGM occupancy impossible')
        profile=''.join(str((sum(pix[y*wh+x]//42 for y in range(wh))+wh//2)//wh) for x in range(wh))
        if profile!=gas['hexworld_profile']:raise ValueError('Reported gas profile mismatches image')
        for suffix,key in [('.gas.pgm','image_sha256'),('.gas.hx','polyform_sha256'),('.gas.stdout.txt','gas_stdout_sha256'),('.gas.hx89.stdout.txt','executed_hx89_gas_stdout_sha256')]:
            if file_sha(prefix.with_suffix(suffix))!=gas[key]:raise ValueError('Gas artifact modified '+suffix)
        gas_out=prefix.with_suffix('.gas.stdout.txt').read_text()
        match=m.GAS_RE.search(gas_out)
        if not match or int(match.group(3))!=gas['steps'] or int(match.group(4))!=gas['mass'] or int(match.group(7))!=gas['collisions'] or match.group(8)!=gas['model_state_final_hash']:
            raise ValueError('Gas reversal or mass evidence missing or modified')
        if not any(line==profile for line in prefix.with_suffix('.gas.hx89.stdout.txt').read_text().splitlines()):
            raise ValueError('HX89 executed model output differs from raw image')
        command=m.next_control(hx,gas,rows[0]['requested_cpu_control']['work'])
        if command!=row['next_cpu_control']:raise ValueError('Causal next command differs from real machine outputs')
        changed+=command!=row['requested_cpu_control']
        if idx+1<cycles and command!=rows[idx+1]['requested_cpu_control']:
            raise ValueError('Subsequent CPU command not derived from preceding executed HX89 state')
    if changed!=result['changed_cpu_commands'] or changed<1:raise ValueError('Missing real command changes')
    return {'verified_cycles':cycles,'verified_cpu_interventions':cycles*4,
            'verified_hx89_gas_reversals':cycles,'command_changed_cycles':changed,
            'physical_nonbinary_material_computation_verified':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out',type=Path);args=p.parse_args()
    try:print(json.dumps(assert_verified(args.out),indent=2))
    except Exception as exc:print(json.dumps({'status':'FAIL','error':str(exc)}),file=sys.stderr);sys.exit(1)
