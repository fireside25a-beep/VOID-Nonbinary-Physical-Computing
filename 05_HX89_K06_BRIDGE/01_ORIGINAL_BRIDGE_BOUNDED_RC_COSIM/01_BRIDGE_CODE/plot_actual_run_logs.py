#!/usr/bin/env python3
"""Plot real saved solver logs; these are NOT physical instrument readings."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'05_TESTS_AND_AUDITS'/'figures'
OUT.mkdir(exist_ok=True)
scenarios=['closed_loop','open_write_a','forced_a','no_excitation']
for signal in ['charge_a_v','charge_b_v']:
 plt.figure(figsize=(10,4.5))
 for scenario in scenarios:
  p=ROOT/'04_EXPERIMENT_LOGS'/scenario/'analog_waveforms.csv'
  with p.open() as f:r=list(csv.DictReader(f))
  plt.plot([float(x['time_s'])*1000 for x in r],[float(x[signal])*1000 for x in r],label=scenario,linewidth=1.3)
 plt.title(f'Limited K06 R/C co-simulation — {signal}; NOT measured hardware')
 plt.xlabel('Simulated time (ms)');plt.ylabel('Source-derived simulated node potential (mV)')
 plt.legend(ncol=2,fontsize=8)
 plt.tight_layout();plt.savefig(OUT/f'{signal}_controlled_interventions.png',dpi=150)
 plt.close()
print('Plots written from existing analog_waveforms.csv; no instrument readings claimed')
