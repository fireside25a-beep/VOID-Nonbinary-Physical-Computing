#!/usr/bin/env python3
"""Snapshot and split the ONE canonical VOID/HX89 workplace into logical <200 MB ZIPs.
All historical versions retained in existing hierarchy; never edits the source worktree.
"""
import hashlib,json,os,sys,zipfile,stat,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=None
LIMIT=200_000_000
EXCLUDE='workplace/01_SOURCES_VERIFIED/VOID_COMPLETE_BUILD_RESEARCH_VOLUME_20261029.zip'
PRE='01_SOURCES_VERIFIED/00_ORIGINAL_USER_UPLOADS/'
PART_A='workplace/'+PRE+'VOID_COMPLETE_VOLUME_PART_01_OF_02.zip.001'
PART_B='workplace/'+PRE+'VOID_COMPLETE_VOLUME_PART_02_OF_02.zip.002'

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def main():
 import argparse
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--dest',required=True,type=Path)
 args=ap.parse_args()
 global OUT
 OUT=args.dest.resolve()
 if OUT.exists() and any(OUT.iterdir()):raise RuntimeError('Refusing to overwrite existing release '+str(OUT))
 OUT.mkdir(parents=True,exist_ok=True)
 modules_dir=OUT/'02_MODULE_FOLDERS';modules_dir.mkdir()
 membership=ROOT/'06_RELEASE_CONTROL/ORIGINAL_FOLDER_MEMBERSHIP_INDEX.json'
 # Reuse the preserved and independently audited historical folder membership;
 # do NOT depend on a previous download or an external absolute machine path.
 previous_index=json.loads(membership.read_text())
 prev={key:(value if value.endswith('.zip') else value+'.zip')
       for key,value in previous_index.items()}
 originals=[p for p in ROOT.rglob('*') if p.is_file()]
 paths=['workplace/'+p.relative_to(ROOT).as_posix() for p in originals]
 if len(paths)!=len(set(paths)):raise RuntimeError('duplicate source paths')
 if EXCLUDE not in paths:raise RuntimeError('301MB historical master is missing')
 workmap=dict(zip(paths,originals))
 if PART_A not in workmap or PART_B not in workmap:raise RuntimeError('Required original master transport halves absent')
 # Do not ever rewrite/copy the >200 MB source as a standalone module member.
 with open(workmap[PART_A],'rb') as f1,open(workmap[PART_B],'rb') as f2:
  h=hashlib.sha256(); n=0
  for stream in (f1,f2):
   for chunk in iter(lambda:stream.read(1<<20),b''):
    h.update(chunk);n+=len(chunk)
 if (h.hexdigest(),n)!=(digest(workmap[EXCLUDE]),workmap[EXCLUDE].stat().st_size):
  raise RuntimeError('source master differs from concatenated original split halves')
 module_names=sorted(set(prev.values()))
 assignments={p:[] for p in module_names}
 def choose(path):
  if path in prev:return prev[path]
  rel=path[len('workplace/'):]
  if rel.startswith(('04_TESTS_AND_LOGS/','05_EVIDENCE/','06_RELEASE_CONTROL/','07_DELIVERY/','08_DOCUMENTATION/','09_RESULTS_VISUALS/','00_PROJECT_PORTAL/','00_CONTROL/','90_PRESERVED_PROVENANCE/')) or '/' not in rel:
   return '08_ALL_TESTS_LOGS_PLANNER_WATCHDOG.zip'
  if rel.startswith('03_NATIVE_TOOLCHAIN/'):
   return '07_HX89_AVX_CPU_NATIVE_EXECUTABLES.zip'
  if rel.startswith(('01_SOURCES_VERIFIED/ACDC/','01_SOURCES_VERIFIED/AVX/')):
   return '09_ACDC_AVX_SEPARATE_SOURCE_SNAPSHOTS.zip'
  if rel.startswith('02_ACTIVE_R08/'):
   return '03_VOID_R08_ORIGINAL_AND_ACTIVE_NETLISTS.zip'
  if rel.startswith('01_SOURCES_VERIFIED/'):
   raise RuntimeError('New historical source member needs manual classification '+path)
  raise RuntimeError('Unclassified project member '+path)
 for rel in paths:
  if rel!=EXCLUDE:assignments[choose(rel)].append(rel)
 actual_members=set(sum(assignments.values(),[]))
 if actual_members != set(paths)-{EXCLUDE}:raise RuntimeError('coverage loss or duplicate')
 module_records=[]
 for name, members in assignments.items():
  zpath=modules_dir/name
  with zipfile.ZipFile(zpath,'w',allowZip64=True) as z:
   for rel in sorted(members):
    filepath=workmap[rel]
    ext=filepath.suffix.lower()
    # Already compressed archives store verbatim; documents compress efficiently.
    comp=zipfile.ZIP_STORED if ext in ('.zip','.zst','.gz','.xz','.jpg','.jpeg','.png','.webp','.mp4','.pdf','.bin','.001','.002','.tar') else zipfile.ZIP_DEFLATED
    z.write(filepath,arcname=rel,compress_type=comp,compresslevel=5 if comp==zipfile.ZIP_DEFLATED else None)
  if zpath.stat().st_size>=LIMIT:raise RuntimeError(f'{name} exceeds 200MB: {zpath.stat().st_size}')
  with zipfile.ZipFile(zpath) as z:
   if z.testzip() is not None:raise RuntimeError('CRC failure '+name)
   if set(z.namelist())!=set(members):raise RuntimeError('module coverage mismatch '+name)
  item={'name':name,'files':len(members),'bytes':zpath.stat().st_size,'sha256':digest(zpath)}
  module_records.append(item)
  print('PACKED',name,round(item['bytes']/1e6,2),'MB',len(members),'files',flush=True)
 allfiles=[];total=0
 for rel,p in sorted(workmap.items()):
  sz=p.stat().st_size;total+=sz
  allfiles.append({'path':rel,'size':sz,'sha256':digest(p),'mode':stat.S_IMODE(p.stat().st_mode)})
 dirs=['workplace']+['workplace/'+p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()]
 dirs=sorted(set(dirs))
 audit=OUT/'03_AUDIT';audit.mkdir()
 (audit/'ALL_FILES_SHA256.json').write_text(json.dumps(allfiles,indent=2)+'\n')
 manifest={'schema':'VOID_HX89_CANONICAL_COHERENT_WORKPLACE_NINE_MODULES_V3',
           'root':'workplace/','expected_file_count':len(allfiles),
           'expected_total_file_bytes':total,'directory_paths':dirs,'modules':module_records,
           'large_historical_master_regeneration':{
              'path':EXCLUDE,'bytes':workmap[EXCLUDE].stat().st_size,
              'sha256':digest(workmap[EXCLUDE]),'parts':[PART_A,PART_B]},
           'module_size_limit_bytes_exclusive':LIMIT,
           'one_active_native_machine':'workplace/00_CONTROL/run_canonical_release.py',
           'physical_nonbinary_material_machine_verified':False}
 (audit/'CANONICAL_RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (OUT/'README_START_HERE.md').write_text('# VOID / HX89 — Complete Canonical Workplace\n\n'
     'The nine folder ZIPs collectively restore **one complete workplace/** tree, not nine competing versions. '
     'The source hierarchy contains all original archives, retained historical versions, real HX89/AVX/native CPU sources, K01–K06 netlists, physical experiments, tests, logs, failures, diagrams, graphs and 116 historical milestones.\n\n'
     '## Restore and verify\n\n'
     'Place all nine ZIPs and the audit kit in one directory (ZIPs may stay under `02_MODULE_FOLDERS/`). '
     'Extract the audit kit and run:\n\n'
     '```sh\npython3 RESTORE_AND_AUDIT.py --source . --verify-only\npython3 RESTORE_AND_AUDIT.py --source . --dest RESTORED_VOID_HX89\n```\n\n'
     'The verifier recreates the exact historical 301,454,742-byte archive from its TWO original uploaded byte parts; '
     'it is not missing from the restored tree. It then SHA-verifies **every file**, validates directories and executable flags. '
     'A restore destination must not already exist.\n\n'
     '## Canonical build & integration run\n\n'
     '```sh\ncd RESTORED_VOID_HX89/workplace\n'
     'python3 -S 00_CONTROL/repair_restored_native_build.py\n'
     'python3 -S 00_CONTROL/run_canonical_release.py --repeat 2 --cycles 4 --material-blocks 2\n```\n\n'
     'See `README.md`, `08_DOCUMENTATION/`, `09_RESULTS_VISUALS/`, and latest `04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/`. '
     'Native/software gate PASS does not prove a nonbinary physical CPU substrate or K06-connected analog memory.\n\n'
     '## Module sizes and files\n\n'+''.join(f"- {e['name']}: {e['bytes']:,} bytes, {e['files']:,} files\n" for e in module_records))
 print('SOURCE INVENTORY',len(allfiles),'regular files',total,'bytes',len(dirs),'directories',flush=True)
 print('SOURCE INTEGRITY HASHES WRITTEN',flush=True)
 return manifest

if __name__=='__main__':
 try:main()
 except Exception as e:print('FINAL PACKAGING ERROR:',e,file=sys.stderr,flush=True);sys.exit(1)
