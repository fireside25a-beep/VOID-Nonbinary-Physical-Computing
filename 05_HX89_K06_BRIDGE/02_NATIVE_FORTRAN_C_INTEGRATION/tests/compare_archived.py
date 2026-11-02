#!/usr/bin/env python3
"""Independent comparison ONLY, never part of live Fortran/C feedback loop."""
from pathlib import Path
import csv, json, math, hashlib, sys
new=Path(sys.argv[1]);old=Path(sys.argv[2]);out=Path(sys.argv[3]);report={};bad=False
for scenario in ['closed_loop','closed_loop_repeat','open_write_a','no_excitation','forced_a','inverted_action','open_write_b']:
    with (new/(scenario+'_trajectory.csv')).open() as f: n=list(csv.DictReader(f))
    with (old/scenario/'analog_waveforms.csv').open() as f: h=list(csv.DictReader(f))
    with (new/(scenario+'_native.csv')).open() as f: nn=list(csv.DictReader(f))
    with (old/scenario/'native_steps.csv').open() as f: hh=list(csv.DictReader(f))
    checks={}
    if not (len(n)==len(h)==1152 and len(nn)==len(hh)==96):bad=True
    maxdif=0;max_rel=0;offender=[]
    for i,(a,b) in enumerate(zip(n,h)):
        for k in ['time_s','drive_a_v','drive_b_v','charge_a_v','charge_b_v','charge_c_v','probe_a_v','probe_b_v','energy_j']:
            delta=abs(float(a[k])-float(b[k]));maxdif=max(delta,maxdif)
            r=delta/max(1e-12,abs(float(b[k])));max_rel=max(r,max_rel)
            if delta>1e-8 and len(offender)<5:offender.append((i,k,delta))
        if int(a['step'])!=int(b['step']) or int(a['substep'])!=int(b['substep']):bad=True
    nerrs=[];control_errors=[]
    for i,(a,b) in enumerate(zip(nn,hh)):
        for ak,bk in [('adc_a','adc_a'),('adc_b','adc_b'),('native_sum','native_sum'),('native_bit','native_bit')]:
            if a[ak]!=b[bk]:control_errors.append((i,ak,a[ak],b[bk]))
        for ak,bk in [('observed_charge_a_v','observed_charge_a_v'),('observed_charge_b_v','observed_charge_b_v')]:
            if abs(float(a[ak])-float(b[bk]))>1e-8:nerrs.append((i,ak))
    scenario_ok=not offender and not nerrs and not control_errors and len(n)==1152 and len(nn)==96
    bad=bad or not scenario_ok
    report[scenario]={'pass':scenario_ok,'native_calls':len(nn),'state_samples':len(n),'max_abs_difference':maxdif,'max_relative_difference':max_rel,'offenders':offender,'control_conflicts':control_errors,'charge_conflicts':nerrs}
result={'schema':'VOID_FORTRAN_C_VS_ARCHIVED_PYTHON_RC_V1','all_pass':not bad,'scenarios':report}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':not bad,'scenario_summary':{k:{'pass':v['pass'],'max_abs_difference':v['max_abs_difference']} for k,v in report.items()}},indent=2))
sys.exit(0 if not bad else 1)
