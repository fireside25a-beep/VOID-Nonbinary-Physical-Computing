#!/usr/bin/env python3
"""Portable, fail-closed reconstruction of the VOID sealed multi-part ZIP release.
Python >=3.9 stdlib only. No shell, external unzip, or destructive overwrite.
Use: python3 reconstruct_void_parts.py RELEASE_PARTS_MANIFEST.json --output /some/new/folder
"""
import argparse,csv,hashlib,io,json,os,stat,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
BLOCK=1024*1024

def hash_stream(src,dst=None):
    digest=hashlib.sha256();length=0
    for part in iter(lambda:src.read(BLOCK),b''):
        digest.update(part);length+=len(part)
        if dst is not None:dst.write(part)
    return digest.hexdigest(),length

def safe_name(name):
    if '\\' in name or '\x00' in name or name.startswith('/'):
        raise ValueError(f'unsafe ZIP name: {name!r}')
    p=PurePosixPath(name)
    if not p.parts or any(x in ('','.','..') for x in p.parts) or p.parts[0]!='VOID':
        raise ValueError(f'unsafe ZIP name: {name!r}')
    return p

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest',type=Path)
    ap.add_argument('--output',type=Path,required=True,help='New destination directory; cannot already exist')
    args=ap.parse_args()
    meta=json.loads(args.manifest.read_text(encoding='utf-8'))
    if meta.get('schema')!='VOID_SPLIT_ARCHIVE_V1' or not isinstance(meta.get('parts'),list) or not meta['parts']:
        raise ValueError('unknown or empty release manifest')
    out=args.output.expanduser().absolute();par=out.parent
    if out.exists():raise FileExistsError(f'refuse existing output: {out}')
    if not par.is_dir():raise FileNotFoundError(f'parent directory missing: {par}')
    root=args.manifest.resolve().parent
    total_parts=0
    with tempfile.TemporaryDirectory(prefix='.void-reassemble-',dir=par) as work:
        work=Path(work);zip_path=work/'release.assembled.zip'
        sha=hashlib.sha256()
        with zip_path.open('wb') as assembled:
            for idx,chunk in enumerate(meta['parts'],1):
                rel=PurePosixPath(chunk['path'])
                if len(rel.parts)!=2 or any(p in ('..','.') for p in rel.parts):
                    raise ValueError('unsafe chunk path')
                path=root.joinpath(*rel.parts)
                if not path.is_file():raise FileNotFoundError(path)
                h=hashlib.sha256();n=0
                with path.open('rb') as src:
                    for block in iter(lambda:src.read(BLOCK),b''):
                        n+=len(block);h.update(block);sha.update(block);assembled.write(block)
                if n!=chunk['bytes'] or h.hexdigest()!=chunk['sha256']:
                    raise ValueError(f'part {idx} failed size/SHA-256 check: {rel}')
                total_parts+=n
        if total_parts!=meta['archive_bytes'] or sha.hexdigest()!=meta['archive_sha256']:
            raise ValueError('assembled archive identity mismatch')
        expected={}
        with zipfile.ZipFile(zip_path) as z:
            raw=z.read('VOID/00_CONTROL/RELEASE_FILE_SHA256.csv').decode('utf-8')
            for row in csv.DictReader(io.StringIO(raw)):
                name=row['relative_path']
                safe_name(name)
                if name in expected:raise ValueError('duplicate manifest path '+name)
                expected[name]=(int(row['bytes']),row['sha256'])
            info_list=z.infolist();seen=set();file_count=0;volume=0
            for entry in info_list:
                pp=safe_name(entry.filename);name=str(pp)
                if name in seen:raise ValueError('duplicate ZIP member '+name)
                seen.add(name)
                mode=(entry.external_attr >> 16)&0xffff
                if stat.S_ISLNK(mode):raise ValueError('symlink prohibited: '+name)
                if entry.is_dir():continue
                file_count+=1;volume+=entry.file_size
                if name=='VOID/00_CONTROL/RELEASE_FILE_SHA256.csv':continue
                if name not in expected:raise ValueError('unmanifested ZIP file '+name)
                if entry.file_size!=expected[name][0]:raise ValueError('size mismatch '+name)
            if file_count!=meta['archive_file_count'] or volume!=meta['uncompressed_bytes']:
                raise ValueError('member/size totals disagree')
            if len(expected)!=file_count-1:raise ValueError('manifest coverage mismatch')
            result=work/'extracted';result.mkdir()
            for entry in info_list:
                name=entry.filename;rel=safe_name(name)
                dest=result.joinpath(*rel.parts)
                if entry.is_dir():dest.mkdir(parents=True,exist_ok=True);continue
                dest.parent.mkdir(parents=True,exist_ok=True)
                with z.open(entry,'r') as src,dest.open('xb') as target:
                    digest,length=hash_stream(src,target)
                if name!='VOID/00_CONTROL/RELEASE_FILE_SHA256.csv' and (digest,length)!=(expected[name][1],expected[name][0]):
                    raise ValueError('file identity mismatch '+name)
                mode=(entry.external_attr>>16)&0o777
                if mode & 0o111:os.chmod(dest,0o755)
                else:os.chmod(dest,0o644)
        # Atomic destination creation only after every member and file hash matches.
        result.rename(out)
        print(json.dumps({'status':'PASS','destination':str(out/'VOID'),'files':file_count,
                          'bytes':volume,'verified_archive_sha256':meta['archive_sha256']}))
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:
        print(f'RECONSTRUCTION_REFUSED: {type(exc).__name__}: {exc}',file=sys.stderr)
        sys.exit(1)
