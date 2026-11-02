#!/usr/bin/env python3
"""Index first-level ZIP-in-ZIP contents read-only, avoiding redundant copies."""
from pathlib import Path
from zipfile import ZipFile,BadZipFile
from io import BytesIO
from collections import Counter
import hashlib,json,csv,os
root=Path(os.environ.get('VOID_ARCHIVE_DIR', Path(__file__).resolve().parent.parent));out=Path(os.environ.get('VOID_AUDIT_OUTPUT', Path(__file__).resolve().parent));out.mkdir(parents=True,exist_ok=True)
seen={}; rows=[]; errors=[]
for p in sorted(root.glob('*.zip')):
 with ZipFile(p) as z:
  for info in z.infolist():
   if not info.filename.lower().endswith('.zip'):continue
   data=z.read(info)
   h=hashlib.sha256(data).hexdigest()
   basic=dict(archive=p.name,outer_member=info.filename,nested_zip_sha256=h,nested_zip_bytes=len(data),duplicate_of=seen.get(h,''))
   if h in seen:
    basic.update(file_members=seen[h][1],internal_uncompressed_bytes=seen[h][2],verified_crc=seen[h][3],nested_zip_member_count=seen[h][4]);rows.append(basic)
    continue
   try:
    with ZipFile(BytesIO(data)) as nz:
     members=[n for n in nz.infolist() if not n.is_dir()]
     count=len(members); nbytes=sum(x.file_size for x in members)
     nested_count=sum(x.filename.lower().endswith('.zip') for x in members)
     # source-only verification: read every member, no extraction
     failure=nz.testzip(); good=failure is None
     if failure:errors.append((p.name,info.filename,failure))
     seen[h]=(info.filename,count,nbytes,good,nested_count)
     basic.update(file_members=count,internal_uncompressed_bytes=nbytes,verified_crc=good,nested_zip_member_count=nested_count)
   except Exception as e:
    errors.append((p.name,info.filename,str(e)))
    basic.update(file_members=-1,internal_uncompressed_bytes=-1,verified_crc=False,nested_zip_member_count=-1)
   rows.append(basic)
with (out/'NESTED_ZIP_INDEX.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (out/'NESTED_ZIP_ERRORS.json').open('w') as f:json.dump(errors,f,indent=2)
print('nested copies',len(rows),'distinct archives',len(seen),'errors',len(errors),'sum distinct internal file members',sum(s[1] for s in seen.values()))
for r in rows:
 if not r['duplicate_of']:print(str(r['file_members']).rjust(6),'members',str(r['internal_uncompressed_bytes']).rjust(10),'bytes ',r['outer_member'].split('/')[-1], 'nested',r['nested_zip_member_count'])
