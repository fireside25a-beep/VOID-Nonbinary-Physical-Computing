#!/usr/bin/env python3
"""Cross-platform exact ZIP reconstruction: Python 3 stdlib only.
All output bytes are checked against the published SHA-256 manifest; every part
is verified before any file is written. No path traversal, symlinks or overwrite.
"""
from __future__ import annotations
import argparse,hashlib,json,os,stat,sys,zipfile
from pathlib import Path,PurePosixPath

def checksum(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def safe_name(s):
    p=PurePosixPath(s)
    if not s.startswith('VOID/') or '\\' in s or p.is_absolute() or any(x in ('..','.','') for x in p.parts) or len(p.parts)<2:
        raise ValueError('invalid ZIP file path '+s)
    return p

def read_tsv(file,columns):
    rows=[]
    for n,line in enumerate(file.read_text().splitlines(),1):
        if not line:continue
        fields=line.split('\t')
        if len(fields)!=columns:raise ValueError(f'{file.name}:{n}: wrong number of columns')
        rows.append(fields)
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--parts-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,help='Must be absent or empty; extracted VOID/ goes here')
    ap.add_argument('--verify-only',action='store_true')
    args=ap.parse_args()
    base=args.parts_dir.resolve()
    parts=read_tsv(base/'PARTS_SHA256.tsv',3)
    manifest=read_tsv(base/'FILES_SHA256.tsv',3)
    expected={}
    for p,size,sha in manifest:
        safe_name(p)
        if p in expected:raise ValueError('duplicate manifest path: '+p)
        expected[p]=(int(size),sha)
    seen=set()
    # Scan all input hashes and ZIP CRCs before doing anything destructive.
    for name,size,sha in parts:
        if '/' in name or '\\' in name or not name.endswith('.zip'):raise ValueError('invalid part name')
        f=base/name
        if not f.is_file() or f.stat().st_size!=int(size) or checksum(f)!=sha:
            raise ValueError('missing or corrupted release part: '+str(f))
        if f.stat().st_size>200_000_000:raise ValueError('part above max 200 MB: '+str(f))
        with zipfile.ZipFile(f) as z:
            wrong=z.testzip()
            if wrong:raise ValueError('bad ZIP member CRC: '+str(wrong))
            for member in z.infolist():
                safe_name(member.filename)
                mode=(member.external_attr>>16)&0o170000
                if member.is_dir() or mode not in (0,stat.S_IFREG):raise ValueError('directory/symlink/unsupported ZIP member: '+member.filename)
                if member.filename in seen:raise ValueError('duplicated ZIP member: '+member.filename)
                seen.add(member.filename)
                if member.filename not in expected or member.file_size!=expected[member.filename][0]:
                    raise ValueError('unexpected file/size in ZIP: '+member.filename)
    if seen!=set(expected):
        missing=sorted(set(expected)-seen);raise ValueError('incomplete release: '+str(missing[:5]))
    print('RELEASE_PARTS_VERIFIED',len(parts),'files',len(expected),flush=True)
    if args.verify_only:return
    if args.output is None:raise ValueError('supply --output or --verify-only')
    target=args.output.resolve()
    if target==base or base in target.parents:raise ValueError('output must not be inside parts-dir')
    if target.exists() and any(target.iterdir()):raise ValueError('REFUSE nonempty output destination')
    target.mkdir(parents=True,exist_ok=True)
    count=0
    for name,_,__ in parts:
        with zipfile.ZipFile(base/name) as z:
            for member in z.infolist():
                p=safe_name(member.filename)
                f=target.joinpath(*p.parts)
                f.parent.mkdir(parents=True,exist_ok=True)
                h=hashlib.sha256();length=0
                with z.open(member) as read, f.open('xb') as write:
                    while True:
                        block=read.read(1048576)
                        if not block:break
                        h.update(block);length+=len(block);write.write(block)
                if (length,h.hexdigest())!=expected[member.filename]:
                    raise ValueError('EXTRACTED BYTES DO NOT MATCH: '+member.filename)
                perm=(member.external_attr>>16)&0o777
                if perm:f.chmod(0o755 if perm & 0o111 else 0o644)
                count+=1
    receipt={'schema':'VOID_RELEASE_RECONSTRUCTION_V1','file_count':count,'parts':len(parts),
             'all_file_hashes_verified':True,'original_tree':'VOID/'}
    (target/'RECONSTRUCTION_PASSED.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('RECONSTRUCTION_PASSED',count,'files at',target/'VOID')
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,zipfile.BadZipFile,AssertionError) as err:
        print('RECONSTRUCTION_REFUSED:',err,file=sys.stderr)
        sys.exit(1)
