#!/usr/bin/env python3
"""Compile and test CSV ingestion using synthetic parser fixtures only.

Run: python3 09_PHYSICAL_PROTOTYPE_AND_GATEWAY/native_bench_ingestion/test_csv_schema.py
Optional VOID_BENCH_SOURCE selects an original source for regression comparison.
Nothing here constitutes a physical acquisition or writes archived evidence.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
HEADER = ("sample_index,time_ns,instrument_serial,calibration_id,charge_a_v,"
          "charge_b_v,charge_c_v,probe_a_v,probe_b_v,write_a_v,write_b_v")
ROWS = ["0,100,TEST_ONLY,CAL_TEST,0.1,0.2,0.3,-0.4,0.5,0.6,0.7",
        "1,200,TEST_ONLY,CAL_TEST,0.2,0.3,0.4,-0.3,0.6,0.7,0.8"]


class CsvSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory(prefix="void_parser_test_")
        cls.addClassCleanup(cls.build.cleanup)
        cls.exe = Path(cls.build.name) / "void_bench_ingest"
        source = os.environ.get("VOID_BENCH_SOURCE", str(HERE / "void_bench_ingest.c"))
        subprocess.run(["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                        "-pedantic", "-fstack-protector-strong", "-D_FORTIFY_SOURCE=2",
                        source, "-o", str(cls.exe), "-lcrypto", "-lm"], check=True)

    def invoke(self, rows, newline="\n"):
        folder = tempfile.TemporaryDirectory(prefix="void_SYNTHETIC_csv_")
        self.addCleanup(folder.cleanup)
        source = Path(folder.name) / "fixture.csv"
        receipt = Path(folder.name) / "receipt.txt"
        payload = (newline.join([HEADER] + rows) + newline).encode()
        source.write_bytes(payload)
        result = subprocess.run([str(self.exe), str(source), str(receipt)],
                                capture_output=True, text=True, timeout=5)
        return result, receipt, payload

    def assert_refused(self, rows):
        result, receipt, _ = self.invoke(rows)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("REFUSE", result.stderr)
        self.assertFalse(receipt.exists(), "Refusal must not publish a receipt")

    def test_valid_receipt_and_crlf(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                result, receipt, payload = self.invoke(ROWS, newline)
                self.assertEqual(result.returncode, 0, result.stderr)
                values = dict(line.split("=", 1) for line in receipt.read_text().splitlines())
                self.assertEqual(values["INPUT_SHA256"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(values["RECORDS"], "2")
                self.assertEqual(values["DEVICE_SERIAL"], "TEST_ONLY")
                self.assertEqual(values["CALIBRATION_ID"], "CAL_TEST")
                self.assertEqual(values["LAST_TIME_NS"], "200")
                self.assertAlmostEqual(float(values["MIN_CHARGE_A"]), 0.1)
                self.assertAlmostEqual(float(values["MAX_WRITE_B"]), 0.8)

    def test_extra_empty_columns_every_position(self):
        for position in range(12):
            with self.subTest(position=position):
                malformed = []
                for row in ROWS:
                    fields = row.split(",")
                    fields.insert(position, "")
                    malformed.append(",".join(fields))
                self.assert_refused(malformed)

    def test_missing_values_every_position(self):
        for position in range(11):
            with self.subTest(position=position):
                malformed = []
                for row in ROWS:
                    fields = row.split(",")
                    fields[position] = ""
                    malformed.append(",".join(fields))
                self.assert_refused(malformed)

    def test_existing_rejection_controls(self):
        cases = {
            "header_only": [],
            "one_row": ROWS[:1],
            "nan": [ROWS[0].replace("0.1", "nan"), ROWS[1]],
            "infinity": [ROWS[0].replace("0.1", "inf"), ROWS[1]],
            "duplicate_time": [ROWS[0], ROWS[1].replace("1,200,", "1,100,")],
            "index_gap": [ROWS[0], ROWS[1].replace("1,200,", "2,200,")],
            "changed_calibration": [ROWS[0], ROWS[1].replace("CAL_TEST", "CAL_OTHER")],
            "overvoltage": [ROWS[0].replace("0.6,0.7", "3.3,0.7"), ROWS[1]],
            "extra_nonempty_column": [row + ",1" for row in ROWS],
        }
        for name, rows in cases.items():
            with self.subTest(case=name):
                self.assert_refused(rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
