#!/usr/bin/env python3
"""Executed CPU native interventions -> actual HX89 Q2 feedback, with provenance.

No simulated waveform, inferred quantum voltage or invented measurement. Native
CPU observations are constrained digital telemetry about actual silicon execution.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, statistics, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ACTIVE=ROOT/'02_ACTIVE_R08'
CONN=ACTIVE/'07_HX89_PHYSICAL_CONNECTOR/connector.py'
EXEC=HERE/'cpu_batch'
LOGROOT=ROOT/'04_TESTS_AND_LOGS/20261029_RESUMED'
EXPECTED=['scalar','avx2','avx512','large_cache']

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def check_master():
    master=ROOT/'00_CONTROL/VOID_HX89_EXPANDED_MASTER_INPUT_COPY_PASTE_20261029.txt'
    ledger=ROOT/'00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv'
    historical=ACTIVE/'05_MILESTONES/VOID_R08_FULL_116_MILESTONE_CROSSWALK.tsv'
    with ledger.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
    with historical.open(newline='') as f:old=list(csv.DictReader(f,delimiter='\t'))
    ids=[f'M{i:02}' for i in range(116)]
    if [r['id'] for r in rows]!=ids:raise RuntimeError('canonical milestone IDs missing, duplicated or reordered')
    if [r['id'] for r in old]!=ids:raise RuntimeError('historical milestone IDs missing, duplicated or reordered')
    if len(master.read_bytes())!=67474:raise RuntimeError('expanded master identity changed')
    for x,y in zip(rows,old):
        for key in ['id','original_title','roadmap_phase','original_source_status','void_r05_verified_scope','original_dependency','supporting_file_or_baseline','next_evidence_for_physical_completion']:
            if x[key]!=y[key]:raise RuntimeError('historical field changed: '+x['id']+':'+key)
    if len(list((ACTIVE/'02_PHYSICAL_CIRCUITS').glob('*')))!=9:raise RuntimeError('active circuit source inventory unexpected')
    return {'master_sha256':sha(master),'canonical_ledger_sha256':sha(ledger),'original_crosswalk_sha256':sha(historical),'milestone_ids':116}

def analyze(rows,header):
    if header['schema']!='VOID_CPU_BATCH_V1' or not header['avx2']:raise RuntimeError('native probe contract invalid')
    rounds=header['rounds']
    if len(rows)!=4*rounds:raise RuntimeError(f'trial count {len(rows)} != {4*rounds}')
    modes=['scalar','avx2','avx512' if header['avx512f'] else 'avx2_fallback','large_cache']
    by_mode={m:[] for m in modes}
    for r in range(rounds):
        block=rows[4*r:4*r+4]
        if {x['mode'] for x in block}!=set(modes):raise RuntimeError('not all native interventions executed once per round')
        for trial in block:
            if trial['round']!=r or trial['position'] not in range(4):raise RuntimeError('incorrect round/position')
            if not all(isinstance(trial.get(k),int) and trial[k]>0 for k in ['pre_ticks','post_ticks','stimulus_ticks']):raise RuntimeError('invalid TSC observation')
            if any(trial[k]!=trial['processor_id_pre'] for k in ['processor_id_post','processor_id_stim_start','processor_id_stim_end']):raise RuntimeError('CPU migration detected; measurements rejected')
            if not re.fullmatch('[a-f0-9]{16}',trial['native_checksum']):raise RuntimeError('native checksum invalid')
            by_mode[trial['mode']].append(trial)
    summary={m:{'n':len(samples),'median_pre_ticks':statistics.median(x['pre_ticks'] for x in samples),
                'median_post_ticks':statistics.median(x['post_ticks'] for x in samples),
                'median_stimulus_ticks':statistics.median(x['stimulus_ticks'] for x in samples),
                'median_post_minus_pre_ticks':statistics.median(x['post_ticks']-x['pre_ticks'] for x in samples),
                'rdrand_succeeded':sum(x['rdrand_success'] for x in samples),
                'rdseed_succeeded':sum(x['rdseed_success'] for x in samples)} for m,samples in by_mode.items()}
    return summary

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rounds',type=int,default=16)
    ap.add_argument('--work',type=int,default=8)
    ap.add_argument('--out',type=Path,default=LOGROOT)
    args=ap.parse_args()
    if args.rounds<4 or args.rounds>128 or args.work<1 or args.work>200:raise RuntimeError('strict bounds required')
    args.out.mkdir(parents=True,exist_ok=True)
    p=subprocess.run([str(EXEC),'--rounds',str(args.rounds),'--work',str(args.work),'--pin'],text=True,capture_output=True,timeout=120,check=False)
    rawpath=args.out/'cpu_native_trials.jsonl';rawpath.write_text(p.stdout)
    (args.out/'cpu_native_stderr.txt').write_text(p.stderr)
    if p.returncode:raise RuntimeError('Native CPU experiment failed status '+str(p.returncode)+': '+p.stderr)
    decoded=[json.loads(ln) for ln in p.stdout.splitlines()]
    if len(decoded)<2 or decoded[0]['type']!='header':raise RuntimeError('missing native observation header')
    header,rows=decoded[0],decoded[1:]
    if not header['affinity_succeeded']:raise RuntimeError('CPU affinity not achieved, preserving results but rejecting causal inference')
    summary=analyze(rows,header)
    # Invoke existing HX89 native code path, then full Q2 program feedback for each
    # observed round. Never modify original or substitute a simulated native trace.
    sys.path.insert(0,str(CONN.parent));import connector
    machine=check_master()
    contract=connector.k06_contract()
    native=connector.native_trace()
    feedback=[]
    for r in range(args.rounds):
        block=rows[4*r:4*r+4]
        observed=sum(x['post_ticks'] for x in block)+sum(x['stimulus_ticks'] for x in block)
        target=observed%25  # digital transport into HX89, *not* physical material transformation
        response=connector.hx_execute(connector.Q2PROGRAM,('--target-q',str(target)))
        seen=re.findall(r'^SEARCH step=\d+ head=\d+ q=\d+ fitness=\d+ target=(\d+)$',response['stdout'],re.M)
        if not seen or any(int(x)!=target for x in seen):raise RuntimeError('HX89 did not accept actual CPU trial feedback')
        feedback.append({'round':r,'source_trial_indices':[4*r+i for i in range(4)],'target_q':target,
                         'hx89_halt_semantic_hash':response['semantic_hash'],'hx89_program_sha256':response['program_sha256']})
    result={'schema':'VOID_HX89_CPU_NATIVE_BATCH_EXECUTION_V1','status':'NATIVE_CPU_AND_HX89_EXECUTED',
            'physical_nonbinary_substrate_verified':False,'classification':'REAL_NATIVE_CPU_INTERVENTION_AND_HX89_DIGITAL_FEEDBACK',
            'limits_of_evidence':'TSC is digital elapsed-counter evidence with scheduler/VM/power confounders; no raw charge, on-die thermodynamic or K06 board readout',
            'cpu':header,'summary':summary,'hx89_native':{k:v for k,v in native.items() if k!='stdout'},
            'hx89_feedback':feedback,'original_k06':contract,'historical':machine,
            'trace_sha256':sha(rawpath),'probe_source_sha256':sha(HERE/'cpu_batch.c'),
            'bridge_source_sha256':sha(HERE/'batch_bridge.py'),'native_executable_sha256':sha(EXEC)}
    out=args.out/'VOID_CPU_HX89_BATCH_EXECUTION.json';out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'rounds':args.rounds,'native_trials':len(rows),
                      'hx89_feedback_cycles':len(feedback),'summary':summary,'evidence':str(out),'physical_nonbinary_substrate_verified':False},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(json.dumps({'status':'FAIL','reason':str(exc)}),file=sys.stderr)
        sys.exit(5)
