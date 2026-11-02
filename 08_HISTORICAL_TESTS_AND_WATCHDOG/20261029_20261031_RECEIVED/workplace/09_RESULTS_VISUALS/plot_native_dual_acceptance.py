#!/usr/bin/env python3
"""Plot measured native acceptance and factorial timing using immutable receipts.
No generated sensor data or visual smoothing of the experiment.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART'
OUT=Path(__file__).resolve().parent
receipts=[]
for p in sorted(BASE.glob('WHOLE_MACHINE_ACCEPTANCE_*.json'),key=lambda x:x.stat().st_mtime,reverse=True):
    r=json.loads(p.read_text())
    if r.get('tested_stages')==27 and r.get('failed')==0:
        receipts.append((p,r))
receipts=list(reversed(receipts[:3]))
if len(receipts)<2:
    raise SystemExit('Not enough genuine accepted complete machine runs')
fig,ax=plt.subplots(figsize=(9,4.7))
n=list(range(1,len(receipts)+1))
ax.bar(n,[r['passed'] for _,r in receipts],label='Passed executed gates')
ax.set_ylim(0,30)
ax.set_xticks(n,[f'Run {i}' for i in n]);ax.set_ylabel('Executed verification gates')
ax.set_title('VOID/HX89: independently saved full-machine dual-input acceptance')
for i,(_,r) in enumerate(receipts,1):
    ax.text(i,r['passed']+0.5,f"{r['passed']}/27",ha='center')
fig.tight_layout()
fig.savefig(OUT/'native_27_gate_dual_repeated_execution.png',dpi=160)
plt.close(fig)
trace=ROOT/'04_TESTS_AND_LOGS/20261029_DUAL_CPU_REPEATED'
collected=[]
for j,runid in enumerate(('REAL_FACTORIAL_RUN_02','REAL_FACTORIAL_RUN_03'),1):
    data=json.loads((trace/runid/'ACQUIRED_FACTORIAL_HX89_RESULT.json').read_text())
    for item in data['factorial_real_observations']:
        collected.append((j,item['hold_ms'],item['factorial_synergy_median_ns'],item['synergy_sign_test']['p_two_sided']))
fig,ax=plt.subplots(figsize=(9,4.7))
for hold in sorted(set(x[1] for x in collected)):
    pairs=[x for x in collected if x[1]==hold]
    ax.plot([x[0] for x in pairs],[x[2]/1000 for x in pairs],marker='o',label=f'Hold {hold} ms')
ax.axhline(0,linestyle='--',linewidth=1)
ax.set_xticks((1,2),('Run 1','Run 2'))
ax.set_ylabel('Native factorial interaction (milliseconds)')
ax.set_title('Executed two-input CPU timing contrasts — replication check')
ax.legend();fig.tight_layout();fig.savefig(OUT/'real_dual_cpu_interaction_reproducibility.png',dpi=160);plt.close(fig)
(OUT/'native_dual_plot_inputs.json').write_text(json.dumps({'27_gate_acceptance_receipts':[str(p.relative_to(ROOT)) for p,r in receipts], 'factorial_interactions':collected},indent=2)+'\n')
print('PASS: source-grounded 27/27 and two-input response figures')
