#!/usr/bin/env python3
"""Immutable-input intake, deterministic manifest, bounded safe extraction."""
from pathlib import Path
from hashlib import sha256
import zipfile, json, csv, stat, shutil, sys, time
BASE=Path('/mnt/data'); W=BASE/'workplace'; CTRL=W/'00_CONTROL'; SRC=W/'01_SOURCES_VERIFIED'; SRC.mkdir(parents=True,exist_ok=True)
parts=[BASE/'VOID_COMPLETE_VOLUME_PART_01_OF_02.zip.001', BASE/'VOID_COMPLETE_VOLUME_PART_02_OF_02.zip.002']
expected=['9fac288a28d626c6da8e459fa88aae45d5a5ef5ee62bee95f13c75154b546c98','886062734193bbda1afa7668bc250bbb7bc1ff7a1c3335866afc9836865900f0']
def digest(p):
 h=sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
log={'inputs':[],'zips':[],'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
for p,he in zip(parts,expected):
 assert p.stat().st_size==150727371,(p,p.stat().st_size)
 got=digest(p);assert got==he,(p,got)
 log['inputs'].append({'name':p.name,'bytes':p.stat().st_size,'sha256':got,'result':'PASS'})
full=SRC/'VOID_COMPLETE_BUILD_RESEARCH_VOLUME_20261029.zip'
if not full.exists():
 with full.open('xb') as out:
  for p in parts:
   with p.open('rb') as stream:shutil.copyfileobj(stream,out,1024*1024)
assert full.stat().st_size==301454742 and digest(full)=='3870dddb2cc7c89a5f0f2da6d7f9cc00770cf5ba3832956e587a42ecbbe801fc'
archives=[('MASTER',full,'3870dddb2cc7c89a5f0f2da6d7f9cc00770cf5ba3832956e587a42ecbbe801fc'),('R08',BASE/'VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip','d5e1a2ef956d5c6fefda727e294a0d25f3aaa15882543779181f072c901b97ad'),('AVX',BASE/'EntropyAVXEngine-source-trace-and-bootstrap(3).zip','94310df038c8f5024bba59420fe104a8748b0044a538f9799ce8a84570c8a176'),('ACDC',BASE/'AC_DC_Passive_AI_Proof(2)(1).zip',None)]
with (CTRL/'FILE_INVENTORY.tsv').open('w',newline='') as f:
 wr=csv.writer(f,delimiter='\t');wr.writerow(['archive','path','uncompressed_bytes','crc32','sha256'])
 for name,p,expected_hash in archives:
  actual=digest(p)
  if expected_hash: assert actual==expected_hash, (name,actual)
  dest=SRC/name;dest.mkdir(exist_ok=True)
  with zipfile.ZipFile(p) as z:
   infos=z.infolist();seen=set();total=0
   for info in infos:
    s=info.filename
    pp=Path(s)
    assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in s and not s.startswith('/'),s
    assert not stat.S_ISLNK(info.external_attr>>16),s
    assert s not in seen,s
    seen.add(s)
    if info.is_dir():continue
    assert info.file_size<=150_000_000,('oversize',s)
    total+=info.file_size
    assert total<=1_500_000_000,('zipbomb',name)
    output=dest/pp
    output.parent.mkdir(parents=True,exist_ok=True)
    # CRC is verified while streaming; refuse overwrite on conflicting snapshots.
    with z.open(info) as src:
     h=sha256()
     if output.exists():
      with output.open('rb') as old:
       for chunk in iter(lambda:old.read(1024*1024),b''):h.update(chunk)
      assert h.hexdigest()==(lambda: hash_member(z,info))(),s
     else:
      with output.open('xb') as dst:
       for chunk in iter(lambda:src.read(1024*1024),b''):
        dst.write(chunk);h.update(chunk)
    wr.writerow([name,s,info.file_size,f'{info.CRC:08x}',h.hexdigest()])
  log['zips'].append({'name':name,'source_name':p.name,'bytes':p.stat().st_size,'sha256':actual,'members':len(infos),'unpacked_bytes':total,'result':'PASS'})
(CTRL/'INTAKE.json').write_text(json.dumps(log,indent=2)+'\n')
print(json.dumps(log,indent=2))
