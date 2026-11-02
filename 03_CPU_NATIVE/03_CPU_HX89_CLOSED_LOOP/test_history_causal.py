"""Native three-intensity CPU history with negative tests mutating REAL measured traces."""
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import history_causal as h
import full_stack_cycle as s
import verify_full_stack as v

class NativeThreeIntensityHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='void_real_three_level_')
        cls.dir=Path(cls.tmp.name)
        h.compile_native()
        cls.probe=h.run_probe(cls.dir/'measured',0x83F17479,2)
        cls.path=cls.dir/'measured.history.csv'

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def mutate(self,name,change):
        with self.path.open(newline='') as f:
            reader=csv.DictReader(f);rows=list(reader);cols=reader.fieldnames
        change(rows)
        target=self.dir/f'{name}.csv'
        with target.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
        return target

    def test_real_native_all_intensities_observed(self):
        self.assertEqual(self.probe['intensity_counts'],[12,12,12])
        self.assertEqual(self.probe['trials'],36)
        self.assertFalse(self.probe['direct_temperature_or_current_observed'])
        self.assertEqual(h.inspect(self.path,2,0x83F17479),{k:v for k,v in self.probe.items() if k not in ('source_sha256','binary_sha256','stdout_sha256','stderr_sha256')})

    def test_reject_missing_real_measurement(self):
        path=self.mutate('missing',lambda rows:rows.pop())
        with self.assertRaises(ValueError):h.inspect(path,2,0x83F17479)

    def test_reject_reordered_real_measurement(self):
        path=self.mutate('reorder',lambda rows:rows[2].__setitem__('intensity','0'))
        with self.assertRaises(ValueError):h.inspect(path,2,0x83F17479)

    def test_reject_tampered_physical_timestamp(self):
        path=self.mutate('invalid',lambda rows:rows[4].__setitem__('post_tsc','0'))
        with self.assertRaises(ValueError):h.inspect(path,2,0x83F17479)

    def test_reject_cpu_migration(self):
        path=self.mutate('migration',lambda rows:rows[5].__setitem__('aux_post_end','999999'))
        with self.assertRaises(ValueError):h.inspect(path,2,0x83F17479)

    def test_reject_predetermined_hardware_claim(self):
        x=dict(self.probe);x['physical_nonbinary_thermodynamic_operator_verified']=True
        with self.assertRaises(ValueError):h.with_observation({'rotate':0,'work':4},x,4)

    def test_hx89_whole_cycle_and_native_history(self):
        destination=self.dir/'actual_full_machine'
        actual=s.run(4,4,destination,history_probe=True)
        self.assertEqual(actual['cycles'],4)
        self.assertEqual(actual['native_trials'],16)
        self.assertEqual(v.assert_verified(destination)['native_three_intensity_trials'],72)
        self.assertFalse(actual['physical_nonbinary_material_computation_verified'])
        # Adversarially change a REAL recorded history delta and require refusal.
        native_csv=destination/'round_001.history.csv'
        data=native_csv.read_bytes()
        try:
            lines=native_csv.read_text().splitlines()
            fields=lines[1].split(',')
            fields[5]='0'
            lines[1]=','.join(fields)
            native_csv.write_text('\n'.join(lines)+'\n')
            with self.assertRaises(ValueError):v.assert_verified(destination)
        finally:native_csv.write_bytes(data)
        # The same original valid evidence must still pass after restoration.
        self.assertEqual(v.assert_verified(destination)['verified_cycles'],4)

if __name__=='__main__':unittest.main()
