#!/usr/bin/env python3
"""Rebuild all eight exact, byte-verified originally uploaded ZIPs from preserved fragments.
Never overwrites originals; refuses any missing/changed fragment.
"""
from pathlib import Path
import argparse,hashlib,json,sys
BASE=Path(__file__).resolve().parent
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    out=a.output.resolve()
    if out.exists() and any(out.iterdir()):raise SystemExit('REFUSE nonempty destination; exact archives are not overwritten')
    out.mkdir(parents=True,exist_ok=True)
    m=json.loads((BASE/'ORIGINAL_INPUTS_RECONSTRUCTION_MANIFEST.json').read_text())
    for item in m['files']:
        final=out/item['original_name'];tmp=out/(item['original_name']+'.incomplete')
        if final.exists() or tmp.exists():raise SystemExit('REFUSE preexisting archive target '+str(final))
        h=hashlib.sha256();length=0
        with tmp.open('xb') as w:
            for frag in item['fragments']:
                p=BASE/frag['path'];assert p.is_file(),f'missing {p}'
                assert p.stat().st_size==frag['size'] and digest(p)==frag['sha256'],f'invalid fragment {p}'
                with p.open('rb') as f:
                    for b in iter(lambda:f.read(1048576),b''):
                        w.write(b);h.update(b);length+=len(b)
        if length!=item['size'] or h.hexdigest()!=item['sha256']:
            raise SystemExit('INVALID full original hash '+item['original_name'])
        tmp.rename(final)
        print('EXACT_ORIGINAL_PASS',final.name,length,flush=True)
    print('EIGHT_EXACT_ORIGINALS_RECONSTRUCTED',len(m['files']))
if __name__=='__main__':main()
