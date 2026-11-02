#!/usr/bin/env python3
"""Independent readback of literal native transcripts, event logs, and control evidence."""
from __future__ import annotations
import csv,hashlib,json,re
from pathlib import Path
from native_bridge import ROOT,EXPECTED_BINARY,sha,NATIVE_RESULT,HALT_RESULT,STIMULUS_V
from k06_rc import Network

SCENARIOS=['closed_loop','closed_loop_repeat','open_write_a','no_excitation','forced_a','inverted_action','open_write_b']
R=ROOT/'04_EXPERIMENT_LOGS'
errors=[];result={};total=0
for sc in SCENARIOS:
 base=R/sc
 s=json.loads((base/'summary.json').read_text())
 steps=list(csv.DictReader((base/'native_steps.csv').open()))
 waves=list(csv.DictReader((base/'analog_waveforms.csv').open()))
 if len(steps)!=96 or len(waves)!=96*12:errors.append(f'{sc}:wrong counts')
 if sha((base/'analog_waveforms.csv').read_bytes())!=s['waveforms_sha256']:errors.append(sc+':waveform hash mismatch')
 for i,row in enumerate(steps):
  total+=1
  program=(base/'generated_polyforms'/f'{i:04d}.hx').read_bytes()
  out=(base/'native_stdout_stderr'/f'{i:04d}.stdout').read_bytes()
  err=(base/'native_stdout_stderr'/f'{i:04d}.stderr').read_bytes()
  if sha(program)!=row['program_sha256']:errors.append(sc+f':polyform#{i}')
  if sha(out)!=row['stdout_sha256'] or sha(err)!=row['stderr_sha256']:errors.append(sc+f':stdout#{i}')
  jit=NATIVE_RESULT.findall(out);final=HALT_RESULT.findall(out)
  if len(jit)!=1 or len(final)!=1:errors.append(sc+f':native-missing#{i}');continue
  aa=int(row['adc_a']);bb=int(row['adc_b'])
  if aa not in (0,1) or bb not in (0,1) or int(jit[0])!=aa+bb or int(final[0][0])!=int(aa or bb):errors.append(sc+f':oracle#{i}')
  if int(row['native_bit'])!=int(aa or bb):errors.append(sc+f':bit#{i}')
  if row['exit_code']!='0' or err:errors.append(sc+f':process#{i}')
  sense_a=float(row['observed_charge_a_v']); sense_b=float(row['observed_charge_b_v'])
  if aa!=int(sense_a>=.006) or bb!=int(sense_b>=.006):errors.append(sc+f':adc sensor#{i}')
  if i>0:
   previous=waves[(i-1)*12+11]
   if abs(float(previous['charge_a_v'])-sense_a)>1e-11 or abs(float(previous['charge_b_v'])-sense_b)>1e-11:errors.append(sc+f':state continuity#{i}')
  for t in range(12):
   wave=waves[i*12+t]
   if int(wave['step'])!=i or int(wave['substep'])!=t:errors.append(sc+f':wave numbering#{i}')
   want_a=float(row['actual_drive_a_v']) if t<9 else 0.
   want_b=float(row['actual_drive_b_v']) if t<9 else 0.
   if float(wave['drive_a_v'])!=want_a or float(wave['drive_b_v'])!=want_b:errors.append(sc+f':DAC-wave mismatch#{i}')
 result[sc]={'native_steps':len(steps),'analog_samples':len(waves),'native_ones':sum(int(x['native_bit']) for x in steps),
             'programs':len(list((base/'generated_polyforms').glob('*.hx'))),
             'stdout_files':len(list((base/'native_stdout_stderr').glob('*.stdout'))),
             'stderr_files':len(list((base/'native_stdout_stderr').glob('*.stderr')))}
# Byte-by-byte rerun includes stdout and stderr, not SHA-only matching.
for i in range(96):
 for suffix in ('.stdout','.stderr'):
  a=(R/'closed_loop'/'native_stdout_stderr'/f'{i:04d}{suffix}').read_bytes()
  b=(R/'closed_loop_repeat'/'native_stdout_stderr'/f'{i:04d}{suffix}').read_bytes()
  if a!=b:errors.append(f'nonidentical replay {i}{suffix}')
if (R/'closed_loop'/'analog_waveforms.csv').read_bytes()!=(R/'closed_loop_repeat'/'analog_waveforms.csv').read_bytes():errors.append('nonidentical analog waveforms')
if sha((ROOT/'03_HX89_BINARY_ONLY'/'hx89').read_bytes())!=EXPECTED_BINARY:errors.append('hx binary changed')
comparison=json.loads((ROOT/'05_TESTS_AND_AUDITS'/'causal_comparison.json').read_text())
if not comparison.get('pass'):errors.append('causal comparison FAILED')
ret={'pass':not errors,'verified_native_runs':total,'verified_waveform_samples':sum(v['analog_samples'] for v in result.values()),
     'native_replay_exact_stdout_and_stderr':True if not any('nonidentical replay' in x for x in errors) else False,
     'cases':result,'errors':errors,'physical_device_test':False,
     'whole_nonlinear_K06_spice_simulation':False,
     'scientific_scope':'native HX89 feedback interacting with independently solved source-derived passive K06 R/C subnetwork only'}
path=ROOT/'05_TESTS_AND_AUDITS'/'independent_readback_report.json'
path.write_text(json.dumps(ret,indent=2)+'\n')
print(json.dumps(ret,indent=2))
raise SystemExit(0 if ret['pass'] else 1)
