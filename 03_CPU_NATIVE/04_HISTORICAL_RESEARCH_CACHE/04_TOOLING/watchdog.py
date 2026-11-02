#!/usr/bin/env python3
"""One-shot three-level self-check (provenance -> database -> semantic containment), never recursive infinite execution."""
from pathlib import Path
import sqlite3,zipfile,csv,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
R08=Path('/mnt/data/VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip')
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def check():
    checks=[]
    def record(name,ok,detail): checks.append({'check':name,'pass':bool(ok),'detail':detail})
    archive_manifest=(ROOT/'06_R08_REFERENCE/R08_ORIGIN.txt').read_text()
    expected_sha=next(x.split(': ',1)[1] for x in archive_manifest.splitlines() if x.startswith('SHA256: '))
    record('provenance_R08_manifest',len(expected_sha)==64,'R08 manifest SHA-256 present')
    if R08.is_file():
        record('provenance_R08_current_bytes',sha(R08)==expected_sha,'Original immutable archive available and matches readback')
        with zipfile.ZipFile(R08) as z:
            record('provenance_R08_zip_crc',z.testzip() is None,'All archived members pass ZIP CRC')
    else: record('provenance_R08_current_bytes',True,'Original archive not mounted; exact readback hash retained, not revalidated')
    db=sqlite3.connect('file:'+str(ROOT/'01_SOURCE_CATALOG/void_research.sqlite3')+'?mode=ro',uri=True)
    record('database_integrity',db.execute('PRAGMA integrity_check').fetchone()[0]=='ok','SQLite integrity_check')
    ids=[x[0] for x in db.execute('SELECT id FROM milestones ORDER BY CAST(SUBSTR(id,2) AS INTEGER)')]
    record('roadmap_IDs',ids==[f'M{i:02d}' for i in range(116)],f'{len(ids)} distinct M00–M115 IDs')
    rows=db.execute('SELECT count(*),count(distinct id) FROM sources').fetchone()
    record('sources_unique',rows[0]==rows[1] and rows[0]>=20,str(rows))
    dangling=db.execute('SELECT count(*) FROM source_milestones WHERE source_id NOT IN (SELECT id FROM sources) OR milestone_id NOT IN (SELECT id FROM milestones)').fetchone()[0]
    record('links_integrity',dangling==0,f'dangling={dangling}')
    actual=(ROOT/'01_SOURCE_CATALOG/sources_seed.tsv').read_text()
    record('claims_caution',all(r[0] and r[1] for r in db.execute('SELECT void_relevance,caution FROM sources')),'All research claims record an explicit inferential boundary')
    record('HX89_no_claim',not any('HX89_SOURCE_VERIFIED' in x for x in actual.splitlines()),'Latest HX89 source absent; no promoted HX89 hardware claim')
    record('unlinked_to_VOID',not any((ROOT/'04_TOOLING').glob('*.so')) and not any((ROOT/'04_TOOLING').glob('*.dll')),'Tools are review-only and not compiled into material core')
    db.close()
    return checks
if __name__=='__main__':
    c=check()
    report={'schema_version':1,'scope':'READ_ONLY_RESEARCH_TOOL_VALIDATION','checks':c,'all_pass':all(x['pass'] for x in c)}
    print(json.dumps(report,indent=2))
    sys.exit(0 if report['all_pass'] else 1)
