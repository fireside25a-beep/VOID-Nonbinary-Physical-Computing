#!/usr/bin/env python3
"""Non-destructive EntropyAVX CMake relocation/build repair for restored workspaces.
Never edits original source archives; preserves stale absolute-path build trees.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'03_NATIVE_TOOLCHAIN/EntropyAVX'
BUILD=SOURCE/'build_workspace_cache'
LOGS=ROOT/'04_TESTS_AND_LOGS/20261029_RELOCATION_FIX'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def run(cmd,timeout):
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
    return {'command':cmd,'status':'PASS' if p.returncode==0 else 'FAIL',
            'exit':p.returncode,'stdout':p.stdout[-10000:],'stderr':p.stderr[-10000:]}
def main():
    LOGS.mkdir(parents=True,exist_ok=True)
    log=LOGS/('relocation_'+str(time.time_ns())+'.json')
    receipts=[]
    cache=BUILD/'CMakeCache.txt'
    if cache.exists():
        txt=cache.read_text(errors='replace')
        if 'CMAKE_HOME_DIRECTORY:INTERNAL='+str(SOURCE) not in txt:
            digest=sha(cache)[:12]
            backup=SOURCE/('build_workspace_cache_preserved_stale_'+digest)
            if backup.exists():raise RuntimeError('Refuse overwrite stale-build backup: '+str(backup))
            BUILD.rename(backup)
            receipts.append({'operation':'preserved_stale_build_directory','location':str(backup)})
    if not (BUILD/'CMakeCache.txt').is_file():
        r=run(['cmake','-S',str(SOURCE),'-B',str(BUILD)],45)
        receipts.append(r)
        if r['status']!='PASS':raise RuntimeError('CMake configure failure')
    r=run(['cmake','--build',str(BUILD),'--parallel','2'],90)
    receipts.append(r)
    if r['status']!='PASS':raise RuntimeError('CMake build failure')
    exe=BUILD/'EntropyAVXEngine'
    if not exe.is_file() or not exe.stat().st_mode&0o111:raise RuntimeError('Native binary missing execute permissions')
    r=run([sys.executable,'-S',str(SOURCE/'microkernel.py')],60)
    receipts.append(r)
    if r['status']!='PASS':raise RuntimeError('Native launcher failed')
    receipt={'schema':'VOID_ENTROPY_AVX_RELOCATION_BUILD_REPAIR_V1',
             'receipts':receipts,'binary_sha256':sha(exe),'status':'PASS'}
    log.write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: restored native build and launcher; receipt',log)
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
