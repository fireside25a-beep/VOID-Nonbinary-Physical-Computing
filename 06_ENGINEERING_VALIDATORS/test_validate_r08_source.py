#!/usr/bin/env python3
"""Real R08 file verification with deliberately damaged temporary copies as negative controls."""
import json,shutil,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from validate_r08_source import parse,NetlistError,R08_DEFAULT
origin=R08_DEFAULT
for file in sorted(origin.glob('*.cir')):parse(file)
print('PASS all 6 real R08 circuit decks')
with tempfile.TemporaryDirectory() as d:
 dst=Path(d);[shutil.copy2(p,dst/p.name) for p in origin.glob('*')]
 root=dst/'VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir'
 src=root.read_text()
 for label,mutation,marker in [
 ('missing_primitive_library',src.replace('"VOID_PRIMITIVE_MATERIAL_INTERFACE.lib"','"NOT_PRESENT.lib"'),'missing INCLUDE'),
 ('wrong_subckt_pin_count',src.replace('CHARGE_A CHARGE_B FIELD_A FIELD_B AXIS_A AXIS_B VOID_MATERIAL_INPUT','CHARGE_A CHARGE_B FIELD_A AXIS_A AXIS_B VOID_MATERIAL_INPUT'),'expects 10 nodes'),
 ('undefined_transistor_model',src.replace('Q_LIGHT_A LED_A_COL LED_A_BASE LED_A_EMITTER Q_2N3904_NOMINAL','Q_LIGHT_A LED_A_COL LED_A_BASE LED_A_EMITTER Q_UNKNOWN_NPN'),'undefined transistor model'),
 ]:
  root.write_text(mutation)
  try:parse(root)
  except NetlistError as e:
   if marker not in str(e):raise AssertionError(f'{label} unexpected failure: {e}')
   print(f'PASS {label}: rejected source damage')
  else:raise AssertionError(f'{label} falsely accepted damaged circuit')
  root.write_text(src)
print('PASS all 4 structure checks (1 positive + 3 independent negative controls)')
