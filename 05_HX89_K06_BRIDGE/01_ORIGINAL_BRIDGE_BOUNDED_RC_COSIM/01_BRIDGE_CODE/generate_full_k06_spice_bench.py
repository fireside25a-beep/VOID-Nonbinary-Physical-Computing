#!/usr/bin/env python3
"""Prepare true original complete K06 SPICE external PULSE fixture.

Generation is source-driven. Running requires external ngspice. The optional
full nonlinear RLC/BJT/diode simulation is NOT claimed to run in this session.
The original K06 netlist is never edited in place; testbench is a new file.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from k06_rc import ROOT,SOURCE_HASHES

ORIGINAL=ROOT/'02_ORIGINAL_K06_NETLIST'
STAGE=ROOT/'07_REPRODUCIBILITY'/'FULL_K06_SPICE_TESTBENCH'

def prepare():
 STAGE.mkdir(parents=True,exist_ok=True)
 for n,h in SOURCE_HASHES.items():
  b=(ORIGINAL/n).read_bytes()
  if hashlib.sha256(b).hexdigest()!=h:raise RuntimeError('source changed '+n)
  (STAGE/n).write_bytes(b)
 src=(ORIGINAL/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir').read_text()
 if not src.endswith('.OP\n.END\n'):raise RuntimeError('unsafe end-of-netlist substitution')
 base=src[:-len('.OP\n.END\n')]
 stimulus='''
* EXTERNAL AUTOMATED BENCH FIXTURE ONLY — not part of R08 physical build.
* 1.2V transient to each protected pad, independently, bounded below UI_1V8.
V_EXT_A WRITE_A 0 PULSE(0 1.2 1m 1u 1u 3m 8m)
V_EXT_B WRITE_B 0 PULSE(0 1.2 5m 1u 1u 3m 8m)
.control
set wr_singlescale
set wr_vecnames
tran 50u 50m
wrdata FULL_K06_TRANSIENT.dat v(CHARGE_A) v(CHARGE_B) v(CHARGE_C) v(PROBE_A) v(PROBE_B) v(WRITE_A) v(WRITE_B)
quit
.endc
.END
'''
 out=STAGE/'EXTERNAL_BENCH_FULL_K06.cir'
 out.write_text(base+stimulus)
 (STAGE/'GENERATION_SCOPE.json').write_text(json.dumps({
  'created_from_original':str(ORIGINAL/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'),
  'original_sha256':SOURCE_HASHES['VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'],
  'new_stimulus_inserted':True,'original_unchanged':True,
  'physical_board_capture':False,
  'note':'full circuit SPICE deck, separate from LIMITED R/C bridge solver; ngspice not run unless explicitly requested and found',
 },indent=2)+'\n')
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--run',action='store_true',help='actually run ngspice if installed')
 args=p.parse_args()
 path=prepare()
 print('GENERATED',path)
 if args.run:
  binary=shutil.which('ngspice')
  if not binary:raise SystemExit('NO_NGSPICE_INSTALLED: no full-circuit simulation performed')
  cp=subprocess.run([binary,'-b','-o','FULL_K06_SIMULATOR.log',path.name],cwd=STAGE,capture_output=True,timeout=150)
  (STAGE/'NGSPICE_PROCESS.stdout').write_bytes(cp.stdout)
  (STAGE/'NGSPICE_PROCESS.stderr').write_bytes(cp.stderr)
  if cp.returncode:raise SystemExit(f'ngspice failed: {cp.returncode}; inspect process logs')
  data=STAGE/'FULL_K06_TRANSIENT.dat'
  if not data.exists() or data.stat().st_size<100:raise SystemExit('No simulator trace created; cannot claim pass')
  print('NGSPICE_RUN_COMPLETE',data.stat().st_size,'bytes; inspect waveform for physical validity')
 else:print('FULL_SPICE_NOT_EXECUTED: generated only; no physical board instrumented')

if __name__=='__main__':main()
