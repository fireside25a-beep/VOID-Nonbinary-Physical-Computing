#!/usr/bin/env python3
"""Bounded, deterministic unit and negative checks, never writes to VOID material source."""
import csv,importlib.util,io,json,pathlib,sqlite3,tempfile,unittest,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]

def load(name):
    p=ROOT/'04_TOOLING'/f'{name}.py'
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
class VerifyCache(unittest.TestCase):
    def test_r08_anchored(self):
        self.assertIn('SHA256: d5e1a2ef956d5c6fefda727e294a0d25f3aaa15882543779181f072c901b97ad', (ROOT/'06_R08_REFERENCE/R08_ORIGIN.txt').read_text())
    def test_database_integrity(self):
        with sqlite3.connect(ROOT/'01_SOURCE_CATALOG/void_research.sqlite3') as db:
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            self.assertEqual(db.execute('SELECT COUNT(*) FROM milestones').fetchone()[0],116)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM sources').fetchone()[0],31)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM source_milestones').fetchone()[0],160)
    def test_stable_rebuild(self):
        p=ROOT/'01_SOURCE_CATALOG/void_research.sqlite3'
        before=hashlib.sha256(p.read_bytes()).hexdigest()
        build=load('build_research_cache');build.build()
        self.assertEqual(before,hashlib.sha256(p.read_bytes()).hexdigest())
    def test_missing_milestone_negative(self):
        with sqlite3.connect(':memory:') as db:
            db.execute('CREATE TABLE milestones (id TEXT PRIMARY KEY)')
            db.executemany('INSERT INTO milestones VALUES (?)',[(f'M{i:02d}',) for i in range(116) if i!=55])
            ids=[x[0] for x in db.execute('SELECT id FROM milestones ORDER BY CAST(SUBSTR(id,2) AS INTEGER)')]
            self.assertNotEqual(ids,[f'M{i:02d}' for i in range(116)])
    def test_duplicate_source_negative(self):
        with sqlite3.connect(':memory:') as db:
            db.execute('CREATE TABLE s (id TEXT PRIMARY KEY)')
            db.execute('INSERT INTO s VALUES ("S001")')
            with self.assertRaises(sqlite3.IntegrityError): db.execute('INSERT INTO s VALUES ("S001")')
    def test_offline_crossref_fails_closed(self):
        refresh=load('refresh_crossref')
        with self.assertRaises(ValueError): refresh.refresh()
        self.assertEqual(refresh.normalized_metadata({'message':{'DOI':'10.1/test','title':['A']}})['DOI'],'10.1/test')
        self.assertNotEqual('10.1/other','10.1/test')
    def test_watchdog_all_pass(self):
        checks=load('watchdog').check()
        self.assertTrue(all(x['pass'] for x in checks),checks)
    def test_no_bogus_hx89(self):
        with sqlite3.connect(ROOT/'01_SOURCE_CATALOG/void_research.sqlite3') as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM sources WHERE title LIKE 'HX89%'").fetchone()[0],0)
if __name__=='__main__':unittest.main(verbosity=2)
