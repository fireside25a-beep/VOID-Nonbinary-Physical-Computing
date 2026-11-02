#!/usr/bin/env python3
"""Generate only descriptive plots from real saved CSV and canonical ledger.

Does not synthesize analog values, infer transistor voltages, or alter raw evidence.
"""
from __future__ import annotations
import csv, json, collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'09_RESULTS_VISUALS'
RAW=ROOT/'05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/04_whole_machine_288_native_cross_core'
LEDGER=ROOT/'00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv'

def main():
    OUT.mkdir(exist_ok=True)
    for hold in (5,50):
        path=RAW/f'hold_{hold}ms.csv'
        with path.open(newline='') as f: rows=list(csv.DictReader(f))
        groups=[[int(r['read_ns'])/1e6 for r in rows if int(r['intensity'])==i] for i in (0,1,2)]
        fig,ax=plt.subplots(figsize=(9,5.2))
        ax.boxplot(groups, tick_labels=['Idle','Partial scalar','Full AVX2'],showfliers=True)
        ax.set_ylabel('Readout routine elapsed time (ms)')
        ax.set_title(f'Real CPU readout after {hold} ms hold — n={len(rows)}')
        ax.set_xlabel('Preceding native CPU workload intensity')
        ax.grid(axis='y',alpha=.25)
        fig.tight_layout()
        fig.savefig(OUT/f'cpu_three_intensity_hold_{hold}ms.png',dpi=155)
        fig.savefig(OUT/f'cpu_three_intensity_hold_{hold}ms.svg')
        plt.close(fig)
        paired=[]
        for j in range(0,len(rows),3):
            trio={int(r['intensity']):int(r['read_ns'])/1e6 for r in rows[j:j+3]}
            if len(trio)==3:paired.append(trio[2]-trio[0])
        fig,ax=plt.subplots(figsize=(9,4.5))
        ax.plot(range(1,len(paired)+1),paired,marker='.',linestyle='none')
        ax.axhline(0,linewidth=1)
        ax.set_xlabel('Randomized balanced triplet')
        ax.set_ylabel('Full AVX2 minus idle readout time (ms)')
        ax.set_title(f'Paired CPU history contrast, hold {hold} ms (no reproducible level established)')
        ax.grid(axis='y',alpha=.25)
        fig.tight_layout()
        fig.savefig(OUT/f'cpu_history_paired_{hold}ms.png',dpi=155)
        fig.savefig(OUT/f'cpu_history_paired_{hold}ms.svg')
        plt.close(fig)
    with LEDGER.open(newline='') as f: rec=list(csv.DictReader(f,delimiter='\t'))
    counts=collections.Counter(r['roadmap_phase'] for r in rec)
    fig,ax=plt.subplots(figsize=(10,5.2))
    ax.barh(list(counts.keys()),list(counts.values()))
    ax.set_xlabel('Number of original milestones')
    ax.set_title('Original 116 VOID milestones by historic roadmap phase')
    for i,amount in enumerate(counts.values()):ax.text(amount+.3,i,str(amount),va='center')
    ax.set_xlim(0,max(counts.values())+8)
    fig.tight_layout()
    fig.savefig(OUT/'canonical_116_milestones.png',dpi=160)
    fig.savefig(OUT/'canonical_116_milestones.svg')
    plt.close(fig)
    print('Generated 10 files, charts use real CSV / authoritative ledger only.')

if __name__=='__main__': main()
