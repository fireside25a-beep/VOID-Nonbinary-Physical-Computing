#!/usr/bin/env python3
"""Actual CPU cache intervention measurement and provenance for HX89's live cycle.

Measures CLFLUSH-caused line eviction relative to warm loads. This is a physical
cache access effect manifested through digital CPU interfaces, *not* proof of
analog/thermal or fundamentally nonbinary computation. No measurement is mocked.
"""
from __future__ import annotations
import csv,hashlib,json,statistics,subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'cache_causality.c'
EXEC=HERE/'cache_causality'

def sha(p:Path)->str:
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<18),b''):h.update(chunk)
    return h.hexdigest()

def compile_native()->dict:
    # Only compile actual source; reject missing compiler or compiler failure.
    p=subprocess.run(['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror',
                      '-o',str(EXEC),str(SOURCE)],capture_output=True,text=True,timeout=40)
    if p.returncode:raise RuntimeError('Native cache probe compilation failed: '+p.stderr[-1000:])
    if not EXEC.is_file():raise RuntimeError('Compiler reported success without executable')
    return {'cache_probe_source_sha256':sha(SOURCE),'cache_probe_executable_sha256':sha(EXEC)}

def verify_csv(path:Path,expected:int=256)->dict:
    path=Path(path)
    with path.open(newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=expected:raise ValueError('Incomplete real cache trials')
    good=[];orders=[0,0];core=None
    for i,r in enumerate(rows):
        try:
            idx=int(r['trial']);o=int(r['order'])
            w=int(r['cached_tsc']);e=int(r['evicted_tsc']);c=int(r['warm_control_tsc'])
            cpu=int(r['cpu_pinned']);aux=[int(r[x]) for x in ('aux_cached','aux_evicted','aux_control')]
        except (ValueError,KeyError,TypeError) as exc:raise ValueError('Invalid trace fields') from exc
        if idx!=i or o not in (0,1) or min(w,e,c)<=0 or len(set(aux))!=1 or any(x==999999 for x in aux):
            raise ValueError('Counter or CPU migration error in actual cache trial')
        if core is None:core=cpu
        if core!=cpu:raise ValueError('Pinned CPU changed')
        orders[o]+=1;good.append((e-w,w-c))
    if min(orders)<expected//5:raise ValueError('Missing counterbalanced cache order')
    d=[x[0] for x in good]
    controls=[x[1] for x in good]
    med=statistics.median(d)
    return {'cache_provenance':'REAL_RDTSCP_LOADS_AND_CLFLUSH_COHERENCE',
            'trace_sha256':sha(path),'trials':expected,'pinned_cpu':core,
            'counterbalanced_orders':orders,'evicted_minus_cached_median_tsc':med,
            'evicted_slower_fraction':sum(x>0 for x in d)/expected,
            'warm_minus_warm_control_median_tsc':statistics.median(controls),
            'cache_latency_causal_gate':bool(med>20 and sum(x>0 for x in d)/expected>=0.90),
            'not_analog_voltage_or_temperature_measurement':True}

def run_probe(prefix:Path,number:int=256)->dict:
    if not 200<=number<=5000:raise ValueError('Probe trial bounds')
    prefix=Path(prefix)
    raw=prefix.with_suffix('.cache.csv')
    if raw.exists():raise FileExistsError('Refuse overwrite of cache measurement')
    if not EXEC.is_file():compile_native()
    p=subprocess.run([str(EXEC),str(number),str(raw)],capture_output=True,text=True,timeout=30)
    prefix.with_suffix('.cache.stdout.txt').write_text(p.stdout)
    prefix.with_suffix('.cache.stderr.txt').write_text(p.stderr)
    if p.returncode:raise RuntimeError(f'Actual cache probe failed: {p.returncode}: {p.stderr[-300:]}')
    data=verify_csv(raw,number)
    data.update({'cache_probe_source_sha256':sha(SOURCE),'cache_probe_executable_sha256':sha(EXEC),
                 'stdout_sha256':sha(prefix.with_suffix('.cache.stdout.txt')),
                 'stderr_sha256':sha(prefix.with_suffix('.cache.stderr.txt'))})
    return data

def with_observation(command:dict,observation:dict,base_work:int)->dict:
    """Feed ACTUALLY measured cache response into next native CPU command."""
    if observation['trials']<200 or observation['cache_provenance']!='REAL_RDTSCP_LOADS_AND_CLFLUSH_COHERENCE':
        raise ValueError('No eligible measured cache response')
    # Quantized feedback is a digital interface between engines, not novel silicon physics.
    offset=int(observation['evicted_minus_cached_median_tsc'])
    return {'rotate':(command['rotate']+(offset//17)%4)%4,
            'work':base_work+(command['work']-base_work+(offset//41)%3)%3}
