# Build from the actual source-defined ports

## Editable capture

Nine source-linked KiCad 9 `.kicad_sch` captures are in `01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS`. They contain 216 original SPICE element declarations and 459 SPICE pin connections. The generated `COMPONENT_PORT_MAP.csv` resolves every pin to a source-net label, and `CAPTURE_VALIDATION.json` carries each original source SHA-256. These captures are not inferred from the screenshot images. The renderer source is `06_ENGINEERING_VALIDATORS/generate_editable_spice_schematics.py`; rerun after source changes, never manually retouch to diverge from the source.

## K06 expanded assembly information

The actual assembled K06 hierarchy expands the three source `X_` subcircuit instances into 175 primitive element cards: 130 resistors, 17 capacitors, 15 diodes, four BJTs, one inductor and eight simulated voltage sources. Do NOT buy eight voltage-source components: the V cards represent externally supplied excitation/bias. Some 10MΩ and `1MΩ+30p` elements are simulated meter/probe loads, not second physical parts to solder. `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/K06_HIERARCHICAL_EXPANDED_BOM.csv` differentiates these roles, and `K06_NODE_AND_TEST_POINT_PORTS.csv` lists exact flattened source electrical nets. This is a netlist-accurate assembly *inventory*, not a priced distributor quote, pin-verified component-footprint library, manufactured PCB, or instrument-characterized device list.

## Critical exact terminal names

`V_ISO(SUPPLY,0)=24V` source-deck nominal (optional biased-junction experiment), `JCT`, `PROBE_A`, `PROBE_B`, `CHARGE_A`, `CHARGE_B`, `CHARGE_C`, `WRITE_A`, `WRITE_B`, `BOUNDARY_A`, `BOUNDARY_B`, `UI_1V8`, `DISPLAY_3V3`, `FIELD_A`, `FIELD_B`, `AXIS_A`, `AXIS_B`, `DISPLAY_X/Y/Z`, and material `PAD_11...PAD_24`. Pay attention to SPICE diode anode/cathode and Q pin order C/B/E when purchasing and assigning footprints. Physical `0` is analog return, not automatically a safe USB ground. Do not trust arbitrary MMIO registers or hidden host-only sensor sources.

## Electrical hierarchy and production gate

K06's `.cir` references `VOID_K_MESH_V1.lib`, `VOID_K05_WEIGHTED_NETWORK.lib`, and `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib`. Schematic sheets preserve this hierarchy as source-linked component captures; a production PCB requires verified symbols, matching manufacturer footprints, silk orientation, ERC/DRC, stackup, leakage-appropriate clearances, impedance and probe-loading checks, mechanical/pad layout and manufacturer DFM before a fabrication claim. The current project deliberately does not create fake Gerbers, drill files, fabricated measurements or purported CE/FCC certification.

## Verified source-backed build interfaces (2026-11-02)

`K06_PROTOTYPE_CONNECTOR_PINOUT.csv` contains 15 deliberately proposed connector references and 78 numbered pins, each checked against a net in the 175-primitive/74-net source expansion. `K06_GROUPED_ASSEMBLY_AND_LOAD_POLICY.csv` groups the electrical components by actual assembly role rather than counting eight SPICE V-source definitions as parts to buy. `K06_BUILD_CONTRACT_VALIDATION.json` is the reproducible count/relationship check. `06_ENGINEERING_VALIDATORS/make_k06_build_contract.py` regenerates these files. Read `REAL_K06_LOW_COST_ASSEMBLY_GUIDE.md` before wiring. The original material library defines **eight replaceable 10 MΩ contact elements plus eight distinct fixed 1 kΩ series guard resistors**, not sixteen replaceable sensors. Physical axis potentiometers and piezo model equivalents are explicitly distinguished.
