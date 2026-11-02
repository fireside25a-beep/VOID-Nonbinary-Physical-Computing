#!/usr/bin/env python3
"""Restore/verify entire VOID/HX89 canonical project from <=200MB folder ZIPs.
Pure Python stdlib; no network, no source mutation and no fabricated pass flags.
"""
from __future__ import annotations
import argparse, hashlib, json, os, stat, sys, zipfile
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def require(predicate,message):
    if not predicate:raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--dest',type=Path,default=Path('VOID_HX89_CANONICAL_RESTORED'))
    parser.add_argument('--verify-only',action='store_true')
    opt=parser.parse_args()
    src=opt.source.resolve()
    cand=[src/'03_AUDIT',src]
    audit=next((x for x in cand if (x/'CANONICAL_FOLDER_MANIFEST.json').is_file()),None)
    require(audit is not None,'Missing manifest; extract audit kit at release root.')
    rel=json.loads((audit/'CANONICAL_FOLDER_MANIFEST.json').read_text())
    entries=json.loads((audit/'ALL_FILES_SHA256.json').read_text())
    require(len(entries)==rel['expected_file_count'],'Manifest number of source files differs')
    expected={x['path']:x for x in entries}
    require(len(expected)==len(entries),'Duplicate source paths in inventory')
    sources=[]
    found=set()
    regen=rel['excluded_large_file_to_regenerate']['path']
    for mod in rel['modules']:
        name=mod['name']
        zp=next((x for x in [src/name,src/'02_MODULE_FOLDERS'/name] if x.is_file()),None)
        require(zp is not None,'Missing module: '+name)
        require(zp.stat().st_size==mod['bytes'] and zp.stat().st_size<200_000_000,'Module size invalid: '+name)
        require(sha(zp)==mod['sha256'],'Module SHA256 failed: '+name)
        with zipfile.ZipFile(zp) as z:
            require(z.testzip() is None,'ZIP CRC failed: '+name)
            names=z.namelist()
            require(len(names)==mod['file_count'],'Module count mismatch: '+name)
            for meta in z.infolist():
                relpath=Path(meta.filename)
                require(not relpath.is_absolute() and '..' not in relpath.parts and not meta.is_dir() and
                    relpath.parts[0]=='workplace', 'Unsafe ZIP entry: '+meta.filename)
                require(((meta.external_attr>>16)&0o170000)!=stat.S_IFLNK,'Symlink refused: '+meta.filename)
                require(meta.filename in expected and meta.filename!=regen,'Unregistered source member: '+meta.filename)
                require(meta.filename not in found,'Duplicate ZIP source: '+meta.filename)
                found.add(meta.filename)
        sources.append(zp)
        print('VERIFIED',name,'SHA + CRC',flush=True)
    require(found==set(expected)-{regen},'Member inventory incomplete or inconsistent')
    if opt.verify_only:
        print('PASS: all module ZIP integrity, member coverage and single-source manifest.')
        return 0
    dest=opt.dest.resolve()
    require(not dest.exists(),'Refusing to overwrite destination: '+str(dest))
    dest.mkdir(parents=True)
    for zp in sources:
        with zipfile.ZipFile(zp) as z:
            for meta in z.infolist():
                rec=expected[meta.filename]
                target=dest/meta.filename
                target.parent.mkdir(parents=True,exist_ok=True)
                h=hashlib.sha256()
                total=0
                with z.open(meta) as inp,target.open('xb') as out:
                    while True:
                        b=inp.read(1<<20)
                        if not b:break
                        out.write(b);h.update(b);total+=len(b)
                require(total==rec['size_bytes'] and h.hexdigest()==rec['sha256'],
                    'Extracted member bytes differ: '+meta.filename)
                os.chmod(target,int(rec['mode']) & 0o777)
    for relpath in rel['directory_paths']:
        target=dest/relpath
        require(target.resolve().is_relative_to(dest),'Unsafe recorded directory')
        target.mkdir(parents=True,exist_ok=True)
    spec=rel['excluded_large_file_to_regenerate']
    target=dest/spec['path']
    target.parent.mkdir(parents=True,exist_ok=True)
    require(not target.exists(),'Original master already exists unexpectedly')
    with target.open('xb') as out:
        for relpath in spec['reconstruct_by_concatenating']:
            part=dest/relpath
            require(part.is_file(),'Missing original source split part: '+relpath)
            with part.open('rb') as stream:
                while True:
                    b=stream.read(1<<20)
                    if not b:break
                    out.write(b)
    require(target.stat().st_size==spec['bytes'] and sha(target)==spec['sha256'],
        'Reconstructed original master does not match exact historical SHA')
    os.chmod(target, int(expected[spec['path']]['mode']) & 0o777)
    actual={'workplace/'+x.relative_to(dest/'workplace').as_posix():x for x in (dest/'workplace').rglob('*') if x.is_file()}
    require(set(actual)==set(expected),'Restored file names differ from manifest')
    actualdirs={'workplace/'+x.relative_to(dest/'workplace').as_posix() for x in (dest/'workplace').rglob('*') if x.is_dir()}
    require(actualdirs==set(rel['directory_paths']),'Restored original directory hierarchy differs')
    total=0
    for name,r in expected.items():
        file=actual[name]
        require(file.stat().st_size==r['size_bytes'] and sha(file)==r['sha256'],'Restored byte hash mismatch: '+name)
        total+=file.stat().st_size
    require(total==rel['expected_total_file_bytes'],'Restored total original file bytes differ')
    receipt={'schema':'VOID_HX89_CANONICAL_FRESH_RESTORE_V3','status':'PASS',
             'files':len(expected),'directories':len(actualdirs),'total_file_bytes':total,
             'archive_count':len(sources),
             'historical_master_reassembled_SHA256':spec['sha256']}
    receipt_path=dest/'RESTORE_RECEIPT_OUTSIDE_WORKPLACE.json'
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: restored',len(expected),'exact original files,',total,
          'bytes; complete hierarchy and SHA256 all verified.',flush=True)
    print('WORKPLACE:',dest/'workplace',flush=True)
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as error:
        print('FAIL:',error,file=sys.stderr);sys.exit(1)
