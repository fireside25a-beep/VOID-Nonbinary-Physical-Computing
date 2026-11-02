#!/usr/bin/env python3
"""Measured CPU -> HX89 Q² -> reversible gas -> executed HX89 emissions -> next CPU.

ALL carried values are binary/digital HOST telemetry and model states. No raw on-die
voltage, continuous material memory or nonbinary silicon operator is asserted.
Physical R08 K06 is source-checked without using a software ADC substitute.
Historical sources are not modified; generated evidence stays under --out.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
import closed_native_cycle as cycle
import batch_bridge as base
import connector
HXROOT=connector.HX89.parents[1]
GAS=HXROOT/'bin/hx89-gas'
FIVE=HXROOT/'polyforms/five_dimensional.hx'
PHASE=HXROOT/'polyforms/phase_torus.hx'
SNAP=HXROOT/'polyforms/snapshot.hx'
GAS_RE=re.compile(r'^GAS size=(\d+)x(\d+) steps=(\d+) mass=(\d+) px=(-?\d+) py=(-?\d+) collisions=(\d+) final=([0-9a-f]{16}) reverse=PASS$',re.M)
HALT=re.compile(r'^HX89 halt steps=\d+ heads=\d+ nodes=\d+ stack=\d+ hash=([0-9a-f]{16})$',re.M)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def exec_real(command,cwd,limit=12):
    p=subprocess.run([str(x) for x in command],cwd=cwd,capture_output=True,text=True,timeout=limit)
    if p.returncode:
        raise RuntimeError(f'Real executable failed ({p.returncode}) command={list(map(str,command))!r} cwd={str(cwd)!r} stdout={p.stdout[-400:]!r} stderr={p.stderr[-400:]!r}')
    return p.stdout

def gas_model_to_hx89(outdir,cycle_number,observed,actual):
    """Execute original C reversible lattice model, then original HX89 Polyform.

    Independently compare its raw image pixels, its emitted Polyform output and
    the C engine's conservation/reversal certificate. Not a material measurement.
    """
    w,h=16,16
    steps=4+actual['q']%7
    seed=(observed ^ (actual['q'] << 27) ^ (actual['fitness'] << 41) ^ (cycle_number+1)) & ((1<<64)-1)
    if not seed:seed=1
    prefix=outdir/f'round_{cycle_number:03d}'
    img=prefix.with_suffix('.gas.pgm')
    poly=prefix.with_suffix('.gas.hx')
    gas_stdout=exec_real([GAS,w,h,steps,seed,img,poly],HXROOT)
    prefix.with_suffix('.gas.stdout.txt').write_text(gas_stdout)
    cert=GAS_RE.search(gas_stdout)
    if not cert or (int(cert.group(1)),int(cert.group(2)),int(cert.group(3)))!=(w,h,steps):
        raise RuntimeError('Gas physics-model conservation/reversal certificate absent')
    # Check from the actual image, not the generator's internal state.
    raw=img.read_bytes()
    header=f'P5\n{w} {h}\n255\n'.encode()
    if not raw.startswith(header) or len(raw)!=len(header)+w*h:raise RuntimeError('Gas image format or size invalid')
    pixels=raw[len(header):]
    if any(v%42 for v in pixels):raise RuntimeError('Gas PGM occupancy invalid')
    density=[(sum(pixels[y*w+x]//42 for y in range(h))+h//2)//h for x in range(w)]
    expected=''.join(str(v) for v in density)
    machine_out=exec_real([connector.HX89,poly,1,128],HXROOT)
    prefix.with_suffix('.gas.hx89.stdout.txt').write_text(machine_out)
    if not HALT.search(machine_out):raise RuntimeError('Generated gas Polyform did not halt')
    if not any(line==expected for line in machine_out.splitlines()):
        raise RuntimeError('Executed HX89 gas output mismatches actual gas PGM columns')
    return {'seed':seed,'steps':steps,'mass':int(cert.group(4)),'collisions':int(cert.group(7)),
            'model_state_final_hash':cert.group(8),'reverse_verified_by_c_model':True,
            'hexworld_profile':expected,'image_sha256':sha(img),'polyform_sha256':sha(poly),
            'gas_stdout_sha256':sha(prefix.with_suffix('.gas.stdout.txt')),
            'executed_hx89_gas_stdout_sha256':sha(prefix.with_suffix('.gas.hx89.stdout.txt'))}

def initial_lateral_real_paths(out):
    five=exec_real([connector.HX89,FIVE,1,100],HXROOT)
    phase=exec_real([connector.HX89,'--phase-forward',PHASE,1,20],HXROOT)
    native=connector.native_trace()
    save_dir=out/'snapshot_isolated'
    save_dir.mkdir(exist_ok=True)
    saved=exec_real([connector.HX89,SNAP,12345,100],save_dir)
    state=save_dir/'hx89.state'
    if not state.is_file():raise RuntimeError('HX89 SAVE produced no persistent state')
    resumed=exec_real([connector.HX89,'--resume',state,100],save_dir)
    (out/'hx89_five_dimensional.stdout.txt').write_text(five)
    (out/'hx89_phase.stdout.txt').write_text(phase)
    (out/'hx89_native_accel.stdout.txt').write_text(native['stdout'])
    (out/'hx89_snapshot.stdout.txt').write_text(saved)
    (out/'hx89_resume.stdout.txt').write_text(resumed)
    if 'ZWVY' not in five or 'PHASE old=7' not in phase or not all(HALT.search(v) for v in [five,phase,saved,resumed]):
        raise RuntimeError('A lateral HX89 native path failed to execute as expected')
    return {'five_dimensional_hash':sha(out/'hx89_five_dimensional.stdout.txt'),
            'phase_hash':sha(out/'hx89_phase.stdout.txt'),'native_ir':native['native_ir'],
            'native_result':native['native_result'],'native_code_hash':native['code_bytes_hash'],
            'saved_snapshot_sha256':sha(state),'saved_stdout_sha256':sha(out/'hx89_snapshot.stdout.txt'),
            'resumed_stdout_sha256':sha(out/'hx89_resume.stdout.txt')}

def next_control(hx,gas,base_work):
    rotate,work=cycle.next_command(hx,base_work)
    # Input here comes from bytes ACTUALLY emitted by the executed HX89 machine
    # for the reversible lattice-model result; no shadow prediction is accepted.
    profile=gas['hexworld_profile']
    if len(profile)!=16 or any(c not in '0123456' for c in profile):
        raise RuntimeError('Invalid executed HX89 model-profile state')
    return {'rotate':(rotate+sum(map(int,profile)))%4,
            'work':base_work+((work-base_work+sum((i+1)*int(x) for i,x in enumerate(profile)))%3)}

def run(rounds,base_work,out):
    # The HX89 snapshot is resumed with a child cwd. Normalize once so its
    # state path always names the original saved file, including for CLI-relative --out.
    out=Path(out).resolve()
    if not 4<=rounds<=64 or not 1<=base_work<=20:raise ValueError('Bounded rounds/work violation')
    if out.exists() and any(out.iterdir()):raise RuntimeError('Refusing to overwrite any preexisting run')
    out.mkdir(parents=True,exist_ok=True)
    history=base.check_master()
    circuit=connector.k06_contract()
    hx_lateral=initial_lateral_real_paths(out)
    feedback=[]
    cmd={'rotate':0,'work':base_work}
    changed=0
    for idx in range(rounds):
        pfx=out/f'round_{idx:03d}'
        p=subprocess.run([str(base.EXEC),'--rounds','1','--work',str(cmd['work']),
                          '--rotate',str(cmd['rotate']),'--pin'],capture_output=True,text=True,timeout=25)
        native=pfx.with_suffix('.native.jsonl')
        native.write_text(p.stdout)
        pfx.with_suffix('.native.stderr.txt').write_text(p.stderr)
        if p.returncode:raise RuntimeError(f'Native CPU intervention failed in cycle {idx}: {p.stderr[-300:]}')
        header,trials=cycle.decode_real_native(p.stdout,cmd['rotate'],cmd['work'])
        observed=sum(t['post_ticks']+t['stimulus_ticks'] for t in trials)
        target=observed%25
        actual=connector.hx_execute(connector.Q2PROGRAM,('--target-q',str(target)))
        pfx.with_suffix('.q2.hx89.stdout.txt').write_text(actual['stdout'])
        q=cycle.decode_real_hx89(actual['stdout'],target)
        gas=gas_model_to_hx89(out,idx,observed,q)
        upcoming=next_control(q,gas,base_work)
        changed+=upcoming!=cmd
        feedback.append({'cycle':idx,'requested_cpu_control':dict(cmd),
             'observed_cpu_modes_in_order':[t['mode'] for t in trials],
             'processor_id':header['cpu'],'cpu_instruction_tsc_total':observed,
             'native_trial_sha256':sha(native),'hx89_q2_program_sha256':actual['program_sha256'],
             'executed_hx89_q2':q,'hx89_q2_stdout_sha256':sha(pfx.with_suffix('.q2.hx89.stdout.txt')),
             'executed_gas_model_and_hx89':gas,'next_cpu_control':upcoming})
        cmd=upcoming
    if changed==0:raise RuntimeError('No genuinely changed CPU commands')
    for a,b in zip(feedback,feedback[1:]):
        if a['next_cpu_control']!=b['requested_cpu_control']:
            raise RuntimeError('Broken cycle causal controller linkage')
    result={'schema':'VOID_HX89_CPU_Q2_GAS_HX89_CPU_CLOSED_V2',
      'physical_nonbinary_material_computation_verified':False,
      'actual_hardware_weak_inversion_control_verified':False,
      'digital_lattice_model_not_material_gas':True,
      'classification':'ACTUAL_CPU_INSTRUCTIONS_AND_HX89_EXECUTION_WITH_DIGITAL_GAS_MODEL',
      'utc':datetime.now(timezone.utc).isoformat(),'cycles':rounds,'native_trials':rounds*4,
      'changed_cpu_commands':changed,'historical_116':history,
      'k06_specification_not_physical_attachment':circuit,'hx89_lateral_executions':hx_lateral,
      'native_executable_sha256':sha(base.EXEC),'hx89_executable_sha256':sha(connector.HX89),
      'gas_executable_sha256':sha(GAS),'source_sha256':sha(__file__),'feedback':feedback}
    dest=out/'FULL_STACK_EXECUTION.json'
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--rounds',type=int,default=16)
    p.add_argument('--base-work',type=int,default=4)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    r=run(a.rounds,a.base_work,a.out)
    print(json.dumps({'status':'EXECUTED','cycles':r['cycles'],'native_trials':r['native_trials'],
          'changed_cpu_commands':r['changed_cpu_commands'],
          'physical_nonbinary_material_computation_verified':False,
          'record':str(a.out/'FULL_STACK_EXECUTION.json')},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}),file=sys.stderr)
        sys.exit(1)
