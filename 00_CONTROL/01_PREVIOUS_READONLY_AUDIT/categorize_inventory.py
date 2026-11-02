#!/usr/bin/env python3
"""Conservative *path-derived* categories. Does not infer scientific proof."""
from pathlib import Path
from collections import Counter
import csv,json
D=Path(__file__).resolve().parent
source=list(csv.DictReader((D/'MEMBER_INVENTORY.csv').open()))
def tag(r):
 a=r['archive'];p=r['name']; low=p.lower(); ext=r['extension']
 if a.startswith('04_R08'):
  fam='VOID';sub='R08 physical circuit release'
  if '/01_PRESERVED_INPUTS/' in p:sub='historical R01-R07, DACB/BCSE and preserved original inputs';lin='PRESERVED_HISTORY'
  elif '/02_PHYSICAL_CIRCUITS/' in p: sub='R08 active circuit netlists and libraries';lin='ACTIVE_DESIGN_SOURCE'
  elif '/03_CONNECTION_AND_LAYOUT/' in p:sub='R08 layout, topology, BOM and pin maps';lin='DESIGN_DOCUMENTATION'
  elif '/04_MEASUREMENT_AND_PROOF/' in p:sub='R08 evidence gates and blank physical forms';lin='PROOF_PROTOCOL_NOT_MEASUREMENT'
  elif '/05_MILESTONES/' in p:sub='116-milestone history / crosswalk';lin='PLANNER'
  elif '/06_INTEGRITY/' in p:sub='static validation and preserved reports';lin='HISTORICAL_TEST_RECEIPT'
  else:lin='DOCUMENTATION'
 elif a.startswith('06_MASTER'):
  fam='HX89/MASTER';lin='ORIGINAL_REFERENCE_OR_HANDOFF'
  if '/04_HX89_USER_SUPPLIED_SOURCE_AND_EXISTING_INTAKE/' in p:sub='HX89 original repository, research and intake'
  elif '/05_ENTROPY_AVX_SEPARATE_SOURCE_AND_TRACE/' in p:sub='EntropyAVX separate source trace/reference'
  elif '/03_DACB_BCSE_ORIGINAL_INPUTS/' in p:sub='DACB, BCSE and AC/DC original preserved inputs'
  elif '/09_NEW_CHAT_AIO_HANDOFF/' in p:sub='duplicated historical handoff and documentation'
  else:sub='historical master and research'
 elif a.startswith('07_HX89'):
  fam='NATIVE_TOOLCHAIN';lin='EXECUTABLE_SOURCE_OR_BUILD_SNAPSHOT'
  if '/HX89/' in p:sub='HX89 original native VM, Q2, lattice and tests'
  elif '/EntropyAVX/' in p:sub='EntropyAVX FIXED DERIVATIVE and build outputs'
  elif '/CPU_VOID_BATCH_CYCLE/' in p:sub='x86 scalar/AVX/cache native feedback research'
  elif '/ResearchCache/' in p:sub='research-cache branch and tests'
  else:sub='other native tooling'
 elif a.startswith('08_ALL'):
  fam='WORKPLACE_LOGS';lin='HISTORICAL_RUN_OR_CONTROL_RECORD'
  if '/00_CONTROL/' in p:sub='watchdog/planner/runner and source ledger'
  elif '/04_TESTS_AND_LOGS/' in p:sub='historical raw receipts, outputs and failures'
  elif '/05_EVIDENCE/' in p:sub='CPU material-gate evidence and falsification'
  elif '/06_RELEASE_CONTROL/' in p:sub='release manifests, rebuild and state reports'
  elif '/07_DELIVERY/' in p:sub='delivery status reports'
  elif '/08_DOCUMENTATION/' in p:sub='research and reproduction documentation'
  elif '/09_RESULTS_VISUALS/' in p:sub='graphs and plot scripts'
  elif '/90_PRESERVED_PROVENANCE/' in p:sub='historical snapshots retained'
  else:sub='workplace entry points'
 elif a.startswith('09_ACDC'):
  fam='SOURCE_REFERENCE';lin='ORIGINAL_RECONSTRUCTION_OR_MODEL'
  if '/ACDC/' in p:sub='AC/DC passive admittance solver + SPICE decks'
  elif '/AVX/' in p:sub='original EntropyAVX reconstructed source trace'
  else:sub='reference source'
 elif a.startswith('VOID_HX89_K06_BRIDGE'):
  fam='HX89_K06_BRIDGE';lin='BRIDGE_READBACK_ONLY'
  if '/00_README/' in p:sub='claim matrix and scope'
  elif '/01_BRIDGE_CODE/' in p:sub='new source-derived RC co-simulation/controller/test code'
  elif '/02_ORIGINAL_K06_NETLIST/' in p:sub='preserved R08 K06 SPICE original copies';lin='ORIGINAL_K06_SOURCE_COPY'
  elif '/03_HX89_BINARY_ONLY/' in p:sub='preserved HX89 x86-64 runtime binary';lin='ORIGINAL_NATIVE_BINARY'
  elif '/04_EXPERIMENT_LOGS/' in p:sub='model-only analog trajectories and captured HX89 native output'
  elif '/05_TESTS_AND_AUDITS/' in p:sub='negative tests, readback audit and superseded output'
  elif '/06_PHYSICAL_INTERFACE_PLAN/' in p:sub='physical link NOT YET BUILT'
  elif '/07_REPRODUCIBILITY/' in p:sub='manifest and optional full SPICE testbench'
  else:sub='other bridge research'
  if 'superseded_wrong_sign_run' in low or 'superseded_early_sign_error' in low:lin='INVALID_SUPERSEDED_DO_NOT_CITE'
 else:fam='UNCLASSIFIED';sub='unclassified';lin='UNCLASSIFIED'
 if ext in {'.cir','.lib'}:typ='SPICE_NETLIST_OR_MODEL'
 elif ext in {'.c','.cpp','.cc','.h','.hpp','.s','.asm','.py','.sh','.hx','.f90','.nim'}:typ='SOURCE_OR_SCRIPT'
 elif ext in {'.md','.txt','.tex','.pdf'}:typ='DOCUMENT_OR_REPORT'
 elif ext in {'.log','.stderr','.stdout','.actual','.out'}:typ='RUN_LOG_OR_EXPECTED_OUTPUT'
 elif ext in {'.csv','.tsv','.json','.jsonl','.bits','.seed'}:typ='DATA_MANIFEST_OR_RECEIPT'
 elif ext=='.zip':typ='NESTED_ARCHIVE'
 elif ext in {'.png','.svg','.jpg','.wav','.pgm'}:typ='MEDIA_OR_VISUAL'
 elif ext in {'.o','.a','.so','.pyc'}:typ='BUILD_OUTPUT'
 elif ext=='':typ='UNKNOWN_BINARY_OR_TEXT_BY_SUFFIX'
 else:typ='OTHER_ARTIFACT'
 return {'family':fam,'subsystem':sub,'lineage_tag':lin,'type_by_extension':typ}
rows=[]
for r in source: rows.append({**r,**tag(r)})
with (D/'CATEGORIZED_MEMBER_INDEX.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={}
for key in ('family','subsystem','lineage_tag','type_by_extension'):
 summary[key]=dict(Counter(r[key] for r in rows))
with (D/'CATEGORY_COUNTS.json').open('w') as f:json.dump(summary,f,indent=2)
print('categorized',len(rows),'types',summary['type_by_extension'],'families',summary['family'])
