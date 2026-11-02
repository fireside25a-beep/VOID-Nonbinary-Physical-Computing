#!/usr/bin/env python3
"""Restore the coherent VOID/HX89 workplace from nine independent, audited ZIPs.
Never overwrites files; verifies all complete files and the exact original master.
Python standard library only. Windows/macOS/Linux.
"""
import argparse,hashlib,json,os,stat,sys,zipfile
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def safe_path(name):
 p=Path(name)
 if p.is_absolute() or not p.parts or '..' in p.parts or p.parts[0]!='workplace' or '\\' in name:
  raise RuntimeError('Unsafe path in source archive '+repr(name))
 return p

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parent)
 ap.add_argument('--dest',type=Path,default=Path('RESTORED_VOID_HX89'))
 ap.add_argument('--verify-only',action='store_true')
 args=ap.parse_args()
 source=args.source.resolve()
 def manifest_file(n):
  for p in (source/n, source/'03_AUDIT'/n):
   if p.is_file():return p
  raise RuntimeError('Audit kit manifest missing '+n)
 meta=json.loads(manifest_file('CANONICAL_RELEASE_MANIFEST.json').read_text())
 files=json.loads(manifest_file('ALL_FILES_SHA256.json').read_text())
 if len(files)!=meta['expected_file_count']:raise RuntimeError('Inconsistent expected file count')
 expected={x['path']:x for x in files}
 if len(expected)!=len(files):raise RuntimeError('Duplicate manifest entries')
 excluded=meta['large_historical_master_regeneration']['path']
 listed=set(); modules=[]
 for entry in meta['modules']:
  name=entry['name']
  path=next((x for x in (source/name,source/'02_MODULE_FOLDERS'/name) if x.is_file()),None)
  if path is None:raise RuntimeError('Missing ZIP module '+name)
  if path.stat().st_size!=entry['bytes'] or sha(path)!=entry['sha256']:
   raise RuntimeError('Size/hash mismatch in module '+name)
  if path.stat().st_size>=meta['module_size_limit_bytes_exclusive']:
   raise RuntimeError('Oversized ZIP module '+name)
  with zipfile.ZipFile(path) as z:
   if z.testzip() is not None:raise RuntimeError('ZIP CRC mismatch '+name)
   if len(z.infolist())!=entry['files']:raise RuntimeError('Member count mismatch '+name)
   for info in z.infolist():
    member=info.filename;safe_path(member)
    if info.is_dir() or member in listed or member not in expected or member==excluded:
     raise RuntimeError('Unexpected or duplicated module member '+member)
    mode=(info.external_attr>>16)&0o170000
    if mode not in (0,0o100000):raise RuntimeError('Nonregular/possibly symlink ZIP member '+member)
    listed.add(member)
  modules.append(path)
  print('SHA+CRC PASS:',name,flush=True)
 if listed != set(expected)-{excluded}:raise RuntimeError('Incomplete original source inventory in nine ZIPs')
 if args.verify_only:
  print('PASS: nine ZIP module hashes, CRC, coverage',len(expected),'expected files')
  return
 dest=args.dest.resolve()
 if dest.exists():raise RuntimeError('Non-destructive refusal: destination already exists: '+str(dest))
 dest.mkdir(parents=True)
 for path in modules:
  with zipfile.ZipFile(path) as z:
   for info in z.infolist():
    rel=safe_path(info.filename);out=dest/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    with z.open(info) as f,out.open('xb') as w:
     while True:
      chunk=f.read(1048576)
      if not chunk:break
      w.write(chunk)
    original_mode=expected[info.filename]['mode']
    if os.name!='nt':out.chmod(original_mode&0o777)
 for dir_rel in meta['directory_paths']:
  p=safe_path(dir_rel)
  (dest/p).mkdir(parents=True,exist_ok=True)
 record=meta['large_historical_master_regeneration']
 output=dest/safe_path(record['path'])
 output.parent.mkdir(parents=True,exist_ok=True)
 with output.open('xb') as w:
  for part in record['parts']:
   with (dest/safe_path(part)).open('rb') as r:
    while True:
     chunk=r.read(1048576)
     if not chunk:break
     w.write(chunk)
 if output.stat().st_size!=record['bytes'] or sha(output)!=record['sha256']:
  raise RuntimeError('Reconstructed >200 MB original master mismatched original bytes')
 if os.name!='nt':output.chmod(expected[record['path']]['mode']&0o777)
 total=0
 for obj in files:
  path=dest/safe_path(obj['path']);size=path.stat().st_size
  if size!=obj['size'] or sha(path)!=obj['sha256']:
   raise RuntimeError('Source file failed exact hash check: '+obj['path'])
  total+=size
 if total!=meta['expected_total_file_bytes']:raise RuntimeError('Total source byte count mismatch')
 actual={'workplace/'+p.relative_to(dest/'workplace').as_posix() for p in (dest/'workplace').rglob('*') if p.is_file()}
 if actual!=set(expected):raise RuntimeError('Missing or extraneous output files')
 actual_dirs={'workplace'}|{'workplace/'+p.relative_to(dest/'workplace').as_posix() for p in (dest/'workplace').rglob('*') if p.is_dir()}
 if actual_dirs!=set(meta['directory_paths']):raise RuntimeError('Missing or extraneous directories')
 print('PASS: FRESH RESTORE:',len(files),'complete files,',total,'bytes,',len(actual_dirs),'directories, SHA-256 exact')
 print('Single canonical workplace root:',dest/'workplace')

if __name__=='__main__':
 try:main()
 except Exception as e:print('RESTORE / AUDIT FAILURE:',e,file=sys.stderr);sys.exit(1)
