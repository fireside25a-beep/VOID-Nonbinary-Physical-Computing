# R08 K06 material carrier: electrical construction and independent source checks

Authoritative source: `01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE/VOID_PRIMITIVE_MATERIAL_INTERFACE.lib`. Generated source-specific CSVs and circuit sheets in this directory are derived exclusively from that file and independently compared with the 175-primitive flattened K06 hierarchy. This carrier is a section of K06, not a separate circuit intended to substitute for the K06 power/charge/diode stages.

## Electrical inventory, kept separate by actual behavior

| Source names | Quantity | Nominal source value | Electrical role |
|---|---:|---:|---|
| `R_ACT_11..14`, `R_ACT_21..24` | 8 | `10meg` | Replaceable electrical contact/FSR model, one from common VREF to its own `PAD_ij`; measure each actual installed contact |
| `R_ACT_GUARD_11..14`, `R_ACT_GUARD_21..24` | 8 | `1k` | Fixed **series** resistance between each `PAD_ij` and `F_ij`; despite its historical name it is NOT a grounded perimeter guard |
| `R_NODE_RET_11..14`, `R_NODE_RET_21..24` | 8 | `220k` | Each `F_ij` returns to common `RET` |
| `R_SHEET_H_11..13`, `R_SHEET_H_21..23` | 6 | `22k` | Horizontal sheet bonds between adjacent columns in each row |
| `R_SHEET_V_11..14` | 4 | `22k` | Vertical bonds between row 1 and row 2 at each column |

These **34 physical resistor/replaceable-contact positions** are identified directly in source. Other material interface resistors (fields, axes and charge/mesh coupling) also exist and are captured in the full editable `.kicad_sch` and full K06 flattened BOM; the two vector sheets do **not** silently replace or omit them from K06's total assembly.

## Source-derived and auditable build maps

- `MATERIAL_CONTACT_PLACEMENT_AND_ROLES.csv`: one source-verified row per contact with fixed series device and return. The `10meg` is a *nominal model value*, not a measured FSR specification.
- `MATERIAL_CONTACT_NET_CONNECTIONS.csv`: source resistor reference, exact `.lib` nodes, exact flattened K06 nodes, value, source file and line, and role for all 34 carrier branches/links.
- `MATERIAL_CARRIER_CONTACT_AND_SHEET.svg`: the eight contact/series branches plus the complete 2×4 sheet links.
- `MATERIAL_CARRIER_NODE_RETURNS.svg`: the eight `F_ij`–`220k`–`RET` branches.
- `MATERIAL_CONTACT_INDEPENDENT_SOURCE_VERIFICATION.json` and `MATERIAL_CARRIER_VECTOR_CAPTURE.json`: executable verification results with source SHA-256.

## Assembly and measurement sequence

1. Keep all rails disconnected. Mark the eight distinct pads `PAD_11` through `PAD_24` and eight internal `F_ij` sheet nodes as on the source. Use independent DMM continuity checks before connecting voltage. No conductive 1k perimeter guard may be added: that would change the circuit.
2. Install the six horizontal and four vertical 22k links and the eight 220k returns. Verify end-to-end resistance and adjacency at each source node; record actual resistor values and the instrument settings. The mesh has more than one parallel path, so derive expected node-to-node readings from the connected network rather than expecting one isolated 22k reading across a populated mesh.
3. Install eight separate fixed 1k series devices from each pad to its corresponding `F_ij`. The eight `R_ACT` contact elements are **different** replaceable devices from `VREF` to the pad. Record each actual released and actuated resistance if a force-sensitive element is used.
4. Start with bounded isolated 1.8V power. Follow `02_BENCH_PROTOCOLS/POWER_PRECHECK_AND_IRL_PROCEDURE.md` for independent-host-unplugged measurement, probe loading and three-charge-node tests. Do not count digital RC trajectories or legacy header-only evidence as acquired voltage readings.
5. Bring up the 3.3V display and independently current-limited 24V breakdown stage only after the corresponding K06 source and safety checks have passed. For closed-loop automated WRITE/BOUNDARY operation, first validate actual instrument calibration and device-specific protections.

## Repeatable code checks

From the extracted root `VOID/`:

```bash
python3 06_ENGINEERING_VALIDATORS/expand_r08_k06_hardware.py
python3 06_ENGINEERING_VALIDATORS/verify_material_contact_carrier.py
python3 06_ENGINEERING_VALIDATORS/render_material_carrier_circuit_sheets.py
python3 00_CONTROL/run_physical_preflight.py
```

Source changes must be followed by regeneration and new source-hash capture. No KiCad ERC/DRC, PCB or actual physical test result is inferred from the vector drawings or structural preflight alone.
