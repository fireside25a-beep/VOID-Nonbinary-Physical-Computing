#!/usr/bin/env python3
"""Actual-path, negative and integrity checks; no synthesized passing observations."""
import copy, importlib.util, json, subprocess, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('batch_bridge',HERE/'batch_bridge.py'); b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.fixture=Path(__file__).resolve().parents[2]/'04_TESTS_AND_LOGS/20261029_RESUMED/native_batch_smoke.jsonl'
  content=[json.loads(x) for x in cls.fixture.read_text().splitlines()]
  cls.header,cls.rows=content[0],content[1:]
 def test_valid_actual_native_traces(self):
  self.assertEqual(len(b.analyze(self.rows,self.header)),4)
 def test_missing_trial_rejected(self):
  with self.assertRaisesRegex(RuntimeError,'trial count'):b.analyze(self.rows[:-1],self.header)
 def test_fake_zero_observation_rejected(self):
  a=copy.deepcopy(self.rows);a[0]['post_ticks']=0
  with self.assertRaisesRegex(RuntimeError,'invalid TSC'):b.analyze(a,self.header)
 def test_migration_rejected(self):
  a=copy.deepcopy(self.rows);a[0]['processor_id_post']=4567
  with self.assertRaisesRegex(RuntimeError,'migration'):b.analyze(a,self.header)
 def test_missing_mode_rejected(self):
  a=copy.deepcopy(self.rows);a[0]['mode']='avx2'
  with self.assertRaisesRegex(RuntimeError,'interventions'):b.analyze(a,self.header)
 def test_native_bounds_rejected(self):
  for argv in [['--rounds','0'],['--rounds','129'],['--work','201'],['--invalid']]:
   p=subprocess.run([str(b.EXEC),*argv],capture_output=True,text=True,timeout=10)
   self.assertNotEqual(p.returncode,0)
 def test_original_milestone_fields(self):
  self.assertEqual(b.check_master()['milestone_ids'],116)
 def test_netlist_integrity(self):
  sys.path.insert(0,str(b.CONN.parent));import connector
  z=connector.k06_contract();self.assertEqual(len(z['netlist_sha256']),64)
 def test_real_hx89_native(self):
  sys.path.insert(0,str(b.CONN.parent));import connector
  z=connector.native_trace();self.assertEqual(z['native_ir'],4);self.assertEqual(z['native_result'],122)
if __name__=='__main__':unittest.main(verbosity=2)
