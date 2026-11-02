#!/usr/bin/env python3
"""Read-only, streaming member hashes and inventory for user supplied ZIPs."""
from pathlib import Path
from zipfile import ZipFile,BadZipFile
from collections import defaultdict,Counter
import hashlib,csv,json,os,io,struct
ROOT=Path(os.environ.get('VOID_ARCHIVE_DIR', Path(__file__).resolve().parent.parent))
OUT=Path(os.environ.get('VOID_AUDIT_OUTPUT', Path(__file__).resolve().parent))
OUT.mkdir(parents=True,exist_ok=True)
paths=sorted(p for p in ROOT.glob('*.zip') if p.is_file())

def shafile(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

entries=[]; bundles=[]; dup_content=defaultdict(list); flags=[]
for a in paths:
 rec=dict(archive=a.name,bytes=a.stat().st_size,sha256=shafile(a))
 shaerrors=[]
 with ZipFile(a) as z:
  mem=z.infolist(); rec['entries']=len(mem);rec['uncompressed_bytes']=sum(x.file_size for x in mem)
  rec['dir_entries']=sum(x.is_dir() for x in mem)
  rec['extension_counts']=dict(Counter(Path(i.filename).suffix.lower() or '[none]' for i in mem))
  for idx,item in enumerate(mem):
   fname=item.filename
   suspicious=(fname.startswith('/') or '\\' in fname or '..' in Path(fname).parts or bool(item.flag_bits & 1))
   if suspicious: flags.append(dict(archive=a.name,path=fname,flag='suspicious path or encryption'))
   if item.is_dir():continue
   h=hashlib.sha256()
   try:
    with z.open(item) as f:
     while True:
      chunk=f.read(1024*1024)
      if not chunk:break
      h.update(chunk)
    digest=h.hexdigest()
   except Exception as exc:
    shaerrors.append([fname,str(exc)]); digest='CRC_OR_READ_ERROR'
   pathparts=Path(fname).parts
   entry=dict(archive=a.name,name=fname,member_index=idx,bytes=item.file_size,sha256=digest,crc=f'{item.CRC:08x}',extension=Path(fname).suffix.lower(),is_nested_zip=(Path(fname).suffix.lower()=='.zip'))
   entries.append(entry)
   dup_content[(item.file_size,digest)].append((a.name,fname))
 rec['read_errors']=shaerrors
 bundles.append(rec)
 print(a.name,'entries',len(mem),'read_errs',len(shaerrors),flush=True)
with (OUT/'ARCHIVE_MANIFEST.json').open('w') as f:json.dump(bundles,f,indent=2)
with (OUT/'MEMBER_INVENTORY.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(entries[0]));w.writeheader();w.writerows(entries)
with (OUT/'CONTENT_DUPLICATE_GROUPS.json').open('w') as f:
 groups=[{'bytes':size,'sha256':sha,'copies':locs} for (size,sha),locs in dup_content.items() if len(locs)>1 and sha!='CRC_OR_READ_ERROR']
 groups.sort(key=lambda x:(-x['bytes']*(len(x['copies'])-1),-len(x['copies'])))
 json.dump(groups,f,indent=2)
with (OUT/'ISSUES.json').open('w') as f:json.dump(flags,f,indent=2)
print('TOTAL',len(entries),'unique payloads',len(dup_content),'duplicate groups',len(groups),'duplicate content extra bytes',sum(g['bytes']*(len(g['copies'])-1) for g in groups),'flags',len(flags))
print('largest duplicate groups:')
for d in groups[:15]:
 print(f" {d['bytes']:10} x {len(d['copies'])} {d['sha256'][:16]}")
 for a,b in d['copies'][:3]:print('   ',a,' :: ',b[-120:])
