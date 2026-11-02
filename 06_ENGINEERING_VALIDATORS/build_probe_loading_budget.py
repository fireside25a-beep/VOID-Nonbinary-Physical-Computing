#!/usr/bin/env python3
"""Independent source-exact loading analysis for VOID R08/K06 bench instrumentation.
Only local parallel-to-ground R/C contributions are computed. Other K06 coupling
branches remain in network and require full network analysis; never fake full tau.
"""
from __future__ import annotations
import csv,hashlib,json,math,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=R/'01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE'
OUT=R/'09_PHYSICAL_PROTOTYPE_AND_GATEWAY/04_VERIFIED_BOARD_INTERCONNECT'
K='VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir';M='VOID_K_MESH_V1.lib';MAT='VOID_PRIMITIVE_MATERIAL_INTERFACE.lib'
def read_elements(path):
    out={}
    for n,line in enumerate(path.read_text().splitlines(),1):
        cols=line.split()
        if len(cols)>=4 and cols[0][:1].upper() in ('R','C') and not line.lstrip().startswith(('*',';')):
            out[cols[0].upper()]=(cols[1].upper(),cols[2].upper(),cols[3].lower(),n)
    return out
def val(v):
    match=re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+))([a-z]*)',v,re.I)
    if not match:raise ValueError('not a numeric SPICE value: '+v)
    coeff,suf=float(match[1]),match[2].lower()
    pref={'':1,'f':1e-15,'p':1e-12,'n':1e-9,'u':1e-6,'m':1e-3,'k':1e3,'meg':1e6,'g':1e9}
    if suf not in pref:raise ValueError('unknown suffix '+suf)
    return coeff*pref[suf]
def get(src,ref,nets,value):
    e=src.get(ref)
    if e is None or {e[0],e[1]}!=set(nets) or not math.isclose(val(e[2]),value,rel_tol=1e-12):
        raise ValueError(f'source card mismatch {ref}: {e} expected {nets} {value}')
    return e

def main():
    a=read_elements(S/K);m=read_elements(S/M);material=read_elements(S/MAT)
    source_checks=[];out=[]
    for node in ('A','B','C'):
        net='CHARGE_'+node;cap=val(a['C_CHARGE_'+node][2]);
        assert a['C_CHARGE_'+node][:2]==(net,'0')
        leak=get(a,'R_LEAK_'+node,(net,'0'),10e6)
        probe=get(a,'R_MEM_METER_'+node,(net,'0'),10e6)
        req=1/(1/val(leak[2])+1/val(probe[2]));
        # Show only a local shunt loading factor, not global RC dynamics.
        for scenario,rin in [('source-only load',None),('extra 10M DMM accidentally paralleled',10e6),('ADC 1M directly paralleled',1e6)]:
            combined=1/(1/req+(0 if rin is None else 1/rin))
            out.append({'source_node':net,'scenario':scenario,'native_reference_shunt_ohms':f'{req:.9g}',
                        'effective_local_parallel_shunt_ohms':f'{combined:.9g}',
                        'capacitance_F':f'{cap:.9g}',
                        'illustrative_local_shunt_RC_seconds':f'{combined*cap:.9g}',
                        'note':'Only node-to-ground branches; reciprocal K06 couplings excluded from this local-only diagnostic'})
        source_checks.extend([('R_LEAK_'+node,K,leak[3]),('R_MEM_METER_'+node,K,probe[3]),('C_CHARGE_'+node,K,a['C_CHARGE_'+node][3])])
    for node in ('A','B'):
        e=get(m,'R_P'+node,('PROBE_'+node,'0'),1e6)
        c=get(m,'C_P'+node,('PROBE_'+node,'0'),30e-12)
        source_checks.extend([('R_P'+node,M,e[3]),('C_P'+node,M,c[3])])
    for node in ('Y0','Y1'):
        e=get(a,'R_METER_'+node,(node,'0'),10e6)
        source_checks.append(('R_METER_'+node,K,e[3]))
    for n in ('11','12','13','14','21','22','23','24'):
        v=material['R_ACT_'+n];g=material['R_ACT_GUARD_'+n]
        if val(v[2])!=10e6 or val(g[2])!=1e3 or '0' in g[:2]:raise ValueError('material contact/series resistor mismatch')
        if set(g[:2])!={f'PAD_{n}',f'F_{n}'}:raise ValueError('material guard is not the actual pad-to-F series part')
        source_checks += [('R_ACT_'+n,MAT,v[3]),('R_ACT_GUARD_'+n,MAT,g[3])]
    limit=get(a,'R_CURRENT_LIMIT',('SUPPLY','SHUNT_TOP'),3300)
    source_checks += [('R_CURRENT_LIMIT',K,limit[3])]
    power=24**2/val(limit[2]);assert 0.17<power<0.18
    assert len(out)==9 and len(source_checks)==3*3+4+2+8*2+1
    OUT.mkdir(exist_ok=True,parents=True)
    with (OUT/'K06_SOURCE_DERIVED_PROBE_LOAD_BUDGET.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    with (OUT/'K06_LOAD_CONTRIBUTION_SOURCE_LINES.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_reference','source_filename','line']);w.writerows(source_checks)
    report={'schema':'VOID_SOURCE_LOAD_BUDGET_V1','status':'PASS','source_sha256':{x:hashlib.sha256((S/x).read_bytes()).hexdigest() for x in (K,M,MAT)},
      'verified_source_cards':len(source_checks),'local_scenarios':len(out),'charge_node_loads':3,
      'original_mesh_probe_model':'1 Mohm in parallel with 30 pF for each PROBE_A and PROBE_B',
      'accidental_second_DMM_effect':'10 Mohm source shunt plus 10 Mohm real DMM = 5 Mohm, not 10 Mohm',
      'direct_ADC_warning':'AD7606 family analog input 1 Mohm; must NOT directly substitute for electrometer buffer',
      'R_CURRENT_LIMIT_worst_case_W_at_24V':power,
      'strict_scope':'local shunt calculations; NOT full K06 AC/DC transient, no physically measured signal'}
    (OUT/'K06_PROBE_LOADING_CALCULATIONS.json').write_text(json.dumps(report,indent=2)+'\n')
    print('SOURCE_LOAD_CALCULATIONS_PASS',len(source_checks),'actual source cards',len(out),'scenarios','worst_case_W=',round(power,6))
if __name__=='__main__':main()
