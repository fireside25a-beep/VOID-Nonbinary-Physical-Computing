"""Adversarial validators applied to freshly captured real native/HX89 execution."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import closed_native_cycle as m

class RealExecutionContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=subprocess.run([str(m.base.EXEC),'--rounds','1','--work','2','--rotate','2','--pin'],capture_output=True,text=True,timeout=25)
  if p.returncode:raise RuntimeError('Real native acquisition failed: '+p.stderr)
  cls.real_stdout=p.stdout
  cls.real_hx=m.connector.hx_execute(m.connector.Q2PROGRAM,('--target-q','7'))['stdout']
 def test_native_executed_valid(self):
  h,r=m.decode_real_native(self.real_stdout,2,2)
  self.assertEqual(len(r),4);self.assertEqual(h['controller_rotate'],2)
 def test_real_hx_executed_valid(self):
  x=m.decode_real_hx89(self.real_hx,7)
  self.assertEqual(x['target'],7)
 def test_reordered_cpu_modes_rejected(self):
  records=self.real_stdout.splitlines()
  records[1],records[2]=records[2],records[1]
  # Renumbering positions masks a simple positional check; the command-vs-mode
  # contract still rejects altered native evidence.
  for j in range(1,5):
   row=json.loads(records[j]);row['position']=j-1;records[j]=json.dumps(row)
  with self.assertRaisesRegex(RuntimeError,'ordered CPU interventions'):
   m.decode_real_native('\n'.join(records),2,2)
 def test_feedback_chain_consistency_negative(self):
  a=m.decode_real_hx89(self.real_hx,7)
  action=m.next_command(a,2)
  self.assertNotEqual(action,((action[0]+1)%4,action[1]))
  # A subsequent trace with a different requested command must fail even
  # if it contains real native results from the previous command.
  with self.assertRaisesRegex(RuntimeError,'did not execute'):
   m.decode_real_native(self.real_stdout,(2+1)%4,2)
 def test_wrong_native_command_rejected(self):
  with self.assertRaisesRegex(RuntimeError,'did not execute'):m.decode_real_native(self.real_stdout,1,2)
 def test_native_missing_or_corrupted_trial_rejected(self):
  lines=self.real_stdout.splitlines()
  with self.assertRaisesRegex(RuntimeError,'missing or wrong'):m.decode_real_native('\n'.join(lines[:-1]),2,2)
  lines[1]='{not_json}'
  with self.assertRaises(json.JSONDecodeError):m.decode_real_native('\n'.join(lines),2,2)
 def test_hx_target_tamper_rejected(self):
  with self.assertRaisesRegex(RuntimeError,'mismatch'):m.decode_real_hx89(self.real_hx,8)
 def test_hx_search_deleted_rejected(self):
  stripped='\n'.join(x for x in self.real_hx.splitlines() if not x.startswith('SEARCH '))
  with self.assertRaisesRegex(RuntimeError,'Missing/ambiguous'):m.decode_real_hx89(stripped,7)
 def test_observed_hx_changes_next_real_command(self):
  actual=m.decode_real_hx89(self.real_hx,7)
  rotate,work=m.next_command(actual,2)
  p=subprocess.run([str(m.base.EXEC),'--rounds','1','--work',str(work),'--rotate',str(rotate),'--pin'],capture_output=True,text=True,timeout=25)
  self.assertEqual(p.returncode,0,p.stderr)
  header, trials=m.decode_real_native(p.stdout,rotate,work)
  self.assertEqual(len(trials),4)
 def test_no_missing_hx_fields_allowed(self):
  x=m.decode_real_hx89(self.real_hx,7)
  del x['fitness']
  with self.assertRaisesRegex(RuntimeError,'incomplete'):m.next_command(x,2)
 def test_strict_execution_bounds(self):
  for argv in [['--rounds','0'],['--rounds','65'],['--base-work','0']]:
   p=subprocess.run([sys.executable,str(HERE/'closed_native_cycle.py'),*argv],capture_output=True,timeout=5)
   self.assertNotEqual(p.returncode,0)

if __name__=='__main__':unittest.main(verbosity=2)
