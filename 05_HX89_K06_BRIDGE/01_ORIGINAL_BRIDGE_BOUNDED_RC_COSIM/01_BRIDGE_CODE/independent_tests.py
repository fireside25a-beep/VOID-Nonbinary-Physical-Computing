#!/usr/bin/env python3
"""Separate unit, numerical, physical-model-limitation and native truth-table tests."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path
import numpy as np
from k06_rc import Network,spice_number,NETLIST,MESH,CORE,MESH_ELEMENTS,extract,ROOT
from native_bridge import native_program,evaluate_hx89,BINARY,EXPECTED_BINARY,sha

output=ROOT/'05_TESTS_AND_AUDITS'/'independent_unit_tests'
output.mkdir(parents=True,exist_ok=True)
results=[]
def check(name,predicate,detail=''):
 good=bool(predicate)
 results.append({'test':name,'pass':good,'detail':str(detail)})
 print(('PASS' if good else 'FAIL'),name,detail,flush=True)
 return good

check('native_binary_sha256',sha(BINARY.read_bytes())==EXPECTED_BINARY,EXPECTED_BINARY)
check('parse_10meg',spice_number('10meg')==1e7)
check('parse_100n',abs(spice_number('100n')-1e-7)<1e-18)
check('parse_10mH_scalar',spice_number('10m')==1e-2)
try:spice_number('100bork');check('invalid_spice_units_rejected',False)
except ValueError:check('invalid_spice_units_rejected',True)

# Validate direct source consistency and expected source topology.
N=Network();check('source_components_exact_count',len(N.elements)==40,len(N.elements))
check('write_A_source_path',any(e.name=='C_WRITE_A_COUPLING' and {e.a,e.b}=={'WRITE_A','WRITE_INJ_A'} and e.value==1e-8 for e in N.cap))
check('write_B_source_path',any(e.name=='C_WRITE_B_COUPLING' and {e.a,e.b}=={'WRITE_B','WRITE_INJ_B'} and e.value==1e-8 for e in N.cap))
check('charge_reciprocal_coupling',any(e.name=='R_CHARGE_COUPLE' and {e.a,e.b}=={'CHARGE_A','CHARGE_B'} for e in N.res))
check('three_distinct_stored_states',all(x in N.nodes for x in ('CHARGE_A','CHARGE_B','CHARGE_C')))
check('open_switch_is_real_component_removal',not any(e.name=='C_WRITE_A_COUPLING' for e in Network(source_open_a=True).elements))

# Direct independent nodal KCL residual after each backward-Euler step.
def residual(net,prior,oldfixed,dt):
 x=net.state;g=net.g;c=net.c
 return np.max(np.abs(g@x+(c@(x-prior))/dt-net.rhs_fixed(net.res,net.fixed_v)-
       (net.rhs_fixed(net.cap,net.fixed_v)-net.rhs_fixed(net.cap,oldfixed))/dt))
N=Network();pr=N.state.copy();of=N.fixed_v.copy()
N.step(.0004,1.2,0.)
err=residual(N,pr,of,.0004)
check('implicit_KCL_residual_small',err<1e-9,err)
check('charge_A_responds_to_electrode',abs(N.snapshot()['CHARGE_A'])>1e-6,N.snapshot()['CHARGE_A'])
check('capacitor_energy_nonnegative',N.energy_joules()>=0)
for _ in range(200):N.step(.0004,0.,0.)
check('passive_zero_input_energy_decays',N.energy_joules()<1e-9,N.energy_joules())

# Distinct input electrodes from same initial state must yield distinct node
# responses, not a hard-coded lookup or parser-based outcome.
a=Network();b=Network();
for _ in range(20):a.step(.0004,1.2,0.);b.step(.0004,0.,1.2)
xa=a.snapshot();xb=b.snapshot()
check('electrode_intervention_changes_A',abs(xa['CHARGE_A']-xb['CHARGE_A'])>1e-3,(xa['CHARGE_A'],xb['CHARGE_A']))
check('electrode_intervention_changes_B',abs(xa['CHARGE_B']-xb['CHARGE_B'])>1e-3,(xa['CHARGE_B'],xb['CHARGE_B']))

# Broken path must be silent in zero-biased subnetwork.
o=Network(source_open_a=True)
for _ in range(20):o.step(.0004,1.2,0.)
check('broken_write_A_has_no_charge_A_or_B',abs(o.snapshot()['CHARGE_A'])<1e-14 and abs(o.snapshot()['CHARGE_B'])<1e-14)

# Time step refinement (backward Euler converges on consistent solution).
fast=Network();slow=Network()
for _ in range(40):fast.step(.0002,1.2,0.)
for _ in range(80):slow.step(.0001,1.2,0.)
err_time=abs(fast.snapshot()['CHARGE_A']-slow.snapshot()['CHARGE_A'])
check('time_refinement_convergence',err_time<0.002,err_time)

# Four native Polyform decisions on real HX89, including native code-trace sum.
for ai in (0,1):
 for bi in (0,1):
  d=output/f'bits_{ai}{bi}';d.mkdir(exist_ok=True)
  run=evaluate_hx89(native_program(ai,bi),d/'sense.hx',0,d)
  check(f'HX89_NATIVE_ADC_TRUTH_{ai}{bi}',run['native_sum']==ai+bi and run['native_bit']==int(ai or bi),run)

# Gate refusal is observed from actual binary; no fake/mock native engine.
cp=subprocess.run([str(BINARY),str(output/'bits_11'/'sense.hx'),'1','1000'],capture_output=True,timeout=8)
(output/'without_native_gate.stdout').write_bytes(cp.stdout)
(output/'without_native_gate.stderr').write_bytes(cp.stderr)
check('native_execution_gate_rejects',b'requires --native' in cp.stdout+cp.stderr and b'NATIVE_ACCEL epoch=' not in cp.stdout,
      {'returncode':cp.returncode,'stdout':cp.stdout.decode(errors='replace')})

summary={'tests':len(results),'passed':sum(x['pass'] for x in results),
         'failed':sum(not x['pass'] for x in results),'results':results,
         'physical_device_proof':False,'full_ngspice_proof':False}
(output/'tests.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ('tests','passed','failed')},indent=2))
raise SystemExit(0 if summary['failed']==0 else 1)
