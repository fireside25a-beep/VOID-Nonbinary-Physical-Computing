"""Real native CPU measurements and adversarial mutation of those measurements.
No fake hardware frames: negative cases corrupt the output of an actual run.
"""
import csv,shutil,tempfile,unittest
from pathlib import Path
import material_causal as m

class RealMaterialCacheEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='void_actual_cpu_cache_')
        cls.root=Path(cls.temp.name)
        m.compile_native()
        cls.record=m.run_probe(cls.root/'real',256)
        cls.path=cls.root/'real.cache.csv'

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_actual_cpu_cache_causal_effect(self):
        self.assertTrue(self.record['cache_latency_causal_gate'])
        self.assertEqual(m.verify_csv(self.path,256)['trace_sha256'],self.record['trace_sha256'])
        self.assertGreater(self.record['evicted_minus_cached_median_tsc'],20)

    def _corrupt(self,func):
        bad=self.root/(self.id().split('.')[-1]+'.csv')
        with self.path.open(newline='') as f: rows=list(csv.DictReader(f));names=list(rows[0])
        func(rows)
        with bad.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=names);w.writeheader();w.writerows(rows)
        return bad

    def test_adversarial_missing_real_row_is_refused(self):
        bad=self._corrupt(lambda rows:rows.pop())
        with self.assertRaises(ValueError):m.verify_csv(bad,256)

    def test_adversarial_cpu_migration_is_refused(self):
        bad=self._corrupt(lambda rows: rows[5].__setitem__('aux_evicted','999999'))
        with self.assertRaises(ValueError):m.verify_csv(bad,256)

    def test_adversarial_order_rewriting_is_refused(self):
        bad=self._corrupt(lambda rows:[r.__setitem__('order','0') for r in rows])
        with self.assertRaises(ValueError):m.verify_csv(bad,256)

    def test_digital_transport_cannot_be_called_analog_sample(self):
        self.assertTrue(self.record['not_analog_voltage_or_temperature_measurement'])
        self.assertEqual(self.record['cache_provenance'],'REAL_RDTSCP_LOADS_AND_CLFLUSH_COHERENCE')

if __name__=='__main__':unittest.main()
