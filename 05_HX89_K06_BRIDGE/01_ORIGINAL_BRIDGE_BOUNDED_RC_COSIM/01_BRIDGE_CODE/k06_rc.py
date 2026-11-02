#!/usr/bin/env python3
"""Source-locked limited K06 passive R/C subnetwork transient solver.

IMPORTANT: NOT a full ngspice circuit or physical K06 measurement. Extracts named
original R/C components verbatim from preserved R08 K06 .cir and mesh .lib;
solves their linear nodal backward Euler equations with ideal external electrode
voltage testbench. Omitted nonlinear devices, K05 bias, LEDs, BJT, inductors,
and material sheet mean results are ONLY the selected R/C subnetwork.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NETLIST = ROOT/'02_ORIGINAL_K06_NETLIST'/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
MESH = ROOT/'02_ORIGINAL_K06_NETLIST'/'VOID_K_MESH_V1.lib'
SOURCE_HASHES = {
 'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir':'ccfd7ab640ecc54fee5a2414eaca56c920f6c3dd4d1299f1e7f3b61f9c80d161',
 'VOID_K_MESH_V1.lib':'67cb648471f27c4338ceac014f8569753342fd7b59e4aa0f26cccd7de7db3d15',
 'VOID_K05_WEIGHTED_NETWORK.lib':'9a39456a494cef446610149d88faad6e62bcf772094587ad523a37dc30d01ef6',
 'VOID_PRIMITIVE_MATERIAL_INTERFACE.lib':'ae7f5d7ac9e1255d77d58d779150470e433d71925f4191f46b7ecc2f83558839'
}
# Labels are authoritative *as written* by the R08 netlist, not invented equivalents.
CORE = [
 'R_WRITE_A_BLEED','C_WRITE_A_COUPLING','R_WRITE_A_LIMIT',
 'R_WRITE_B_BLEED','C_WRITE_B_COUPLING','R_WRITE_B_LIMIT',
 'R_INTEG_A','C_CHARGE_A','R_LEAK_A',
 'R_INTEG_B','C_CHARGE_B','R_LEAK_B',
 'R_CHARGE_COUPLE','R_FEEDBACK_A','R_FEEDBACK_B',
 'R_INTEG_C','C_CHARGE_C','R_LEAK_C',
 'R_COUPLE_AC','R_COUPLE_BC','R_FEEDBACK_C',
 'R_MEM_METER_A','R_MEM_METER_B','R_MEM_METER_C',
 'R_XY_BUFFER_A','R_XY_BUFFER_B','R_XY_BUFFER_C',
 'R_XY_INSTR_A','R_XY_INSTR_B','R_XY_INSTR_C',
]
MESH_ELEMENTS = ['R_M12','R_MA','R_MB','R_PA','R_PB','C_M12','C_MA','C_MB','C_PA','C_PB']
# Selected resistor-capacitor passive elements are a strict, source-checked
# subnetwork; whole K06 has additional circuits (and additional R/C branches).
SUFFIX={'t':1e12,'g':1e9,'meg':1e6,'k':1e3,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12,'f':1e-15}

def spice_number(s):
 m=re.fullmatch(r'([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)([a-zA-Z]*)',s)
 if not m: raise ValueError(f'invalid scalar: {s!r}')
 suff=m.group(2).lower()
 if suff and suff not in SUFFIX: raise ValueError(f'unsupported suffix: {suff!r}')
 return float(m.group(1)) * SUFFIX.get(suff,1.)

@dataclass(frozen=True)
class Element:
 name:str
 a:str
 b:str
 value:float
 source:str

def extract(filename:Path,labels):
 wanted=set(labels)
 found={}
 for line in filename.read_text().splitlines():
  line=line.strip()
  if not line or line.startswith(('*','.')):continue
  a=line.split()
  if a[0] not in wanted:continue
  if len(a)!=4 or a[0][0] not in 'RC':raise ValueError('bad component: '+line)
  if a[0] in found:raise ValueError('duplicate: '+a[0])
  found[a[0]]=Element(a[0],a[1].upper(),a[2].upper(),spice_number(a[3]),filename.name)
 if set(found)!=wanted: raise ValueError('Missing source components: '+str(sorted(wanted-set(found))))
 return [found[n] for n in labels]

class Network:
 def __init__(self,source_open_a=False, source_open_b=False):
  for name,expected in SOURCE_HASHES.items():
   b=(ROOT/'02_ORIGINAL_K06_NETLIST'/name).read_bytes()
   digest=hashlib.sha256(b).hexdigest()
   if digest!=expected:raise ValueError('source mismatch: '+name+' '+digest)
  self.elements=extract(NETLIST,CORE)+extract(MESH,MESH_ELEMENTS)
  if source_open_a:self.elements=[e for e in self.elements if e.name!='C_WRITE_A_COUPLING']
  if source_open_b:self.elements=[e for e in self.elements if e.name!='C_WRITE_B_COUPLING']
  self.fixed={'0','WRITE_A','WRITE_B'}
  nodes=sorted({n for e in self.elements for n in (e.a,e.b)}-self.fixed)
  self.nodes=nodes; self.idx={name:i for i,name in enumerate(nodes)}
  self.res=[e for e in self.elements if e.name.startswith('R')]
  self.cap=[e for e in self.elements if e.name.startswith('C')]
  self.g=self.stamp(self.res,'R'); self.c=self.stamp(self.cap,'C')
  self.state=np.zeros(len(nodes),dtype=float)
  self.fixed_v={'0':0.0,'WRITE_A':0.0,'WRITE_B':0.0}
  self.t=0.0
  self.results=[]

 def stamp(self,items,kind):
  n=len(self.idx)
  mat=np.zeros((n,n),dtype=float)
  # The fixed voltage source terms are handled by the stamped equivalent of
  # the Dirichlet boundary via stamp_rhs per transient step.
  for e in items:
   k=1/e.value if kind=='R' else e.value
   a=self.idx.get(e.a);b=self.idx.get(e.b)
   if a is not None:mat[a,a]+=k
   if b is not None:mat[b,b]+=k
   if a is not None and b is not None:mat[a,b]-=k; mat[b,a]-=k
  return mat

 def rhs_fixed(self,items,fixed):
  result=np.zeros(len(self.idx),dtype=float)
  for e in items:
   k=(1/e.value) if e.name.startswith('R') else e.value
   ia=self.idx.get(e.a);ib=self.idx.get(e.b)
   if ia is not None and e.b in fixed:result[ia]+=k*fixed[e.b]
   if ib is not None and e.a in fixed:result[ib]+=k*fixed[e.a]
  return result

 def step(self,dt,a,b):
  if not 0<=a<=1.3 or not 0<=b<=1.3:raise ValueError('test voltage outside declared external bench window')
  if dt<=0:raise ValueError('dt<=0')
  old_fixed=self.fixed_v
  new_fixed={'0':0.,'WRITE_A':float(a),'WRITE_B':float(b)}
  cap_old=self.rhs_fixed(self.cap,old_fixed)
  cap_new=self.rhs_fixed(self.cap,new_fixed)
  load=self.rhs_fixed(self.res,new_fixed)
  lhs=self.g + self.c/dt
  rhs=(self.c @ self.state + cap_new - cap_old)/dt + load
  self.state=np.linalg.solve(lhs,rhs)
  self.t+=dt
  self.fixed_v=new_fixed
  if not np.all(np.isfinite(self.state)):raise ArithmeticError('nonfinite K06 RC state')
  return {k:float(self.state[self.idx[k]]) for k in ('CHARGE_A','CHARGE_B','CHARGE_C','PROBE_A','PROBE_B','DISPLAY_X','DISPLAY_Y','DISPLAY_Z')}

 def energy_joules(self):
  vals=lambda n:(self.state[self.idx[n]] if n in self.idx else self.fixed_v[n])
  return float(sum(0.5*e.value*(vals(e.a)-vals(e.b))**2 for e in self.cap))

 def snapshot(self):
  return dict(time_s=self.t,**{k:float(self.state[self.idx[k]]) for k in self.nodes})
