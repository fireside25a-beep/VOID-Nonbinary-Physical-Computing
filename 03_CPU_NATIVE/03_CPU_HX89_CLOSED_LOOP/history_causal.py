"""Real CPU three-intensity history observations, for original HX89 whole-machine cycle.

Experiment randomization uses deterministic bookkeeping; physical samples are only
those acquired by native RDTSCP/CLOCK_MONOTONIC_RAW. Neither silicon temperature
nor analog current is directly sampled by this experiment.
"""
from __future__ import annotations
import csv
import hashlib
import json
import statistics
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'history_response.c'
EXEC=HERE/'history_response'
PERMS=((0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0))
MASK=(1<<64)-1

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def compile_native():
    r=subprocess.run(['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-o',str(EXEC),str(SOURCE)],capture_output=True,text=True,timeout=30)
    if r.returncode:raise RuntimeError('History probe compile failed: '+r.stderr)
    return {'source_sha256':sha(SOURCE),'binary_sha256':sha(EXEC)}

def shuffled_schedule(seed,blocks):
    state=seed
    def next_rand():
        nonlocal state
        state ^= state>>12
        state ^= (state<<25)&MASK
        state ^= state>>27
        state &= MASK
        return (state*2685821657736338717)&MASK
    for _ in range(blocks):
        order=list(range(6))
        for i in range(5,0,-1):
            j=next_rand()%(i+1)
            order[i],order[j]=order[j],order[i]
        yield [level for pos in order for level in PERMS[pos]]

def inspect(path:Path,blocks:int,seed:int)->dict:
    path=Path(path)
    with path.open(newline='') as f:
        reader=csv.DictReader(f)
        names={'trial','block','position','intensity','previous_intensity','pre_tsc','post_tsc','pre_ns','post_ns','stimulus_ns','active_ns','aux_pre_start','aux_pre_end','aux_post_start','aux_post_end','pinned_cpu','seed'}
        if set(reader.fieldnames or [])!=names:raise ValueError('History source field schema changed')
        rows=list(reader)
    if len(rows)!=blocks*18:raise ValueError('Missing real history observations')
    counts=[0]*3; effects=[[],[],[]]; pinned=None;previous=-1
    transition=[[0]*3 for _ in range(3)]
    active_ns=[[],[],[]]
    schedules=list(shuffled_schedule(seed,blocks))
    for i,row in enumerate(rows):
        try: a={k:int(v) for k,v in row.items()}
        except (ValueError,TypeError) as e:raise ValueError('Invalid native history data') from e
        expected=schedules[i//18][i%18]
        if (a['trial'],a['block'],a['position'],a['intensity'],a['previous_intensity'],a['seed'])!=(i,i//18,i%18,expected,previous,seed):
            raise ValueError('Native randomized history order, seed or predecessor mismatch')
        if min(a[k] for k in ('pre_tsc','post_tsc','pre_ns','post_ns','stimulus_ns'))<=0:
            raise ValueError('Nonpositive real hardware measurement')
        aux={a[k] for k in ('aux_pre_start','aux_pre_end','aux_post_start','aux_post_end')}
        if len(aux)!=1:raise ValueError('Real CPU migrated within history measurement')
        if pinned is None:pinned=a['pinned_cpu']
        if pinned!=a['pinned_cpu']:raise ValueError('CPU pin changed across experiment')
        if a['active_ns']<0 or a['active_ns']>a['stimulus_ns'] or a['stimulus_ns']<2000000 or a['stimulus_ns']>100000000:
            raise ValueError('Incorrect stimulus timing')
        if expected==0 and a['active_ns']!=0 or expected>0 and a['active_ns']==0:
            raise ValueError('Native intensity did not match executed work')
        if expected==1 and a['active_ns']>a['stimulus_ns']*0.8:
            raise ValueError('Low intensity did not leave idle period')
        counts[expected]+=1
        effects[expected].append(a['post_tsc']-a['pre_tsc'])
        active_ns[expected].append(a['active_ns'])
        if previous>=0:transition[previous][expected]+=1
        previous=expected
    if counts!=[blocks*6]*3:raise ValueError('Unbalanced native intensity exposures')
    med=[statistics.median(v) for v in effects]
    contrast=med[2]-med[0]
    # These are observed timing effects only. No sign/magnitude is pre-labelled as PASS.
    return {'schema':'VOID_REAL_CPU_THREE_INTENSITY_HISTORY_V1','blocks':blocks,'trials':len(rows),
            'seed':seed,'pinned_cpu':pinned,'intensity_counts':counts,
            'median_post_minus_pre_tsc_by_intensity':med,
            'high_minus_idle_median_delta_tsc':contrast,
            'active_duration_median_ns_by_intensity':[statistics.median(x) for x in active_ns],
            'transition_counts':transition,'raw_csv_sha256':sha(path),
            'direct_temperature_or_current_observed':False,
            'physical_nonbinary_thermodynamic_operator_verified':False}

def run_probe(prefix:Path,seed:int,blocks:int=1):
    """Acquire authentic CPU evidence, preserving scheduler-contaminated attempts.

    Each retry runs the native program again. A rejected CSV remains immutable,
    with its failure reason and hash in the accepted execution receipt. No sample
    is changed, recalculated, or presented as a successful observation.
    """
    if not 1<=blocks<=24 or not 0<seed<=MASK:raise ValueError('Invalid randomized native probe parameters')
    prefix=Path(prefix)
    csv_path=prefix.with_suffix('.history.csv')
    if csv_path.exists():raise FileExistsError('Refuse overwrite of real history trace')
    compile_native()
    rejected=[]
    # Bounded actual fresh acquisitions. No repeated use of a failed trace.
    for attempt in range(4):
        if attempt:
            if csv_path.exists():raise FileExistsError('Previous attempt not quarantined')
        p=subprocess.run([str(EXEC),str(blocks),str(seed),str(csv_path)],capture_output=True,text=True,timeout=max(30,blocks*2))
        stdout_path=prefix.with_suffix('.history.stdout.txt')
        stderr_path=prefix.with_suffix('.history.stderr.txt')
        if stdout_path.exists() or stderr_path.exists():
            raise FileExistsError('Refuse overwrite of native acquisition outputs')
        stdout_path.write_text(p.stdout)
        stderr_path.write_text(p.stderr)
        if p.returncode:
            raise RuntimeError(f'Native three-intensity probe failed ({p.returncode}): {p.stderr[-300:]}')
        try:
            result=inspect(csv_path,blocks,seed)
        except ValueError as error:
            # Only scheduling-contaminated low-intensity durations qualify for
            # fresh acquisition. All other measurement failures are terminal.
            if str(error)!='Low intensity did not leave idle period':raise
            rej=prefix.with_suffix(f'.history.rejected_{attempt:02d}.csv')
            rejs=prefix.with_suffix(f'.history.rejected_{attempt:02d}.stdout.txt')
            reje=prefix.with_suffix(f'.history.rejected_{attempt:02d}.stderr.txt')
            for dest in (rej,rejs,reje):
                if dest.exists():raise FileExistsError('Preserved failure already exists')
            csv_path.rename(rej);stdout_path.rename(rejs);stderr_path.rename(reje)
            rejected.append({'attempt':attempt,'error':str(error),
                             'raw_csv_sha256':sha(rej),'stdout_sha256':sha(rejs),
                             'stderr_sha256':sha(reje)})
            if attempt==3:
                raise RuntimeError('Four native scheduling-contaminated acquisitions; rejecting incomplete cycle') from error
            continue
        result.update({'source_sha256':sha(SOURCE),'binary_sha256':sha(EXEC),
                       'stdout_sha256':sha(stdout_path),'stderr_sha256':sha(stderr_path)})
        if rejected:result['scheduling_rejected_attempts']=rejected
        return result
    raise RuntimeError('No valid real native acquisition')

def with_observation(command:dict,observation:dict,base_work:int)->dict:
    if observation.get('schema')!='VOID_REAL_CPU_THREE_INTENSITY_HISTORY_V1' or observation.get('physical_nonbinary_thermodynamic_operator_verified') is not False:
        raise ValueError('No legitimate real CPU history evidence')
    c=observation['high_minus_idle_median_delta_tsc']
    if not isinstance(c,(int,float)) or abs(c)>10**10:raise ValueError('Invalid history contrast')
    # Command modulation is a DIGITAL controller based on real executed native observation.
    # It does NOT claim continuous physical nonbinary charge/state computation.
    t=int(abs(c))
    return {'rotate':(command['rotate']+(t%4))%4,
            'work':base_work+((command['work']-base_work+(t//4)%3)%3)}
