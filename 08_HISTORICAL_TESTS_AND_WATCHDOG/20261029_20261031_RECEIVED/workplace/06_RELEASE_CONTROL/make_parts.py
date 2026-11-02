#!/usr/bin/env python3
"""Create portable, byte-exact, bounded transport parts for the canonical workplace.

Requires GNU tar and zstd to PACK. A stdlib-only reassembler verifies/rejoins.
Never deletes or overwrites user-supplied originals or previously existing output.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve()
WORK=HERE.parents[1]
ARCHIVE='VOID_HX89_WORKPLACE_COMPLETE_VERIFIED_20261029.tar.zst'
PART_LIMIT=190_000_000  # decimal, strictly smaller than 200 MB

def sha_file(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(2*1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dest',required=True,type=Path)
    args=ap.parse_args()
    dest=args.dest.resolve()
    if dest.exists() and any(dest.iterdir()):
        raise RuntimeError('Destination must not exist or must be an empty directory: '+str(dest))
    dest.mkdir(parents=True,exist_ok=True)
    archive=dest/ARCHIVE
    command=['tar','--sort=name','--format=pax','--mtime=@0','--owner=0','--group=0',
             '--numeric-owner','-C',str(WORK.parent),'-I','zstd -T2 -3','-cf',str(archive),'workplace']
    subprocess.run(command,check=True)
    subprocess.run(['zstd','-q','-t',str(archive)],check=True)
    members=subprocess.run(['tar','-I','zstd','-tf',str(archive)],capture_output=True,text=True,check=True).stdout
    (dest/'TAR_MEMBER_INDEX.txt').write_text(members)
    parts=[];counter=0
    with archive.open('rb') as fin:
        while True:
            start=fin.read(1)
            if not start:break
            counter+=1
            part=dest/(ARCHIVE+f'.part-{counter:03d}')
            h=hashlib.sha256();size=0
            with part.open('xb') as fout:
                data=start+fin.read(min(2*1024*1024,PART_LIMIT-1))
                while data:
                    fout.write(data);h.update(data);size+=len(data)
                    if size==PART_LIMIT:break
                    data=fin.read(min(2*1024*1024,PART_LIMIT-size))
            parts.append({'name':part.name,'bytes':size,'sha256':h.hexdigest()})
    size=archive.stat().st_size;sha=sha_file(archive)
    assert sum(p['bytes'] for p in parts)==size
    assert parts and all(p['bytes']<=PART_LIMIT for p in parts)
    (dest/'PARTS_MANIFEST.json').write_text(json.dumps({
        'schema':'VOID_HX89_SPLIT_TRANSPORT_VERIFIED_V2','archive_name':ARCHIVE,
        'archive_bytes':size,'archive_sha256':sha,'max_part_size_bytes':PART_LIMIT,
        'member_entries':len(members.splitlines()),'parts':parts,
        'format':'single compressed tar stream, split into contiguous byte segments',
        'original_uploads_not_modified':True},indent=2)+'\n')
    shutil.copyfile(WORK.parent/'VOID_HX89_WORKPLACE_PARTS_20261029/reassemble.py',dest/'reassemble.py')
    (dest/'README_START_HERE.md').write_text(
        '# VOID / HX89 final verified cumulative source and evidence volume\n\n'
        'Download **every** `.part-###` file and `PARTS_MANIFEST.json` and `reassemble.py` into one directory. '
        'Each part is strictly below 200,000,000 bytes. These parts are contiguous segments of ONE archive, not standalone ZIPs.\n\n'
        '1. Verify first: `python3 reassemble.py --verify-only`\n'
        '2. Reassemble: `python3 reassemble.py`\n'
        '3. Extract: `tar -I zstd -xf '+ARCHIVE+'`\n\n'
        'Extracted tree: `workplace/` with the complete canonical 116 milestone planner, all original archives, '
        'HX89, EntropyAVX, K01–K06 netlists, native CPU/HX89/reversible model sources, logs, failed attempts, '
        'bounded watchdog, independent tests, and SHA-256 inventories.\n\n'
        '**Engineering scope:** Full 12-gate real native/toolchain acceptance and separately verified 64-cycle full-stack '
        'run are included. A physically controlled analog/nonbinary CPU substrate remains unverified.\n')
    (dest/'SHA256SUMS.txt').write_text('\n'.join(p['sha256']+'  '+p['name'] for p in parts)+'\n'+sha+'  '+ARCHIVE+'\n')
    # Reassembling from parts is tested with the same public verifier.
    subprocess.run([sys.executable,str(dest/'reassemble.py'),'--verify-only'],check=True)
    print(json.dumps({'archive_bytes':size,'archive_sha256':sha,'parts':parts,
                      'archive_member_entries':len(members.splitlines())},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('PACKAGING FAILED:',exc,file=sys.stderr);sys.exit(1)
