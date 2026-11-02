#!/usr/bin/env python3
"""Generate ONE cumulative milestone/status ledger from unmodified source."""
from pathlib import Path
from hashlib import sha256
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]
master=ROOT/'00_CONTROL/VOID_HX89_EXPANDED_MASTER_INPUT_COPY_PASTE_20261029.txt'
src=ROOT/'02_ACTIVE_R08/05_MILESTONES/VOID_R08_FULL_116_MILESTONE_CROSSWALK.tsv'
with src.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
ids=[r['id'] for r in rows]
assert ids==[f'M{i:02d}' for i in range(116)], 'Missing/duplicate/out-of-order milestone ID'
s=master.read_text()
assert all(re.search(r'^'+i+r' \| ',s,re.M) for i in ids),'Missing original master appendix row'
# A physical milestone cannot be completed by digital code or the current netlist.
software={'M00':('ARCHIVE_VERIFICATION','original intake SHA/ZIP CRC and inventory recorded'),
 'M07':('CPU_INSTRUCTION_MEASURED','RDSEED/RDRAND success, native SIMD exactness and timing digitally observed'),
 'M31':('CPU_PROBE_EXECUTED','CPUID capabilities and virtualized host documented'),
 'M32':('CPU_INSTRUCTION_MEASURED','CPU native code measured, no raw analog port established'),
 'M46':('HX89_TESTS_EXECUTED','HX89 complete make check; source now present and re-executed'),
 'M53':('NO_MATERIAL_OPERATOR_PROOF','K06 circuit netlist only'),
 'M55':('NO_MULTILEVEL_PHYSICAL_PROOF','No measured stable multilevel cell'),
 'M60':('DIGITAL_FEEDBACK_ONLY','CPU instrument -> HX89 target, no physical K06 loop'),
 'M63':('BVH_DEFECT_REPAIRED','Derived EntropyAVX BVH verified by differential/stress tests'),
 'M78':('NO_PHYSICAL_RETENTION_PROOF','No raw physical write/hold/read trace'),
 'M84':('DEVELOPMENT_WATCHDOG_TESTED','Isolated research-cache watchdog passes 10 checks'),
 'M88':('NO_BOARD_SAFETY_TEST','R08 source protection components only'),
 'M113':('NO_CPU_NONBINARY_MEMORY','No actual multi-level on-die writable material state verified'),
 'M115':('RELEASE_BLOCKED','Required physical and complete machine gates unverified')}
# Supplement historical ledger with independently executed, current-session receipts.
# Never promote a model/netlist or conditioned digital entropy to a material proof.
receipt_path=ROOT/'04_TESTS_AND_LOGS/20261029_RESUMED/VOID_CPU_HX89_BATCH_EXECUTION.json'
watchdog_path=ROOT/'04_TESTS_AND_LOGS/20261029_RESUMED/watchdog_latest_summary.json'
if receipt_path.is_file() and watchdog_path.is_file():
 rec=json.loads(receipt_path.read_text()); wd=json.loads(watchdog_path.read_text())
 if rec.get('status')=='NATIVE_CPU_AND_HX89_EXECUTED' and wd.get('all_execution_gates_passed') and wd.get('failed')==0 and not rec.get('physical_nonbinary_substrate_verified'):
  n=rec['cpu']['rounds']*4; cycles=len(rec['hx89_feedback'])
  software.update({
   'M07':('NATIVE_CPU_ENTROPY_INSTRUCTIONS_EXECUTED',f'Conditioned RDRAND/RDSEED outputs observed in {n} real native trials; no raw analog noise sensed'),
   'M31':('NATIVE_CPU_INTERVENTION_EXECUTED',f'{n} pinned native scalar/AVX2/AVX512/cache interventions and instruction observations; hypervisor present'),
   'M32':('MICROARCHITECTURAL_TIMING_OBSERVED',f'{n} actual TSC pre/post readings with strict CPU migration checks; observed timing is not thermometry'),
   'M46':('HX89_NATIVE_Q2_FEEDBACK_EXECUTED',f'{cycles} executed HX89 Q2 feedback cycles, plus full make check PASS'),
   'M60':('HX89_DIGITAL_OBSERVATION_LOOP_EXECUTED',f'{cycles} CPU-measured timing-derived control values consumed by native HX89; K06 physical coupling remains unproved'),
   'M63':('AVX_ENGINE_AND_BVH_RETESTED', 'Native 60-frame AVX2/SNN engine, 3003 BVH build/refits, and crossover interventions executed'),
   'M84':('BOUNDED_WATCHDOG_EXECUTED',f"{wd['passed']}/{wd['tasks']} bounded execution gates PASS, each with persisted result receipt"),
  })
else:
 raise RuntimeError('Expected executable work receipts missing: refuse to regenerate a falsely up-to-date planner')
# Reconcile only independently verified WHOLE-STACK real execution receipts.
# Historical source columns remain untouched, and no material claim is promoted.
stack_root=ROOT/'04_TESTS_AND_LOGS/20261029_FULL_STACK_64'
stack_record=stack_root/'FULL_STACK_EXECUTION.json'
stack_receipt=None
if stack_record.is_file():
 import sys
 sys.path.insert(0,str(ROOT/'03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE'))
 from verify_full_stack import assert_verified as verify_real_stack
 stack_receipt=verify_real_stack(stack_root)
 if stack_receipt['verified_cycles']!=64 or stack_receipt['verified_cpu_interventions']!=256:
  raise RuntimeError('Unexpected full-stack execution scope; do not promote ledger')
 software.update({
  'M31':('NATIVE_BATCH_AND_FULL_STACK_REEXECUTED','64 real full-stack cycles, 256 native scalar/SIMD/cache interventions, source/binary and CPU migration verified'),
  'M32':('REAL_EXECUTION_TIMINGS_AND_CONTROLS_VERIFIED','64 measured physical-instruction timing events accepted by HX89 Q² controller; TSC is not raw analog current'),
  'M46':('HX89_LATERAL_AND_CLOSED_STACK_EXECUTED','5D, Q², phase, native JIT, snapshot/recovery, 64 reversible lattice-gas paths and generated Polyforms actually executed'),
  'M60':('HX89_TWO_WAY_DIGITAL_CLOSED_LOOP_VERIFIED',f"64 measured CPU->HX89 Q²->HexGas->HX89->next CPU cycles; {stack_receipt['command_changed_cycles']} real command changes; no K06 physical coupling"),
  'M63':('REAL_BATCH_SIMD_AND_AVX_ENGINE_RETESTED','256 real CPU interventions plus repaired EntropyAVX 60-frame native execution, 3003 BVH cases'),
  'M84':('WATCHDOG_AND_INDEPENDENT_READBACK_EXECUTED',f"11 original watchdog gates + {stack_receipt['verified_cycles']} full-stack source/trace/feedback readback gates")})
mechanisms={
'M07':'Entropy instructions are conditioned outputs, not raw physical noise',
'M31':'CPU-feature census: CPUID + hypervisor flag; architecture-specific, host-bound',
'M32':'Discriminate CPU instruction effects from genuine analog observables',
'M38':'Measure thermally sensitive dynamics and rule out clock/scheduler confounders',
'M39':'Causal intervention and independently observed physical state',
'M43':'Power and energy readings require calibrated independent counters/sensors',
'M46':'HX89 full 5D/Q2/native/HexGas/reversible lifecycle and artifacts',
'M47':'Charge / phase / current as physical operands with independently verified stability',
'M51':'Constrain/measure AC/DC nonlinear junction behavior and model error',
'M52':'Multi-node coupled fluctuations, not isolated scalar noise or hash values',
'M53':'Collective/batch operator with real material transfer function',
'M54':'Graph-wide simultaneous charge/resonance coupling, not digital table lookup',
'M55':'Reproducible distinguishable physical levels under perturbation',
'M59':'Select novel physically causal operation and independently reproduce it',
'M60':'HX89 native -> measured material actuation -> measured readback -> HX feedback',
'M63':'SIMD AVX2/AVX512, cache-local reproducibility/energy baseline, no ontology promotion',
'M78':'Actual physical write/hold/read and relaxation/retention',
'M80':'Independent stimuli jointly measured through collective substrate',
'M84':'Bounded recursive-check developer watchdog, isolated from substrate',
'M93':'Real RLC resonance response vs calibrated prediction',
'M95':'Actual on-die vs external entropy source distinction',
'M97':'Noise-to-resonator causal coupling with false controls',
'M99':'Physical mechanism accepted only on actual intervention and independent measurement',
'M104':'Typed physically measured observables and uncertainties',
'M105':'Held-out trace forecast only after real acquisition',
'M113':'Scalable physical nonbinary memory; guard against ordinary encoding',
'M114':'Power/output/current/thermal interlocks physically validated',
'M115':'End-to-end general-purpose CPU-native physical nonbinary machine acceptance'}
for r in rows:
 status,evidence=software.get(r['id'],('NOT_NEWLY_VERIFIED','Historical state preserved; no new implementation evidence in this session'))
 r['current_execution_status']=status
 r['current_evidence_summary']=evidence
 r['physical_nonbinary_completion']='NOT_VERIFIED'
 r['cpu_hx89_void_unified_substep']=mechanisms.get(r['id'],'Preserve original dependencies and test against existing source before future integration')
 r['last_evidence_date']='2026-10-29' if r['id'] in software else ''
 r['historical_fields_preserved']='YES'
out=ROOT/'00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv'
with out.open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n');wr.writeheader();wr.writerows(rows)
# Full original appendix not summarized away: 116 rows in canonical document.
md=['# VOID / HX89 canonical cumulative implementation planner','',
'Authoritative R08 original statuses/dependencies are preserved exactly in CANONICAL_IMPLEMENTATION_LEDGER.tsv. This is ONE planner, not a new project branch.','',
'## Proof gates','',
'1. Preserve the original archive and sealed source history byte-exact; verify sha/CRC, as-found full-milestone inventory.','2. Re-execute source suites (HX89 5D, Q², reversible hex gas, chiral finite proofs, native W^X/return; EntropyAVX with BVH/launcher stress; research watchdog).',
'3. Verify native CPU mechanisms as actual host instructions: entropy, SIMD, register use, L1/L2 sample working sets and timestamps. Characterize what is observable and falsify confounders. Digital counters/RNG words are NOT raw thermal or quantum measurements.',
'4. Source-trace K01–K06 physical netlists and all referenced libraries; reject orphan components, double loading, unsourced measurements, hidden digital substitutes.',
'5. Test causally connected collective AC/DC multi-node material operations, nonlinear interaction and write/hold/read; DO NOT equate SPICE/analog formula with physical operation.',
'6. Demonstrate HX89 command -> physically verified coupled substrate stimulus -> independent material readout -> HX89 return. Actual available instrumentation and intervention required; missing hardware is a NOT VERIFIED gate.',
'7. Scale simultaneous nonbinary material states, memory, recovery, full input and output, stable higher-level workloads, meta-universe persistence, safety and independent reproducibility.',
'8. Build reproducible release records and failure-preserving benchmarks before promoting M115.','',
'## Seven-system coupled hypothesis (requirements to test, not accomplishments)','',
'| System | Native component | Established now | Missing physical causal gate |',
'|---|---|---|---|',
'| On-die stochastic entropy | CPU RDRAND/RDSEED | Digital conditioned output under hypervisor | controllable underlying continuous state and verified quantum contribution |',
'| AVX2 / AVX-512 | CPU SIMD integer execution | Instruction availability and scalar equality | actually influence, then sense, nonbinary state |',
'| L1/L2 | native cache working-set activity | TSC timing of 32 KiB/512 KiB scan | independently establish residency, physical state and causal control |',
'| Clock/power | instruction execution activity | no physical rail/thermal measurement | safe measured power/clock feedback |',
'| Thermal timing | timestamps | TSC deltas measured | distinguish noise from hypervisor/scheduler/frequency |',
'| HX89 5D/Q² | source native accelerator + tests | executable digital semantic bridge | physical substrate transition verified |',
'| VOID K06 | joined SPICE design and pads | netlist cards/topology | actual assembled electrically coupled material response |',
'',
'## Native meta-universe and machine completeness',
'Transactions, memory identity, causal history, recovery, index/search, concurrent associations, security, replication, provenance and physical state durability remain real requirements. SQLite research cache is independent development metadata only; NOT VOID runtime. End goal includes startup, programmable control, display, inputs/outputs, sensors, actuators and actual workloads. No single hash or scalar demo qualifies.','',
'## Whole-stack real execution addendum — 2026-10-29',
'',
'New non-destructive derivative `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/full_stack_cycle.py` executed 64 native CPU/HX89 cycles, including 256 real scalar/SIMD/cache interventions, real 5D and Q² native machine paths, an actual finite reversible six-channel Boolean lattice-gas MODEL in C, 64 emitted Polyforms executed by HX89, and snapshot/resume. The executed HX89 outputs alter subsequent CPU machine-workload commands, rather than a shadow predictor changing them. Independent `verify_full_stack.py` checks every saved image, source and binary hash, actual Polyform output, feedback chain and 64 cycle receipts; `test_full_stack.py` attacks corrupted logs and mismatched control. These are meaningful software/native integrations, not new on-die continuous analog or K06 charge operations.',
'',
'No continuous CPU transistor gate bias was accessed, no measured sub-threshold leakage was acquired, and no physical K06 board was connected. The desired collective nonbinary material computation/memory still requires independently proven physical intervention, analog dynamics, retention, scalable batch operation and reliable machine I/O. Historical fields and milestones are unchanged.',
'',
'Execution logs: `04_TESTS_AND_LOGS/20261029_FULL_STACK_64/FULL_STACK_EXECUTION.json`, with 64 per-round source/native/HX89 traces and gas PGM images; suite logs in `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/`.',
'',
'## Historical milestone-by-milestone implementation and evidence',
'']
for r in rows:
 md += [f"### {r['id']} — {r['original_title']}",
 f"Historical phase: {r['roadmap_phase']}. Historical source status: {r['original_source_status']}. Dependence: {r['original_dependency']}.",
 f"Original R08 evidence class: {r['void_r05_verified_scope']}. Historical source: `{r['supporting_file_or_baseline']}`.",
 f"Current execution: **{r['current_execution_status']}**. {r['current_evidence_summary']}.",
 f"Physical nonbinary completion: **NOT VERIFIED**. Gate: {r['next_evidence_for_physical_completion']}.",
 f"Integrated candidate/substep: {r['cpu_hx89_void_unified_substep']}.",""]
(ROOT/'00_CONTROL/CANONICAL_MASTER_PLAN.md').write_text('\n'.join(md))
# Distinct file inventory for the active netlist and preserved comparison baseline.
files=sorted((ROOT/'02_ACTIVE_R08/02_PHYSICAL_CIRCUITS').glob('*'))
with (ROOT/'00_CONTROL/ACTIVE_NETLIST_INVENTORY.tsv').open('w',newline='') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['file','bytes','sha256','external_includes'])
 for p in files:
  if p.is_file():
   included=';'.join(re.findall(r'^\s*\.include\s+"([^"]+)"',p.read_text(),re.I|re.M))
   w.writerow([p.name,p.stat().st_size,sha256(p.read_bytes()).hexdigest(),included])
print('MILESTONES',len(rows),'NETLISTS',len(files),'MASTER_BYTES',master.stat().st_size,'CANONICAL_PLAN_BYTES',(ROOT/'00_CONTROL/CANONICAL_MASTER_PLAN.md').stat().st_size)
