#!/usr/bin/env python3
"""CPU material-history candidate in the ACTUAL VOID/HX89 feedback chain.

Runs three hardware workloads on one pinned CPU, waits in a fixed hold interval,
and times an identical real computation pinned to another CPU. Records original
observations and independently checks counterbalanced schedules. Next CPU
commands derive from an actually executed HX89 Q² result. This experiment does
NOT access raw silicon gate voltage, thermometers, or physical analog memory.
"""
import argparse, csv, hashlib, json, os, statistics, subprocess, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'cpu_cross_core_history.c'
MASK=(1<<64)-1
PERMS=((0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0))
sys.path.insert(0,str(HERE))
import closed_native_cycle as cycle
import batch_bridge as base
import connector
import full_stack_cycle as full_machine
import verify_full_stack as full_verify

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def random_steps(initial):
    v=initial
    while True:
        v^=v>>12;v^=(v<<25)&MASK;v^=v>>27
        v&=MASK
        yield (v*2685821657736338717)&MASK

def expected_order(seed,blocks):
    rg=random_steps(seed)
    for _ in range(blocks):
        order=list(range(6))
        for i in range(5,0,-1):
            j=next(rg)%(i+1)
            order[i],order[j]=order[j],order[i]
        yield [q for p in order for q in PERMS[p]]

FIELDS=('trial','block','position','intensity','heater_cpu','reader_cpu','heat_ns','hold_ns','read_ns','read_tsc','aux','seed')
def inspect_rows(rows,blocks,seed,heater,reader,heat_ms,hold_ms):
    if len(rows)!=18*blocks:raise ValueError('missing or added native measurements')
    schedule=[x for group in expected_order(seed,blocks) for x in group]
    results={0:[],1:[],2:[]}
    perblock=[]
    for i,row in enumerate(rows):
        try:r={k:int(row[k]) for k in FIELDS}
        except (TypeError,ValueError,KeyError) as e:raise ValueError('invalid native measurement') from e
        if set(row)!=set(FIELDS):raise ValueError('unexpected column')
        if (r['trial'],r['block'],r['position'],r['intensity'])!=(i,i//18,i%18,schedule[i]):
            raise ValueError('executed counterbalanced schedule mismatch')
        if (r['heater_cpu'],r['reader_cpu'],r['seed'],r['hold_ns'])!=(heater,reader,seed,hold_ms*1000000):
            raise ValueError('source configuration or hold changed')
        if r['heat_ns']<heat_ms*1000000 or r['heat_ns']>heat_ms*1000000*3:
            raise ValueError('stimulus not acquired at requested wall-time')
        if r['read_ns']<=0 or r['read_tsc']<=0 or r['aux']<0:
            raise ValueError('non-positive or invalid hardware observation')
        results[r['intensity']].append(r['read_ns'])
    for offset in range(0,len(rows),3):
        v={int(row['intensity']):int(row['read_ns']) for row in rows[offset:offset+3]}
        if len(v)!=3:raise ValueError('incomplete three-state crossover')
        perblock.append(v[2]-v[0])
    med=[statistics.median(results[i]) for i in (0,1,2)]
    return {'trials':len(rows),'intensities':{str(k):len(v) for k,v in results.items()},
            'read_ns_median_by_level':med,
            'high_minus_idle_median_ns':med[2]-med[0],
            'within_triplet_high_minus_idle_ns':perblock,
            'triplet_positive':sum(z>0 for z in perblock),
            'triplet_negative':sum(z<0 for z in perblock),
            'triplet_zero':sum(z==0 for z in perblock),
            'reader_cpu':reader,'heater_cpu':heater,'heat_ms':heat_ms,'hold_ms':hold_ms,
            'physical_multilevel_memory_verified':False,
            'analog_current_or_temperature_measured':False,
            'interpretation':'REAL_CROSS_CPU_TIMING_NOT_DIRECT_ANALOG_STATE'}

def read_check(csvpath,blocks,seed,heater,reader,heat,hold):
    with csvpath.open(newline='') as f:
        rr=csv.DictReader(f)
        if rr.fieldnames!=list(FIELDS):raise ValueError('CSV header changed')
        rows=list(rr)
    return inspect_rows(rows,blocks,seed,heater,reader,heat,hold)

def run(out,blocks=2,heat_ms=20,seed=0x91ac5fee):
    out=Path(out).resolve()
    if out.exists():raise FileExistsError('never overwrite evidence')
    out.mkdir(parents=True)
    cpus=sorted(os.sched_getaffinity(0))
    if len(cpus)<2:raise RuntimeError('Need two different available CPU affinities for independent observer')
    heater,reader=cpus[0],cpus[-1]
    binary=out/'cpu_cross_core_history'
    cmd=['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-o',str(binary),str(SOURCE)]
    compilelog=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    (out/'compile.txt').write_text(compilelog.stdout+compilelog.stderr)
    if compilelog.returncode:raise RuntimeError('real native compiler refused experiment')
    base_check=base.check_master()
    # The complete ORIGINAL HX89 5D/Q²/reversible lattice -> next CPU cycle is
    # executed first; the physical-state candidate extends THAT same controller.
    complete_path=out/'original_full_stack'
    full_result=full_machine.run(4,4,complete_path,cache_probe=True,history_probe=True)
    full_verified=full_verify.assert_verified(complete_path)
    inherited_command=full_result['feedback'][-1]['next_cpu_control']
    original_full_sha=sha(complete_path/'FULL_STACK_EXECUTION.json')
    seed=(seed ^ int(original_full_sha[:16],16)) & MASK
    if not seed:seed=1
    initial=subprocess.run([str(base.EXEC),'--rounds','1','--work',str(inherited_command['work']),
                           '--rotate',str(inherited_command['rotate']),'--pin'],capture_output=True,text=True,timeout=25)
    (out/'initial_cpu.jsonl').write_text(initial.stdout)
    (out/'initial_cpu.stderr').write_text(initial.stderr)
    if initial.returncode:raise RuntimeError('initial real CPU batch failed')
    cycle.decode_real_native(initial.stdout,inherited_command['rotate'],inherited_command['work'])
    experiments=[]
    rejected_acquisitions=[]
    # Both hold times are fixed in advance. Retry only an unambiguously invalid
    # scheduler-overshoot acquisition, never an unexpected sign or low effect size.
    # Every rejected real CSV and process transcript is preserved unmodified.
    for delay in (5,50):
        for attempt in range(3):
            csvpath=out/f'hold_{delay}ms.csv'
            stdout_path=out/f'hold_{delay}ms.stdout.txt'
            stderr_path=out/f'hold_{delay}ms.stderr.txt'
            if any(path.exists() for path in (csvpath,stdout_path,stderr_path)):
                raise FileExistsError('Refusing to overwrite any measured CPU acquisition')
            proc=subprocess.run([str(binary),str(blocks),str(seed),str(heater),str(reader),
                                 str(heat_ms),str(delay),str(csvpath)],
                    capture_output=True,text=True,
                    timeout=max(40,blocks*18*(heat_ms+delay+100)//1000+20))
            stdout_path.write_text(proc.stdout)
            stderr_path.write_text(proc.stderr)
            if proc.returncode:
                raise RuntimeError(f'Native cross-core probe failed hold={delay} '
                                   f'return={proc.returncode}: {proc.stderr[-400:]}')
            try:
                row=read_check(csvpath,blocks,seed,heater,reader,heat_ms,delay)
            except ValueError as exc:
                if str(exc)!='stimulus not acquired at requested wall-time' or attempt>=2:
                    raise
                preserved={}
                for original in (csvpath,stdout_path,stderr_path):
                    newpath=out/f'hold_{delay}ms.rejected_{attempt:02d}.{original.name.split(".",1)[-1]}'
                    if newpath.exists():raise FileExistsError('Refuse overwrite of rejected acquisition')
                    original.rename(newpath)
                    preserved[newpath.name]=sha(newpath)
                rejected_acquisitions.append({'hold_ms':delay,'attempt':attempt,
                       'reason':str(exc),'unmodified_rejected_file_sha256':preserved})
                continue
            row.update({'csv':csvpath.name,'csv_sha256':sha(csvpath),
                'stdout_sha256':sha(stdout_path),'stderr_sha256':sha(stderr_path)})
            experiments.append(row)
            break
        else:
            raise RuntimeError('Real CPU acquisition exhaustion, no claim of PASS')
    # A measured CPU timing result, NOT synthetic voltage, drives original HX89.
    reading=int(experiments[0]['high_minus_idle_median_ns'])
    target=abs(reading)%25
    raw=connector.hx_execute(connector.Q2PROGRAM,('--target-q',str(target)))
    (out/'hx89_actual.stdout.txt').write_text(raw['stdout'])
    state=cycle.decode_real_hx89(raw['stdout'],target)
    rotate,work=cycle.next_command(state,4)
    follow=subprocess.run([str(base.EXEC),'--rounds','1','--work',str(work),'--rotate',str(rotate),'--pin'],
                          capture_output=True,text=True,timeout=25)
    (out/'next_cpu.jsonl').write_text(follow.stdout)
    (out/'next_cpu.stderr').write_text(follow.stderr)
    if follow.returncode:raise RuntimeError('next real CPU command failed')
    cycle.decode_real_native(follow.stdout,rotate,work)
    record={'schema':'VOID_CPU_CROSS_CORE_HISTORY_HX89_FEEDBACK_V1','source_sha256':sha(SOURCE),
         'binary_sha256':sha(binary),'original_cpu_binary_sha256':sha(base.EXEC),
         'original_hx89_binary_sha256':sha(connector.HX89),
         'q2_program_sha256':sha(connector.Q2PROGRAM),'original_master_integrity':base_check,
         'complete_original_machine_run_sha256':original_full_sha,
         'complete_original_machine_verification':full_verified,
         'inherited_actual_hx89_command':inherited_command,
         'source_script_sha256':sha(__file__),
         'scheduler_rejected_acquisitions':rejected_acquisitions,
         'seed':seed,'blocks':blocks,'heater':heater,'reader':reader,'heat_ms':heat_ms,
         'experiments':experiments,'executed_hx89_target':target,'executed_hx89_state':state,
         'actual_next_cpu_command':{'rotate':rotate,'work':work},
         'actual_initial_cpu_sha256':sha(out/'initial_cpu.jsonl'),
         'actual_hx89_stdout_sha256':sha(out/'hx89_actual.stdout.txt'),
         'actual_next_cpu_sha256':sha(out/'next_cpu.jsonl'),
         'verified_material_multilevel_memory':False,
         'verified_cpu_subthreshold_gate_control':False,
         'independently_measured_cpu_thermodynamic_calculation':False}
    (out/'result.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    return record

def verify(out):
    out=Path(out);r=json.loads((out/'result.json').read_text())
    if r['schema']!='VOID_CPU_CROSS_CORE_HISTORY_HX89_FEEDBACK_V1':raise ValueError('unrecognized record schema')
    if any(r[k] for k in ('verified_material_multilevel_memory','verified_cpu_subthreshold_gate_control',
                           'independently_measured_cpu_thermodynamic_calculation')):
        raise ValueError('unsupported physical claim')
    if r['source_script_sha256']!=sha(__file__):raise ValueError('source script changed since execution')
    whole=out/'original_full_stack'
    if sha(whole/'FULL_STACK_EXECUTION.json')!=r['complete_original_machine_run_sha256']:
        raise ValueError('whole-machine-to-material path interrupted')
    if full_verify.assert_verified(whole)!=r['complete_original_machine_verification']:
        raise ValueError('whole-machine actual executed outcomes corrupted')
    expected_cmd=json.loads((whole/'FULL_STACK_EXECUTION.json').read_text())['feedback'][-1]['next_cpu_control']
    if expected_cmd!=r['inherited_actual_hx89_command']:
        raise ValueError('material probe initial input disconnected from HX89')
    if r['source_sha256']!=sha(SOURCE) or r['binary_sha256']!=sha(out/'cpu_cross_core_history'):
        raise ValueError('experiment source or native executable altered')
    if r['original_cpu_binary_sha256']!=sha(base.EXEC) or r['original_hx89_binary_sha256']!=sha(connector.HX89):raise ValueError('native core changed')
    for rejected in r.get('scheduler_rejected_acquisitions',[]):
        if rejected['reason']!='stimulus not acquired at requested wall-time':
            raise ValueError('unapproved rejected-data selection reason')
        for name,h in rejected['unmodified_rejected_file_sha256'].items():
            if sha(out/name)!=h:raise ValueError('original rejected CPU acquisition modified')
    for item in r['experiments']:
        raw=out/item['csv']
        if sha(raw)!=item['csv_sha256']:raise ValueError('native physical observation altered')
        actual=read_check(raw,r['blocks'],r['seed'],r['heater'],r['reader'],r['heat_ms'],item['hold_ms'])
        if any(item[k]!=v for k,v in actual.items()):raise ValueError('native observation statistics corrupted')
        for suffix,key in [('stdout.txt','stdout_sha256'),('stderr.txt','stderr_sha256')]:
            if sha(out/f"hold_{item['hold_ms']}ms.{suffix}")!=item[key]:raise ValueError('native subprocess log tampered')
    cycle.decode_real_native((out/'initial_cpu.jsonl').read_text(),expected_cmd['rotate'],expected_cmd['work'])
    target=abs(int(r['experiments'][0]['high_minus_idle_median_ns']))%25
    if target!=r['executed_hx89_target']:raise ValueError('HX89 target disconnected from physical observation')
    if sha(out/'hx89_actual.stdout.txt')!=r['actual_hx89_stdout_sha256']:raise ValueError('HX89 trace tampered')
    hx=cycle.decode_real_hx89((out/'hx89_actual.stdout.txt').read_text(),target)
    if hx!=r['executed_hx89_state']:raise ValueError('HX89 state mismatch')
    rot,work=cycle.next_command(hx,4)
    if r['actual_next_cpu_command']!={'rotate':rot,'work':work}:raise ValueError('next command linkage changed')
    if sha(out/'next_cpu.jsonl')!=r['actual_next_cpu_sha256']:raise ValueError('next CPU evidence tampered')
    cycle.decode_real_native((out/'next_cpu.jsonl').read_text(),rot,work)
    return {'observations_verified':sum(e['trials'] for e in r['experiments']),
            'HX89_native_feedback':'PASS','material_nonbinary_gate':'NOT_ESTABLISHED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--blocks',type=int,default=2);a=ap.parse_args()
    try:
        r=run(a.out,blocks=a.blocks)
        print(json.dumps(verify(a.out),sort_keys=True))
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}),file=sys.stderr);sys.exit(1)
