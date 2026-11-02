#!/usr/bin/env python3
"""Actual HX89 native x86-64 binary ↔ source-derived K06 R/C subnetwork.

A metered simulated analog voltage -> ADC threshold -> HX89 NATIVE_ACCEL
JIT arithmetic + IFZERO_DIR decision -> physical bench-electrode voltage
boundary -> passive R/C transient response -> next analog sample.

This is a co-simulation harness. It does NOT physically drive a K06 board.
"""
from __future__ import annotations
import csv
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from k06_rc import Network, ROOT, NETLIST, SOURCE_HASHES

BINARY=ROOT/'03_HX89_BINARY_ONLY'/'hx89'
EXPECTED_BINARY='50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451'
STIMULUS_V=1.2
THRESHOLD_V=0.006
INTERVAL_S=0.004
SUBSTEPS=12
NATIVE_RESULT=re.compile(rb'^NATIVE_ACCEL epoch=1 ir=3 bytes=18 result=(\d+) src=[0-9a-f]{16} code=[0-9a-f]{16}$',re.M)
HALT_RESULT=re.compile(rb'^([01])HX89 halt steps=(\d+) heads=(\d+) nodes=(\d+) stack=(\d+) hash=[0-9a-f]{16}$',re.M)

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def native_program(bit_a:int,bit_b:int)->bytes:
 if bit_a not in (0,1) or bit_b not in (0,1):raise ValueError('ADC must produce bit values')
 # A NEW generated program is input to original unmodified HX89 binary.
 # Arithmetic is executed by NATIVE_ACCEL, and IFZERO_DIR uses its result.
 text='\n'.join(['HX87P1',
 '# NEW bridge Polyform; no HX89 engine source is included',
 f'# material ADC inputs charge_A={bit_a} charge_B={bit_b}',
 'CELL 0 0 0 0 0 33 3 0 0',
 f'CELL 1 0 0 0 0 34 {bit_a} 0 0',
 f'CELL 2 0 0 0 0 35 {bit_b} 0 0',
 'CELL 3 0 0 0 0 35 0 0 0',
 'CELL 4 0 0 0 0 23 1 1 0',
 'CELL 5 0 0 0 0 1 49 0 0',
 'CELL 6 0 0 0 0 0 0 0 0',
 'CELL 4 1 0 0 0 1 48 0 0',
 'CELL 4 2 0 0 0 0 0 0 0',
 ])+'\n'
 return text.encode('ascii')

def evaluate_hx89(data:bytes,program:Path,number:int,trace_dir:Path):
 program.write_bytes(data)
 t0=time.perf_counter_ns()
 cp=subprocess.run([str(BINARY),'--native',str(program),'1','1000'],
                   capture_output=True,timeout=8,check=False)
 duration=time.perf_counter_ns()-t0
 (trace_dir/f'{number:04d}.stdout').write_bytes(cp.stdout)
 (trace_dir/f'{number:04d}.stderr').write_bytes(cp.stderr)
 if cp.returncode!=0 or cp.stderr:raise RuntimeError(f'HX89 error step={number} returncode={cp.returncode}, stderr={cp.stderr!r}')
 jit=NATIVE_RESULT.findall(cp.stdout); h=HALT_RESULT.findall(cp.stdout)
 if len(jit)!=1 or len(h)!=1:raise RuntimeError(f'HX89 native trace shape mismatch: {cp.stdout!r}')
 jit_result=int(jit[0]); outcome=int(h[0][0])
 if jit_result not in (0,1,2) or outcome!=int(jit_result>0):
  raise RuntimeError(f'HX89 native branch result inconsistent: {cp.stdout!r}')
 if cp.stdout.count(b'HEXWORLD_ENTER')!=1 or cp.stdout.count(b'HX89 seed=')!=1:raise RuntimeError('invalid native header')
 return {'native_sum':jit_result,'native_bit':outcome,'exit_code':cp.returncode,
         'stdout_sha256':sha(cp.stdout),'stderr_sha256':sha(cp.stderr),
         'program_sha256':sha(data),'duration_ns':duration,
         'stdout_bytes':len(cp.stdout),'stderr_bytes':len(cp.stderr),
         'native_trace_steps':int(h[0][1])}

def run_scenario(name:str,step_count:int=96):
 path=ROOT/'04_EXPERIMENT_LOGS'/name
 path.mkdir(parents=True,exist_ok=True)
 pdir=path/'generated_polyforms';tdir=path/'native_stdout_stderr'
 pdir.mkdir(exist_ok=True);tdir.mkdir(exist_ok=True)
 network=Network(source_open_a=name=='open_write_a',source_open_b=name=='open_write_b')
 results=[];analog=[];measured=[];native_controls=[]
 for n in range(step_count):
  state=network.snapshot()
  va=state['CHARGE_A'];vb=state['CHARGE_B']
  adc_a=int(va>=THRESHOLD_V);adc_b=int(vb>=THRESHOLD_V)
  poly=native_program(adc_a,adc_b)
  native=evaluate_hx89(poly,pdir/f'{n:04d}.hx',n,tdir)
  if native['native_sum']!=adc_a+adc_b or native['native_bit']!=int(adc_a or adc_b):
   raise RuntimeError('independent ADC oracle mismatch at step '+str(n))
  native_controls.append(native['native_bit'])
  # Closed loop: actual native output alone chooses which electrode receives
  # the next pulse. Input is explicitly a simulated analog bench signal.
  selected=int(native['native_bit'])
  if name=='forced_a':selected=0
  if name=='inverted_action':selected=1-selected
  if name=='no_excitation':enable=False
  else:enable=True
  dac_a=float(STIMULUS_V if enable and selected==0 else 0.)
  dac_b=float(STIMULUS_V if enable and selected==1 else 0.)
  # 75% pulse ON + 25% OFF; this is an external testbench stimulation,
  # NOT a waveform source added to the preserved physical K06 netlist.
  for tick in range(SUBSTEPS):
   active=tick<9
   state=network.step(INTERVAL_S/SUBSTEPS,
                      dac_a if active else 0.,dac_b if active else 0.)
   analog.append({'step':n,'substep':tick,'time_s':f"{network.t:.9f}",
        'drive_a_v':dac_a if active else 0.,'drive_b_v':dac_b if active else 0.,
        'charge_a_v':f"{state['CHARGE_A']:.12g}",'charge_b_v':f"{state['CHARGE_B']:.12g}",
        'charge_c_v':f"{state['CHARGE_C']:.12g}",
        'probe_a_v':f"{state['PROBE_A']:.12g}",'probe_b_v':f"{state['PROBE_B']:.12g}",
        'energy_j':f'{network.energy_joules():.12g}'})
  results.append({'step':n,'observed_time_s':f'{n*INTERVAL_S:.9f}',
          'observed_charge_a_v':f'{va:.12g}','observed_charge_b_v':f'{vb:.12g}',
          'adc_a':adc_a,'adc_b':adc_b,'native_bit':native['native_bit'],
          'native_sum':native['native_sum'],'selected_electrode':'B' if selected else 'A',
          'actual_drive_a_v':dac_a,'actual_drive_b_v':dac_b,
          **native})
 for filename,rows in [('native_steps.csv',results),('analog_waveforms.csv',analog)]:
  with (path/filename).open('w',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 summary={'scenario':name,'step_count':step_count,'native_executions':len(results),
          'native_ones':sum(native_controls),'native_zeros':len(results)-sum(native_controls),
          'max_abs_charge_a_v':max(abs(float(row['charge_a_v'])) for row in analog),
          'max_abs_charge_b_v':max(abs(float(row['charge_b_v'])) for row in analog),
          'max_abs_charge_c_v':max(abs(float(row['charge_c_v'])) for row in analog),
          'end_state_v':{k:network.snapshot()[k] for k in ('CHARGE_A','CHARGE_B','CHARGE_C')},
          'analog_samples':len(analog),'all_native_oracle_correct':True,
          'waveforms_sha256':sha((path/'analog_waveforms.csv').read_bytes()),
          'native_steps_sha256':sha((path/'native_steps.csv').read_bytes()),
          'completed_utc':datetime.now(timezone.utc).isoformat()}
 (path/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 return summary,results,analog

def main():
 if sha(BINARY.read_bytes())!=EXPECTED_BINARY:raise RuntimeError('binary mismatch')
 summaries={};runs={}
 for scenario in ('closed_loop','closed_loop_repeat','open_write_a','no_excitation','forced_a','inverted_action','open_write_b'):
  summaries[scenario],steps,analog=run_scenario(scenario)
  runs[scenario]=(steps,analog)
  print(f"{scenario:20s} run={len(steps)} ones={summaries[scenario]['native_ones']} "
        f"A_max={summaries[scenario]['max_abs_charge_a_v']:.6g} B_max={summaries[scenario]['max_abs_charge_b_v']:.6g}",flush=True)
 base=runs['closed_loop'];repeat=runs['closed_loop_repeat']
 # Strip measured process duration from step outputs, compare raw native bytes
 # separately below. The analog waveform CSVs must be bit identical.
 same_analog=(summaries['closed_loop']['waveforms_sha256']==summaries['closed_loop_repeat']['waveforms_sha256'])
 literal_native_equal=all((ROOT/'04_EXPERIMENT_LOGS'/'closed_loop'/'native_stdout_stderr'/f'{i:04d}.stdout').read_bytes()==
   (ROOT/'04_EXPERIMENT_LOGS'/'closed_loop_repeat'/'native_stdout_stderr'/f'{i:04d}.stdout').read_bytes() and
   (ROOT/'04_EXPERIMENT_LOGS'/'closed_loop'/'native_stdout_stderr'/f'{i:04d}.stderr').read_bytes()==
   (ROOT/'04_EXPERIMENT_LOGS'/'closed_loop_repeat'/'native_stdout_stderr'/f'{i:04d}.stderr').read_bytes()
   for i in range(len(base[0])))
 def state_diff(a,b):
  return max(abs(float(x['charge_a_v'])-float(y['charge_a_v']))+
             abs(float(x['charge_b_v'])-float(y['charge_b_v'])) for x,y in zip(runs[a][1],runs[b][1]))
 comparisons={
   'closed_vs_repeat_analog_byte_equal':same_analog,
   'closed_vs_repeat_native_stdout_stderr_byte_equal':literal_native_equal,
   'closed_vs_no_excitation_max_delta_v':state_diff('closed_loop','no_excitation'),
   'closed_vs_open_write_a_max_delta_v':state_diff('closed_loop','open_write_a'),
   'closed_vs_forced_a_max_delta_v':state_diff('closed_loop','forced_a'),
   'closed_vs_inverted_action_max_delta_v':state_diff('closed_loop','inverted_action'),
   'closed_vs_open_write_b_max_delta_v':state_diff('closed_loop','open_write_b'),
   'source_scope':'Strict K06 R/C SUBNETWORK only; not full circuit SPICE or hardware',
   'hardware_physical_capture':'NONE',
   'full_k06_non_linear_SPICE_pass':'NOT_RUN; no ngspice installed',
 }
 comparisons['pass']=(same_analog and literal_native_equal and
                        comparisons['closed_vs_no_excitation_max_delta_v']>1e-4 and
                        comparisons['closed_vs_open_write_a_max_delta_v']>1e-4 and
                        comparisons['closed_vs_forced_a_max_delta_v']>1e-4 and
                        summaries['closed_loop']['native_ones']>0 and
                        summaries['open_write_a']['native_ones']==0 and
                        summaries['no_excitation']['native_ones']==0)
 (ROOT/'05_TESTS_AND_AUDITS'/'causal_comparison.json').write_text(json.dumps(comparisons,indent=2)+'\n')
 (ROOT/'05_TESTS_AND_AUDITS'/'scenario_summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
 print('CAUSAL_COMPARISON',json.dumps(comparisons,indent=2),flush=True)
 return 0 if comparisons['pass'] else 1

if __name__=='__main__':sys.exit(main())
