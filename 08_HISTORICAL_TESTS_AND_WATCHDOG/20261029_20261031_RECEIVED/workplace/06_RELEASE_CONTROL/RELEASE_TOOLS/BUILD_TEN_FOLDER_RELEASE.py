#!/usr/bin/env python3
"""Seal one complete VOID/HX89 workplace as logical ZIP folders <200MB each.

The restored directory tree is the source of truth. Historical archives are
preserved unchanged; a single >200MB historical master is reconstructed from
its authentic split sources by the independently audited restoration kit.
"""
from __future__ import annotations
import csv, hashlib, json, os, shutil, stat, sys, time, zipfile
from pathlib import Path

SRC=Path(sys.argv[1]).resolve()
DEST=Path(sys.argv[2]).resolve()
MAX=200_000_000
HIST_INDEX=SRC/'06_RELEASE_CONTROL/ORIGINAL_FOLDER_MEMBERSHIP_INDEX.json'
EXCLUDED='workplace/01_SOURCES_VERIFIED/VOID_COMPLETE_BUILD_RESEARCH_VOLUME_20261029.zip'
PARTS=[
'workplace/01_SOURCES_VERIFIED/00_ORIGINAL_USER_UPLOADS/VOID_COMPLETE_VOLUME_PART_01_OF_02.zip.001',
'workplace/01_SOURCES_VERIFIED/00_ORIGINAL_USER_UPLOADS/VOID_COMPLETE_VOLUME_PART_02_OF_02.zip.002']
NAMES=[
'01_ORIGINAL_VOID_MASTER_PART_1.zip',
'02_ORIGINAL_VOID_MASTER_PART_2.zip',
'03_VOID_R08_ACTIVE_ARCHITECTURE_NETLISTS.zip',
'04_VERIFIED_R08_SOURCE_WORKTREES.zip',
'05_HISTORICAL_VOID_RELEASE_ARCHIVES.zip',
'06_HX89_RESEARCH_SOURCE_AND_HANDOFF.zip',
'07_ACTIVE_HX89_AVX_CPU_MACHINE.zip',
'08_COMPLETE_TESTS_LOGS_MILESTONES_WATCHDOG.zip',
'09_ACDC_AND_AVX_ORIGINAL_SNAPSHOTS.zip',
'10_UNIFIED_README_DOCS_GRAPHS.zip'
]

def sha(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda:f.read(1<<20),b''):h.update(data)
    return h.hexdigest()

def assign(rel,index):
    old=index.get(rel)
    if old:
        n=int(old.split('_',1)[0])
        return n-1
    r=Path(rel).relative_to('workplace')
    top=r.parts[0]
    if top in ('00_PROJECT_PORTAL','08_DOCUMENTATION','09_RESULTS_VISUALS') or len(r.parts)==1:
        return 9
    if top=='03_NATIVE_TOOLCHAIN':return 6
    if top in ('00_CONTROL','04_TESTS_AND_LOGS','05_EVIDENCE','06_RELEASE_CONTROL',
               '07_DELIVERY','90_PRESERVED_PROVENANCE'):
        return 7
    if top=='02_ACTIVE_R08':return 2
    raise ValueError('Unclassified new path; must not omit a source: '+rel)

def main():
    if not (SRC/'00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv').is_file():
        raise RuntimeError('Not an authoritative VOID/HX89 worktree')
    if DEST.exists():raise RuntimeError('Target folder exists: refuse overwriting a prior release')
    index=json.loads(HIST_INDEX.read_text())
    inventory={}
    groups=[[] for _ in NAMES]
    for f in sorted(SRC.rglob('*')):
        if not f.is_file():continue
        if f.is_symlink():raise RuntimeError('Symlink refused: '+str(f))
        rel='workplace/'+f.relative_to(SRC).as_posix()
        mode=stat.S_IMODE(f.stat().st_mode)
        if mode & 0o6000:raise RuntimeError('Setuid/setgid source refused: '+rel)
        inventory[rel]={'path':rel,'size_bytes':f.stat().st_size,'sha256':sha(f),'mode':mode}
        if rel!=EXCLUDED:groups[assign(rel,index)].append((rel,f))
    if EXCLUDED not in inventory:raise RuntimeError('Historical master missing')
    if inventory[EXCLUDED]['size_bytes']<=MAX:raise RuntimeError('Unexpected source-master contract')
    all_files=set(inventory)
    packed={name for group in groups for name,_ in group}
    if packed!=all_files-{EXCLUDED}:
        raise RuntimeError(f'Unassigned or duplicated files: {len(packed)} vs {len(all_files)}')
    dirs=sorted('workplace/'+p.relative_to(SRC).as_posix() for p in SRC.rglob('*') if p.is_dir())
    DEST.mkdir(parents=True)
    mods=DEST/'02_MODULE_FOLDERS'
    mods.mkdir()
    status=[]
    for idx,entries in enumerate(groups):
        zp=mods/NAMES[idx]
        with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
            for rel,path in entries:
                z.write(path,arcname=rel)
        if zp.stat().st_size>=MAX:raise RuntimeError('Module exceeds 200 million bytes; abort release: '+str(zp))
        with zipfile.ZipFile(zp) as z:
            if z.testzip() is not None:raise RuntimeError('ZIP CRC failure: '+str(zp))
            if len(z.infolist())!=len(entries):raise RuntimeError('ZIP member count mismatch')
        status.append({'name':zp.name,'file_count':len(entries),'bytes':zp.stat().st_size,'sha256':sha(zp)})
        print(f'PACKED {idx+1:02} {zp.name} {len(entries)} files, {zp.stat().st_size} bytes',flush=True)
    audits=DEST/'03_AUDIT'
    audits.mkdir()
    with (audits/'ALL_FILES_SHA256.json').open('w') as f:
        json.dump([inventory[k] for k in sorted(inventory)],f,separators=(',',':'));f.write('\n')
    expected_master=inventory[EXCLUDED]
    origin={'schema':'VOID_HX89_ONE_TREE_SEALED_V3','root':'workplace',
            'expected_file_count':len(inventory),'expected_total_file_bytes':sum(r['size_bytes'] for r in inventory.values()),
            'modules':status,'directory_paths':dirs,
            'excluded_large_file_to_regenerate':{
                'path':EXCLUDED,'reconstruct_by_concatenating':PARTS,
                'bytes':expected_master['size_bytes'],'sha256':expected_master['sha256']},
            'all_single_module_files_present':True,
            'historical_milestones':116,
            'physical_nonbinary_material_computation_verified':False}
    (audits/'CANONICAL_FOLDER_MANIFEST.json').write_text(json.dumps(origin,indent=2)+'\n')
    print('SOURCE INVENTORY',len(inventory),'files',origin['expected_total_file_bytes'],'bytes',flush=True)
    print('SUCCESS: ZIPs all under 200MB, proof verification continues in restore tool.',flush=True)
if __name__=='__main__':main()
