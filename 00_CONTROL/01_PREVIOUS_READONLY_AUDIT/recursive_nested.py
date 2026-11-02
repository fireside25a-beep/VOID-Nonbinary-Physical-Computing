from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
import csv,json,os
ROOT=Path(os.environ.get('VOID_ARCHIVE_DIR', Path(__file__).resolve().parent.parent));OUT=Path(os.environ.get('VOID_AUDIT_OUTPUT', Path(__file__).resolve().parent));OUT.mkdir(parents=True,exist_ok=True); seen=set(); rows=[]; failures=[];MAX_DEPTH=6;MAX_NESTED_SIZE=65_000_000

def scan(blob,prov,depth):
 d=sha256(blob).hexdigest()
 if d in seen:return
 seen.add(d)
 try:
  with ZipFile(BytesIO(blob)) as z:
   infos=z.infolist(); crc=z.testzip();
   rows.append({'sha256':d,'name':prov,'depth':depth,'bytes':len(blob),'members':len(infos),'uncompressed_bytes':sum(i.file_size for i in infos),'crc_ok':crc is None,'nested_zip_count':sum(i.filename.lower().endswith('.zip') for i in infos)})
   if crc:failures.append({'zip':prov,'failure':crc})
   if depth>=MAX_DEPTH:return
   for i in infos:
    if i.filename.lower().endswith('.zip'):
     if i.file_size>MAX_NESTED_SIZE:failures.append({'zip':prov,'failure':'oversize nested file '+i.filename});continue
     scan(z.read(i),prov+'::'+i.filename,depth+1)
 except Exception as e:
  failures.append({'zip':prov,'failure':str(e)})
for p in sorted(ROOT.glob('*.zip')):
 with ZipFile(p) as z:
  for i in z.infolist():
   if i.filename.lower().endswith('.zip'):scan(z.read(i),p.name+'::'+i.filename,1)
with (OUT/'RECURSIVE_NESTED_INDEX.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/'RECURSIVE_NESTED_WARNINGS.json').open('w') as f:json.dump(failures,f,indent=2)
print('unique nested',len(rows),'maxdepth',max(r['depth'] for r in rows),'bad',len(failures),'members total across unique nested',sum(x['members'] for x in rows))
print('depth counts',[(d,sum(x['depth']==d for x in rows)) for d in range(1,MAX_DEPTH+1)])
print('last',[(x['name'][-85:],x['members'],x['depth']) for x in rows[-12:]])
