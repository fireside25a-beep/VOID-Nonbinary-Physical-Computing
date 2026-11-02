#!/usr/bin/env python3
"""Make deterministic, independently extractable VOID ZIP parts, each <200MB.
Returns a byte-verifiable, 100% standard-Python Mac reconstruction kit.
The release tree is never modified except its own generated source-file manifest.
"""
from pathlib import Path
import hashlib,json,zipfile,stat,os,shutil,sys,argparse,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=Path('/mnt/data/VOID_MAC_RELEASE_20261102')
CHUNK_BUDGET=165_000_000
MAX_ARCHIVE=200_000_000
INTERNAL=ROOT/'00_CONTROL/RELEASE_CONTENT_SHA256.tsv'

def sha(p):
    d=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):d.update(chunk)
    return d.hexdigest()
def allfiles():return sorted((p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink()),key=lambda x:x.relative_to(ROOT).as_posix())

def main():
    global OUTPUT
    parser=argparse.ArgumentParser(description='Deterministically partition the preserved VOID release; never overwrite an existing package.')
    parser.add_argument('--output',type=Path,default=OUTPUT,help='New, empty destination for independent ZIP parts')
    OUTPUT=parser.parse_args().output.resolve()
    if OUTPUT.exists() and any(OUTPUT.iterdir()):
        raise SystemExit('REFUSE release output nonempty: '+str(OUTPUT))
    OUTPUT.mkdir(parents=True,exist_ok=True)
    entries=[]
    for p in allfiles():
        if p==INTERNAL:continue
        entries.append((str(Path('VOID')/p.relative_to(ROOT)),p.stat().st_size,sha(p),p))
    INTERNAL.write_text(''.join(f'{h}\t{s}\t{n}\n' for n,s,h,_ in entries))
    # A read-only production manifest, derived after writing the internal index.
    entries=[]
    for p in allfiles():entries.append((str(Path('VOID')/p.relative_to(ROOT)),p.stat().st_size,sha(p),p))
    (OUTPUT/'FILES_SHA256.tsv').write_text(''.join(f'{n}\t{s}\t{h}\n' for n,s,h,_ in entries))
    parts=[];pending=[];pending_bytes=0
    def write_part(index,collection):
        name=f'VOID_RELEASE_PART_{index:03d}.zip'
        target=OUTPUT/name
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
            for arc,size,hash_,p in collection:
                info=zipfile.ZipInfo(arc,(2026,11,2,0,0,0))
                info.compress_type=zipfile.ZIP_STORED
                mode=0o755 if os.access(p,os.X_OK) else 0o644
                info.external_attr=(stat.S_IFREG|mode)<<16
                with p.open('rb') as src,z.open(info,'w',force_zip64=size>=0xffffffff) as dest:
                    while True:
                        chunk=src.read(1048576)
                        if not chunk:break
                        dest.write(chunk)
        if target.stat().st_size>=MAX_ARCHIVE:raise ValueError('oversized ZIP '+name)
        checksum=sha(target)
        parts.append((name,target.stat().st_size,checksum,len(collection)))
        print('ZIP_COMPLETE',name,target.stat().st_size,'bytes',len(collection),'source files',flush=True)
    for entry in entries:
        arc,size,_,_=entry
        estimate=size+len(arc)*2+512
        if estimate>=CHUNK_BUDGET:raise ValueError('single oversized member '+arc)
        if pending and pending_bytes+estimate>CHUNK_BUDGET:
            write_part(len(parts)+1,pending);pending=[];pending_bytes=0
        pending.append(entry);pending_bytes+=estimate
    if pending:write_part(len(parts)+1,pending)
    (OUTPUT/'PARTS_SHA256.tsv').write_text(''.join(f'{n}\t{s}\t{h}\n' for n,s,h,c in parts))
    shutil.copy2(ROOT/'00_CONTROL/reconstruct_void_parts.py',OUTPUT/'reconstruct_void_parts.py')
    # A complete archive manifest is not useful if the shipped script speaks a
    # different release format. Execute the actual bundled reader on the freshly
    # generated parts before publishing any release-status PASS receipt.
    verify=subprocess.run([sys.executable,str(OUTPUT/'reconstruct_void_parts.py'),
                           '--parts-dir',str(OUTPUT),'--verify-only'],
                           capture_output=True,text=True,timeout=240)
    if verify.returncode!=0 or 'RELEASE_PARTS_VERIFIED' not in verify.stdout:
        raise RuntimeError('packaged Mac reconstruction verification failed: '+verify.stdout+' '+verify.stderr)
    (OUTPUT/'PACKAGED_RECONSTRUCTOR_VERIFY.log').write_text(verify.stdout+verify.stderr)
    (OUTPUT/'README_MAC_REBUILD.txt').write_text('''VOID — all parts reconstruct the original VOID/ source hierarchy, no merging by hand.\n\n1. Download EVERY VOID_RELEASE_PART_*.zip together with PARTS_SHA256.tsv, FILES_SHA256.tsv and reconstruct_void_parts.py into one directory.\n2. On your MacBook, open Terminal in that directory and run:\n   python3 reconstruct_void_parts.py --parts-dir . --verify-only\n   python3 reconstruct_void_parts.py --parts-dir . --output ./EXTRACTED\n3. Result is ./EXTRACTED/VOID. Every extracted file was checked byte-for-byte by SHA-256; RECONSTRUCTION_PASSED.json reports the total.\n4. Original 04_R08 and 06_HX89 upload archives are retained as verified fragments. To recover full copies without changing the tree:\n   python3 ./EXTRACTED/VOID/91_EXACT_UPLOADED_INPUTS/rebuild_original_archives.py --output ./ORIGINAL_UPLOADS\n5. Do not commit the reconstruction receipt as source. GitHub publish of the full tree is a separate action performed by you; confirm licensing and Git LFS/size constraints for historical large binary assets.\n\nThe native HX89 binary is Linux x86-64; this reconstruction script is portable Python3 and does not require running that binary on Apple Silicon.\n''')
    gates={}
    for k,f in {
        'unified':'07_FRESH_TEST_EVIDENCE/UNIFIED_CANONICAL_ACCEPTANCE_20261102/RESULTS.json',
        'legacy':'07_FRESH_TEST_EVIDENCE/INTEGRATED_RELEASE_GATE/VALIDATION.json',
        'physical_preflight':'07_FRESH_TEST_EVIDENCE/PHYSICAL_PREFLIGHT_20261102/RESULTS.json',
    }.items():
        p=ROOT/f
        if p.is_file():
            data=json.loads(p.read_text());gates[k]={'passed':data.get('passed'),'failed':data.get('failed')}
    summary={'release_root':'VOID','source_file_count':len(entries),'source_bytes':sum(e[1] for e in entries),
             'part_count':len(parts),'part_max_bytes':max(x[1] for x in parts),
             'all_parts_below_200_000_000_bytes':all(x[1]<MAX_ARCHIVE for x in parts),
             'independently_executable_gates':gates,
             'physical_bench_verified':False,'kiCad_ERC_DRC_verified':False,
             'component_capture':{'R08_SPICE_files':9,'R08_SPICE_components':216,'component_pins':459,'K06_flat_primitives':175},
             'do_not_claim':'fabricated PCB, measured nonlinear physical computing, certified compliance, CPU silicon clock control'}
    (OUTPUT/'RELEASE_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('PACKAGE_MANIFEST_COMPLETE',json.dumps(summary),flush=True)
if __name__=='__main__':main()
