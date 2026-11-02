"""Adversarial proof gates against changes to REAL crossover and HX89 feedback."""
import csv,shutil,tempfile,unittest
from pathlib import Path
import power_into_hx89 as m

class RealPowerTimingHX89Evidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='void_power_actual_native_')
        cls.root=Path(cls.tmp.name)
        cls.record=m.run(cls.root/'actual',16)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_real_cpu_power_to_hx89_to_cpu_chain(self):
        self.assertEqual(m.verify(self.root/'actual')['power_crossover_trials_verified'],16)
    def test_physical_nonbinary_claim_remains_unverified(self):
        self.assertIs(self.record['physical_thermodynamic_response_verified'],False)
        self.assertTrue(self.record['not_an_independent_temperature_or_power_measurement'])
    def _copy(self):
        dest=self.root/self.id().split('.')[-1]
        shutil.copytree(self.root/'actual',dest)
        return dest
    def test_altered_real_timing_is_rejected(self):
        d=self._copy();p=d/'intervention.power.csv'
        with p.open(newline='') as f:rows=list(csv.DictReader(f));cols=list(rows[0])
        rows[0]['after_busy_tsc']=str(int(rows[0]['after_busy_tsc'])+350)
        with p.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
        with self.assertRaises(ValueError):m.verify(d)
    def test_altered_real_next_cpu_trace_is_rejected(self):
        d=self._copy();p=d/'next_cpu.jsonl';p.write_text(p.read_text().replace('scalar','avx2',1))
        with self.assertRaises(ValueError):m.verify(d)
if __name__=='__main__':unittest.main()
