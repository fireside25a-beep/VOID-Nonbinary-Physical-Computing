#!/usr/bin/env python3
"""Rebuild review-only SQLite database deterministically. No network and no VOID runtime imports."""
import csv, sqlite3, hashlib, json, pathlib, argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
SEED=ROOT/'01_SOURCE_CATALOG/sources_seed.tsv'
MILESTONES=ROOT/'06_R08_REFERENCE/VOID_R08_FULL_116_MILESTONE_CROSSWALK.tsv'
DEST=ROOT/'01_SOURCE_CATALOG/void_research.sqlite3'
DB_SCHEMA='''
CREATE TABLE sources (id TEXT PRIMARY KEY, year INTEGER NOT NULL, kind TEXT NOT NULL, authors TEXT NOT NULL,
 title TEXT NOT NULL, doi TEXT NOT NULL, url TEXT NOT NULL, review_depth TEXT NOT NULL,
 mechanism TEXT NOT NULL, void_relevance TEXT NOT NULL, caution TEXT NOT NULL);
CREATE TABLE milestones (id TEXT PRIMARY KEY, title TEXT NOT NULL, original_source_status TEXT NOT NULL,
 r08_scope TEXT NOT NULL, dependencies TEXT NOT NULL);
CREATE TABLE source_milestones (source_id TEXT NOT NULL REFERENCES sources(id), milestone_id TEXT NOT NULL REFERENCES milestones(id), PRIMARY KEY(source_id,milestone_id));
CREATE TABLE source_review (source_id TEXT PRIMARY KEY REFERENCES sources(id), reviewed_on TEXT NOT NULL,
 recorded_method TEXT NOT NULL, available_claim_scope TEXT NOT NULL, user_supplied_source INTEGER NOT NULL);
CREATE TABLE research_events (sequence INTEGER PRIMARY KEY, action TEXT NOT NULL, evidence TEXT NOT NULL);
CREATE INDEX idx_sources_year ON sources(year);
CREATE INDEX idx_source_milestone ON source_milestones(milestone_id);
'''
def build():
    with SEED.open(newline='', encoding='utf-8') as f: sources=list(csv.DictReader(f,delimiter='\t'))
    with MILESTONES.open(newline='',encoding='utf-8-sig') as f: milestones=list(csv.DictReader(f,delimiter='\t'))
    ids=[x['id'] for x in milestones]
    assert len(ids)==116 and ids==[f'M{i:02d}' for i in range(116)], 'Milestones missing or unordered'
    assert len(sources)==len({s['id'] for s in sources}) and len(sources)>=20
    assert all(1990 <= int(s['year']) <=2026 and s['url'].startswith('https://') for s in sources)
    db=sqlite3.connect(':memory:')
    db.executescript(DB_SCHEMA)
    db.executemany('INSERT INTO milestones VALUES (?,?,?,?,?)',[(m['id'],m['original_title'],m['original_source_status'],m['void_r05_verified_scope'] if 'void_r05_verified_scope' in m else m.get('void_r08_verified_scope','NOT_RECORDED'),m['original_dependency']) for m in milestones])
    for s in sources:
        db.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?)',(s['id'],int(s['year']),s['type'],s['author'],s['title'],s['doi'],s['url'],s['review_depth'],s['mechanism'],s['void_relevance'],s['caution']))
        for mid in s['milestones'].split(','):
            assert mid in ids,(s['id'],mid)
            db.execute('INSERT INTO source_milestones VALUES (?,?)',(s['id'],mid))
        db.execute('INSERT INTO source_review VALUES (?,?,?,?,0)',(s['id'],'2026-10-29','Public scholarly source search and accessible landing-page/abstract reading',s['review_depth']))
    db.execute('INSERT INTO research_events VALUES (?,?,?)',(1,'source_provenance','R08 SHA from /06_R08_REFERENCE/R08_ORIGIN.txt'))
    db.execute('INSERT INTO research_events VALUES (?,?,?)',(2,'scope_hold','HX89 latest archive pending user attachment; no HX89 claims promoted'))
    db.execute('INSERT INTO research_events VALUES (?,?,?)',(3,'execution_isolation','Research database not imported by K06, DACB or any application runtime'))
    db.commit()
    # deterministically serialize in standard library sqlite backup and VACUUM; disk header SQLite stable but version-specific.
    if DEST.exists(): DEST.unlink()
    disk=sqlite3.connect(DEST)
    db.backup(disk)
    disk.commit(); disk.execute('VACUUM'); disk.commit(); disk.close(); db.close()
    return sources,milestones
if __name__=='__main__':
    ss,mm=build()
    print(json.dumps({'sources':len(ss),'milestones':len(mm),'source_milestone_links':sum(len(x['milestones'].split(',')) for x in ss),'database_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest()},indent=2))
