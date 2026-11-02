#!/usr/bin/env python3
"""Bounded, restartable, fail-closed native engineering watchdog.

This independent verification software is NOT VOID's material computing substrate.
It runs only when launched by a user/process; it cannot wake ChatGPT between turns.
Commands have bounded duration. A result is logged for every attempted task, and
failures remain in the append-only journal, never rewritten to passing results.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, subprocess, sys, time, zipfile
import execution_guard
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'01_SOURCES_VERIFIED/00_ORIGINAL_USER_UPLOADS'
LOG=ROOT/'04_TESTS_AND_LOGS/20261029_RESUMED'
BATCH=ROOT/'03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE'
HX=ROOT/'03_NATIVE_TOOLCHAIN/HX89'
AVX=ROOT/'03_NATIVE_TOOLCHAIN/EntropyAVX'
CACHE=ROOT/'03_NATIVE_TOOLCHAIN/ResearchCache'
SOURCES=[
 ('R08',DATA/'VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip','d5e1a2ef956d5c6fefda727e294a0d25f3aaa15882543779181f072c901b97ad',113),
 ('AVX',DATA/'EntropyAVXEngine-source-trace-and-bootstrap(3).zip','94310df038c8f5024bba59420fe104a8748b0044a538f9799ce8a84570c8a176',31),
 ('ACDC',DATA/'AC_DC_Passive_AI_Proof(2)(1).zip','4372eaf5629908da322c7031d437ddbc20295f061ae48e63ee78a4c1ed28a7c4',11),
]
PARTS=[(DATA/'VOID_COMPLETE_VOLUME_PART_01_OF_02.zip.001','9fac288a28d626c6da8e459fa88aae45d5a5ef5ee62bee95f13c75154b546c98'),
       (DATA/'VOID_COMPLETE_VOLUME_PART_02_OF_02.zip.002','886062734193bbda1afa7668bc250bbb7bc1ff7a1c3335866afc9836865900f0')]

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def source_gate():
 for name,p,h,expected in SOURCES:
  if sha(p)!=h:raise RuntimeError('source byte identity changed: '+name)
  with zipfile.ZipFile(p) as z:
   if len(z.namelist())!=expected:raise RuntimeError('archive members changed: '+name)
   bad=z.testzip()
   if bad:raise RuntimeError('CRC failed: '+name+':'+bad)
 for p,h in PARTS:
  if sha(p)!=h:raise RuntimeError('split master changed: '+p.name)
 return {'archive_count':len(SOURCES),'split_parts':len(PARTS),'crc':'PASS'}

def netlist_gate():
 import re
 folder=ROOT/'02_ACTIVE_R08/02_PHYSICAL_CIRCUITS'
 entries=list(folder.glob('*'))
 if len(entries)!=9:raise RuntimeError('unexpected number of active netlist/library sources')
 includes={}
 for file in entries:
  if not file.is_file():raise RuntimeError('unexpected active source path')
  refs=re.findall(r'^\s*\.include\s+"([^"]+)"',file.read_text(),flags=re.I|re.M)
  for name in refs:
   if Path(name).name!=name or not (folder/name).is_file():raise RuntimeError('missing/unsafe lib '+name)
  includes[file.name]=refs
 if not any(len(refs)==3 for refs in includes.values()):raise RuntimeError('expected K06 lib dependency contract missing')
 return {'active_sources':len(entries),'includes':includes,'K06_sha256':sha(folder/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir')}

def master_gate():
 sys.path.insert(0,str(BATCH));import batch_bridge
 return batch_bridge.check_master()

def record(task,status,details,runid):
 LOG.mkdir(parents=True,exist_ok=True)
 out={'run_id':runid,'sequence':len(events),'task':task,'status':status,'details':details,'unix_time':time.time_ns()}
 events.append(out)
 with (LOG/'watchdog_events_append_only.jsonl').open('a') as f:f.write(json.dumps(out,sort_keys=True)+'\n')
 print(json.dumps({'task':task,'status':status,'details':details if status!='PASS' else 'receipt recorded'}),flush=True)

def callable_check(name,fn,runid):
 try:
  details=fn();record(name,'PASS',details,runid)
 except Exception as e:record(name,'FAIL',{'reason':str(e)},runid)

def command_check(name,command,cwd,timeout,runid):
 dest=LOG/(name+'.'+runid+'.log')
 try:
  with dest.open('w') as f:
   p=subprocess.run(command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
  if p.returncode:record(name,'FAIL',{'exit_code':p.returncode,'log':str(dest),'sha256':sha(dest)},runid)
  else:record(name,'PASS',{'exit_code':0,'log':str(dest),'sha256':sha(dest)},runid)
 except subprocess.TimeoutExpired:
  record(name,'FAIL',{'timeout_seconds':timeout,'log':str(dest)},runid)
 except Exception as e:record(name,'FAIL',{'reason':str(e),'log':str(dest)},runid)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runs',type=int,default=1);ns=ap.parse_args()
 if ns.runs<1 or ns.runs>3:raise SystemExit('bounded --runs 1..3')
 for _ in range(ns.runs):
  runid=str(time.time_ns())
  callable_check('source_integrity',source_gate,runid)
  callable_check('milestone_integrity',master_gate,runid)
  callable_check('K01_K06_include_integrity',netlist_gate,runid)
  command_check('cpu_native_compile',['gcc','-O2','-std=c11','-Wall','-Wextra','-Werror','-mrdseed','-mrdrnd','cpu_batch.c','-o','cpu_batch'],BATCH,30,runid)
  command_check('cpu_bridge_negative_tests',[sys.executable,'-m','unittest','-v','test_bridge'],BATCH,45,runid)
  command_check('hx89_complete_suite',['make','check'],HX,180,runid)
  # Each watchdog invocation builds a unique executable. Two concurrent verification
  # runs must not overwrite each other's BVH test binary between compile and exec.
  bvh_binary='bvh_extended_watchdog_'+runid
  command_check('avx_bvh_compile',['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','test_bvh_extended.cpp','bvh_spatial.cpp','-o',bvh_binary],AVX,60,runid)
  if (AVX/bvh_binary).is_file() and os.access(AVX/bvh_binary,os.X_OK):
   command_check('avx_bvh_3003_build_refits',['./'+bvh_binary],AVX,40,runid)
  else:
   record('avx_bvh_3003_build_refits','FAIL',{'reason':'Compiled executable missing/non-executable'},runid)
  command_check('avx_full_build',['cmake','--build','build_workspace_cache','--parallel','2'],AVX,100,runid)
  command_check('research_cache_suite',[sys.executable,'-m','unittest','-v','test_cache'],CACHE/'04_TOOLING',60,runid)
  command_check('cpu_hx89_64_round_causal_run',[sys.executable,str(BATCH/'batch_bridge.py'),'--rounds','64','--work','16'],BATCH,150,runid)
  # The evidence summary is an auditable physical-scope boundary, not a release PASS.
  result={'run_id':runid,'tasks':len(events),'passed':sum(x['status']=='PASS' for x in events),'failed':sum(x['status']=='FAIL' for x in events),
          'all_execution_gates_passed':all(x['status']=='PASS' for x in events),
          'on_die_physical_nonbinary_operator_verified':False,
          'original_archives_unmodified_by_design':True,
          'source_hashes':{p.name:sha(p) for _,p,_,_ in SOURCES},
          'watchdog_source_sha256':sha(Path(__file__))}
  (LOG/'watchdog_latest_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 return 0 if all(x['status']=='PASS' for x in events) else 1

events=[]
if __name__=='__main__':
 try:
  inherited = os.environ.get('VOID_MACHINE_LOCK_FD')
  with execution_guard.exclusive(inherited_fd=inherited):
   sys.exit(main())
 except (RuntimeError, OSError) as exc:
  print('FAIL-CLOSED NATIVE WATCHDOG:', exc, file=sys.stderr)
  sys.exit(2)
