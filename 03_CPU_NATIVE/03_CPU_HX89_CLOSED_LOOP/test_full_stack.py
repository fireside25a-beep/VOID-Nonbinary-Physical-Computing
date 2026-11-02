"""Adversarial tests using true saved native executions as test evidence."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import full_stack_cycle as m
import verify_full_stack as verify

class RealFullStackChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(tempfile.mkdtemp(prefix='void_real_stack_tests_'))
  cls.capture=cls.root/'capture'
  cls.real=m.run(4,3,cls.capture)
 @classmethod
 def tearDownClass(cls):
  import shutil
  shutil.rmtree(cls.root)
 def test_cli_relative_output_executes_and_resumes_real_hx89(self):
  # Regression: a relative --out used to be incorrectly joined to snapshot cwd.
  proc=subprocess.run([sys.executable,str(HERE/'full_stack_cycle.py'),'--rounds','4',
                       '--out','relative_stack'],cwd=self.root,text=True,capture_output=True,timeout=25)
  self.assertEqual(proc.returncode,0,msg=proc.stderr+proc.stdout)
  self.assertEqual(verify.assert_verified(self.root/'relative_stack')['verified_cycles'],4)
 def test_actual_full_stack_passes(self):
  self.assertEqual(verify.assert_verified(self.capture)['verified_cycles'],4)
 def test_real_hx89_native_plus_5d_phase_and_persistence(self):
  meta=self.real['hx89_lateral_executions']
  self.assertEqual(meta['native_ir'],4)
  self.assertEqual(len(meta['five_dimensional_hash']),64)
  self.assertGreater((self.capture/'snapshot_isolated/hx89.state').stat().st_size,0)
 def test_actual_lattice_reverse_and_emitted_output(self):
  self.assertTrue(all(x['executed_gas_model_and_hx89']['reverse_verified_by_c_model'] for x in self.real['feedback']))
 def test_invalid_analog_claim_rejected(self):
  report=self.capture/'FULL_STACK_EXECUTION.json'
  original=report.read_bytes()
  try:
   altered=copy.deepcopy(self.real);altered['physical_nonbinary_material_computation_verified']=True
   report.write_text(json.dumps(altered))
   with self.assertRaisesRegex(ValueError,'Unsupported physical claim'):verify.assert_verified(self.capture)
  finally:report.write_bytes(original)
 def test_corrupted_lattice_image_rejected(self):
  target=self.capture/'round_000.gas.pgm'
  original=target.read_bytes()
  try:
   target.write_bytes(original[:-1]+bytes([original[-1]^1]))
   with self.assertRaisesRegex(ValueError,'PGM occupancy impossible|Reported gas profile mismatches image|Gas artifact modified'):verify.assert_verified(self.capture)
  finally:target.write_bytes(original)
 def test_corrupted_hx89_output_rejected(self):
  target=self.capture/'round_000.gas.hx89.stdout.txt'
  original=target.read_bytes()
  try:
   target.write_bytes(original.replace(b'HEXWORLD_ENTER',b'HEXWORLD_FAKE'))
   with self.assertRaisesRegex(ValueError,'Gas artifact modified'):verify.assert_verified(self.capture)
  finally:target.write_bytes(original)
 def test_incorrect_next_cpu_control_rejected(self):
  target=self.capture/'FULL_STACK_EXECUTION.json'
  original=target.read_bytes()
  try:
   data=copy.deepcopy(self.real)
   data['feedback'][0]['next_cpu_control']['rotate']=(data['feedback'][0]['next_cpu_control']['rotate']+1)%4
   target.write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'Causal next command differs'):verify.assert_verified(self.capture)
  finally:target.write_bytes(original)
 def test_truncated_real_cpu_trace_rejected(self):
  target=self.capture/'round_000.native.jsonl'
  original=target.read_bytes()
  try:
   target.write_bytes(b'\n'.join(original.splitlines()[:-1])+b'\n')
   with self.assertRaisesRegex(ValueError,'Native trace byte hash mismatch'):verify.assert_verified(self.capture)
  finally:target.write_bytes(original)
 def test_refuse_unbounded_process(self):
  for n in [0,65]:
   with self.assertRaises(ValueError):m.run(n,3,self.root/f'bad_{n}')
 def test_real_crosscycle_causality(self):
  rows=self.real['feedback']
  for old,new in zip(rows,rows[1:]):self.assertEqual(old['next_cpu_control'],new['requested_cpu_control'])
if __name__=='__main__':unittest.main(verbosity=2)
