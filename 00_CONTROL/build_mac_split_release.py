#!/usr/bin/env python3
"""Create a deterministic self-verifying ZIP then split into GitHub-size parts.
Run outside of concurrently mutating builds/tests. No worktree deletions.
"""
import csv,hashlib,io,json,os,stat,sys,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DEST=Path(os.environ.get('VOID_RELEASE_DEST','/mnt/data/VOID_RELEASE_SPLIT_FOR_MAC_20261102'))
ARCHIVE=DEST/'VOID_RELEASE_20261102.reassembled.zip'
CHUNK=64_000_000
FIXED=(2026,11,2,0,0,0)
BLOCK=1024*1024

def sha_file(p):
    h=hashlib.sha256();n=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(BLOCK),b''):
            n+=len(b);h.update(b)
    return n,h.hexdigest()

def main():
    if DEST.exists() and any(DEST.iterdir()):
        raise FileExistsError('Refuse overwrite of populated release destination')
    DEST.mkdir(parents=True,exist_ok=True)
    paths=sorted(x for x in R.rglob('*') if x.is_file())
    manifest=[]
    for path in paths:
        if path.is_symlink():raise ValueError('no symlinks allowed '+str(path))
        rel='VOID/'+path.relative_to(R).as_posix()
        size,sha=sha_file(path)
        manifest.append((rel,size,sha,path))
    # Internal manifest is virtual. It cannot recursively include its own hash.
    out=io.StringIO();w=csv.writer(out,lineterminator='\n')
    w.writerow(['relative_path','bytes','sha256'])
    for rel,size,sha,_ in manifest:w.writerow([rel,size,sha])
    internal=out.getvalue().encode('utf-8')
    with zipfile.ZipFile(ARCHIVE,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for rel,size,sha,path in manifest:
            zi=zipfile.ZipInfo(rel,FIXED)
            zi.create_system=3
            zi.external_attr=(stat.S_IFREG|(0o755 if path.stat().st_mode&0o111 else 0o644))<<16
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.flag_bits=0x800
            with z.open(zi,'w',force_zip64=True) as dst,path.open('rb') as src:
                found=hashlib.sha256();length=0
                for chunk in iter(lambda:src.read(BLOCK),b''):
                    dst.write(chunk);found.update(chunk);length+=len(chunk)
                if found.hexdigest()!=sha or length!=size:
                    raise ValueError('source changed during packaging: '+rel)
        zi=zipfile.ZipInfo('VOID/00_CONTROL/RELEASE_FILE_SHA256.csv',FIXED)
        zi.create_system=3;zi.external_attr=(stat.S_IFREG|0o644)<<16
        zi.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(zi,internal)
    # Read and validate compressed ZIP member CRC (not just container SHA256).
    with zipfile.ZipFile(ARCHIVE) as z:
        bad=z.testzip()
        if bad:raise ValueError('ZIP member CRC failed '+bad)
        if len(z.namelist())!=len(manifest)+1:raise ValueError('unexpected ZIP member count')
    parts=[];h=hashlib.sha256();count=0
    with ARCHIVE.open('rb') as stream:
        while True:
            index=count+1
            folder=DEST/f'PART_{index:02d}';folder.mkdir(exist_ok=False)
            name=f'VOID_RELEASE_20261102.zip.part{index:03d}'
            dest=folder/name
            hasher=hashlib.sha256();n=0
            with dest.open('wb') as dst:
                left=CHUNK
                while left:
                    block=stream.read(min(BLOCK,left))
                    if not block:break
                    dst.write(block);h.update(block);hasher.update(block);n+=len(block);left-=len(block)
            if not n:
                dest.unlink();folder.rmdir();break
            parts.append({'path':dest.relative_to(DEST).as_posix(),'bytes':n,'sha256':hasher.hexdigest()});count+=1
    size=ARCHIVE.stat().st_size
    assert size==sum(x['bytes'] for x in parts) and size<=count*CHUNK
    whole=sha_file(ARCHIVE)[1]
    if whole!=h.hexdigest():raise ValueError('split stream checksum incorrect')
    data={'schema':'VOID_SPLIT_ARCHIVE_V1','archive_name':ARCHIVE.name,'archive_bytes':size,
          'archive_sha256':whole,'archive_file_count':len(manifest)+1,
          'uncompressed_bytes':sum(x[1] for x in manifest)+len(internal),
          'part_size_ceiling_bytes':CHUNK,'parts':parts}
    (DEST/'RELEASE_PARTS_MANIFEST.json').write_text(json.dumps(data,indent=2)+'\n')
    from shutil import copy2
    copy2(R/'90_HISTORY/03_ALTERNATE_SEALED_ARCHIVE_RECONSTRUCTOR/reconstruct_void_parts_SINGLE_ARCHIVE_FORMAT.py',DEST/'reconstruct_void_parts.py')
    (DEST/'README_MAC_RECONSTRUCTION.txt').write_text('VOID/HX89 R08 complete source and evidence volume.\n'
      'Copy RELEASE_PARTS_MANIFEST.json, reconstruct_void_parts.py and EVERY PART_nn folder to one directory.\n'
      'Run: python3 reconstruct_void_parts.py RELEASE_PARTS_MANIFEST.json --output ~/Desktop/VOID_RECONSTRUCTED\n'
      'Do not rename or re-order the part files. The reassembler independently checks each part SHA-256,\n'
      'full archive SHA-256, ZIP member CRC, individual extracted file hashes, safe paths, and completeness.\n'
      'This is a byte reconstruction on macOS; included Linux x86-64 binaries require a compatible system for execution.\n'
      'Do not push the temporary assembled ZIP to GitHub; upload extracted source tree or the numbered sub-100 MB archive chunks.\n')
    print(json.dumps({'status':'PACKAGE_PASS','files':len(manifest),'chunks':len(parts),'archive_bytes':size,'archive_sha256':whole}))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('PACKAGING_FAILED',repr(e),file=sys.stderr)
        sys.exit(1)
