#!/usr/bin/env python3
"""Render strictly from the accepted native run JSON; no invented data."""
import json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
here=Path(__file__).resolve().parent
root=here.parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else root/'04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/LATEST_ACCEPTED_REPEATED_NATIVE.json'
r=json.loads(src.read_text())
if len(r.get('executions',[]))!=2:raise SystemExit('Two real receipts required')
data=r['executions']
if any(x['failed']!=0 or x['passed']!=24 for x in data):raise SystemExit('No claim of complete PASS with failed runs')
fig,ax=plt.subplots(figsize=(8,4.5))
labels=['Execution 1','Execution 2']
ax.bar(labels,[x['passed'] for x in data])
for i,x in enumerate(data):ax.text(i,x['passed']+.2,f"{x['passed']}/{x['stages']} completed",ha='center',va='bottom')
ax.set_ylim(0,27)
ax.set_ylabel('Executed verification gates passed')
ax.set_title('VOID/HX89: two sequential native whole-machine regressions')
ax.text(0.5,-0.19,'Does not certify physical nonbinary silicon computation',transform=ax.transAxes,ha='center',fontsize=9)
fig.tight_layout()
fig.savefig(here/'native_repeated_acceptance.png',dpi=170)
fig.savefig(here/'native_repeated_acceptance.svg')
plt.close(fig)
print('Generated from',src)
