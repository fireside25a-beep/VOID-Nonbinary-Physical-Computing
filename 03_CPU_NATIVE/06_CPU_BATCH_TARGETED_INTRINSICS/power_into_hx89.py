#!/usr/bin/env python3
"""Actual CPU busy/idle crossover -> HX89 Q² -> real next native CPU command.

No independent die-temperature measurement: this remains an unproved thermal/power
mechanism and is never called a verified nonbinary material operator.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import power_causal as p
import closed_native_cycle as native
import batch_bridge as base
import connector

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(out:Path,count:int=80):
    out=out.resolve()
    if out.exists() and any(out.iterdir()):raise RuntimeError('Refuse overwrite of real power evidence')
    out.mkdir(parents=True,exist_ok=True)
    # Existing CPU executable is run first; no disconnected synthetic controller.
    baseline=subprocess.run([str(base.EXEC),'--rounds','1','--work','4','--rotate','0','--pin'],capture_output=True,text=True,timeout=25)
    (out/'initial_cpu.jsonl').write_text(baseline.stdout)
    if baseline.returncode:raise RuntimeError('Initial CPU batch failed: '+baseline.stderr[-200:])
    native.decode_real_native(baseline.stdout,0,4)
    power_source,power_binary=p.compile_native()
    physical=p.run_probe(out/'intervention',count)
    measured=physical['busy_minus_idle_median_tsc']
    # State injection carries an actual observed host timing measurement; not a
    # fabricated direct transistor current measurement. Models/ISA remain digital.
    target=int(abs(measured))%25
    response=connector.hx_execute(connector.Q2PROGRAM,('--target-q',str(target)))
    (out/'measured_hx89.stdout.txt').write_text(response['stdout'])
    hx=native.decode_real_hx89(response['stdout'],target)
    rot,work=native.next_command(hx,4)
    next_cpu=subprocess.run([str(base.EXEC),'--rounds','1','--work',str(work),'--rotate',str(rot),'--pin'],capture_output=True,text=True,timeout=25)
    (out/'next_cpu.jsonl').write_text(next_cpu.stdout)
    if next_cpu.returncode:raise RuntimeError('Measured effect did not reach next CPU command')
    native.decode_real_native(next_cpu.stdout,rot,work)
    result={'schema':'VOID_POWER_TIMING_TO_HX89_TO_CPU_ACTUAL_V1',
            'physical_thermodynamic_response_verified':False,
            'not_an_independent_temperature_or_power_measurement':True,
            'actual_native_crossover':physical,'hx89_q2_execution':hx,
            'resulting_next_cpu_command':{'rotate':rot,'work':work},
            'initial_cpu_sha256':sha(out/'initial_cpu.jsonl'),
            'hx89_stdout_sha256':sha(out/'measured_hx89.stdout.txt'),
            'next_cpu_sha256':sha(out/'next_cpu.jsonl'),
            'source_sha256':sha(__file__),'source_power_sha256':power_source,
            'native_power_binary_sha256':power_binary,
            'existing_native_binary_sha256':sha(base.EXEC),
            'existing_hx89_binary_sha256':sha(connector.HX89),
            'hx89_q2_program_sha256':sha(connector.Q2PROGRAM)}
    (out/'POWER_HX89_EXECUTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result

def verify(out:Path):
    r=json.loads((out/'POWER_HX89_EXECUTION.json').read_text())
    if r['schema']!='VOID_POWER_TIMING_TO_HX89_TO_CPU_ACTUAL_V1' or r['physical_thermodynamic_response_verified'] is not False:
        raise ValueError('Invalid evidence schema or unproved claim')
    if r['source_sha256']!=sha(__file__) or r['source_power_sha256']!=sha(p.SOURCE) or r['native_power_binary_sha256']!=sha(p.EXEC):
        raise ValueError('Measured power-source/binary identity mismatch')
    if r['existing_native_binary_sha256']!=sha(base.EXEC) or r['existing_hx89_binary_sha256']!=sha(connector.HX89):
        raise ValueError('Original machine binaries no longer match')
    if r['hx89_q2_program_sha256']!=sha(connector.Q2PROGRAM):raise ValueError('HX89 Q² source mutated')
    x=r['actual_native_crossover']
    obs=p.inspect(out/'intervention.power.csv',x['trials'])
    if any(obs[k]!=v for k,v in x.items() if k in obs):raise ValueError('Real timed values mismatch recorded result')
    for path,key in [('intervention.power.stdout.txt','stdout_sha256'),('intervention.power.stderr.txt','stderr_sha256')]:
        if sha(out/path)!=x[key]:raise ValueError('Candidate subprocess evidence tampered')
    for path,key in [('initial_cpu.jsonl','initial_cpu_sha256'),('measured_hx89.stdout.txt','hx89_stdout_sha256'),('next_cpu.jsonl','next_cpu_sha256')]:
        if sha(out/path)!=r[key]:raise ValueError('Subsequent genuine machine output tampered')
    native.decode_real_native((out/'initial_cpu.jsonl').read_text(),0,4)
    hx=native.decode_real_hx89((out/'measured_hx89.stdout.txt').read_text(),int(abs(obs['busy_minus_idle_median_tsc']))%25)
    if hx!=r['hx89_q2_execution']:raise ValueError('HX89 did not derive from actual measurement')
    rot,work=native.next_command(hx,4)
    if r['resulting_next_cpu_command']!={'rotate':rot,'work':work}:raise ValueError('HX89 next-CPU linkage broken')
    native.decode_real_native((out/'next_cpu.jsonl').read_text(),rot,work)
    return {'power_crossover_trials_verified':obs['trials'],'median_busy_minus_idle_tsc':obs['busy_minus_idle_median_tsc'],
            'HX89_feedback_to_next_CPU':'VERIFIED_NATIVE_DIGITAL_FEEDBACK',
            'thermal_computation':'NOT_VERIFIED'}

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--trials',type=int,default=80);args=a.parse_args()
    r=run(args.out,args.trials);print(json.dumps({'record':str(args.out/'POWER_HX89_EXECUTION.json'),**verify(args.out)},indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'status':'FAIL','error':str(e)}),file=sys.stderr);sys.exit(1)
