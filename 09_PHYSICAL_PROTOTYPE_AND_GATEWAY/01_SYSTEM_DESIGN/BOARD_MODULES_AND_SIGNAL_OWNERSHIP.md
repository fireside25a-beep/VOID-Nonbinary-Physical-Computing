# Cheap experimental VOID: board and signal ownership

This is a **construction and verification architecture**, not a Gerber/PCB fabrication release. Start with a removable component-carrier or perfboard, ordinary passive parts and an isolated/current-limited bench supply, then migrate to routed boards after the measurements and loading calculations agree. A 4-layer controlled-impedance board is not necessary to begin a low-frequency experiment.

## Core + four surrounding schematic functions

**CORE K06 (active R08 source):** Populate the exact source-derived R, C, L, D and Q network from the expanded inventory. Use three independently observable charge nodes `CHARGE_A/B/C`, `PROBE_A/B`, `FIELD_A/B`, `AXIS_A/B`, write pads `WRITE_A/B`, and bounded inputs `BOUNDARY_A/B`. K05 five-input two-output weighted resistor network and K_MESH_V1 are subcircuits, not detached research branches. The original simulated supplies `V_ISO`, `V_UI_RAIL`, `V_DISPLAY_RAIL` are *external power connections*, not resistors to purchase.

**P1 isolated power and return:** independent current-limited 24 V only for biased junction K01, monitored 1.8 V UI/material rail (with `R_UI_CURRENT=100Ω`) and independent 3.3 V display rail. No unverified fixed-24V LDO part number; select a verified supply. Add physical power disconnect, rail current monitoring and appropriate test headers. Connect analog return at a controlled common reference; assess ground loops before PC USB connection. Maximum worst-case power in the 3.3kΩ resistor at 24V is ~0.175 W, select rating ≥0.5 W with margin and check thermal conditions. The K06 diode model uses nominal BV=7.5V, which is not a manufacturer-tolerance proof.

**P2 high-impedance acquisition:** use a calibrated 10MΩ DMM or high-Z probe for the initial experiment, **instead of installing the netlist's parallel 10MΩ instrument equivalents as separate resistors**. The mesh deck models 1MΩ+30p probes for `PROBE_A/B`: either match that meter configuration or replace the equivalent circuit model with the actual probe's measured impedance; never double-shunt. Later provide a guarded FET/electrometer buffer and real ± supplies as needed, plus antialias/filtering and ADC level translation. Keep capacitor and diode leakage low and clean the board.

**P3 host acquisition/control:** first record measured timestamped voltages using an actual calibrated instrument (manual export or direct SCPI if the user's instrument is known). The native C validator checks shape, monotonic time, bounds, and append-only SHA-256 receipt. To close automated hardware feedback, choose a specific ADC/DAC/interface with calibrated voltage span and real firmware+driver, then wire its input to the high-Z buffers and its output through verified attenuation/current-limiting to `WRITE_A/B` and `BOUNDARY_A/B`. **Do not attach MCU pins or unprotected DACs directly to K06 high-Z nodes.** This source release does not invent an unknown hardware driver or claim device performance.

**P4 contact carrier:** an accessible 2×4 matrix corresponding exactly to `PAD_11, PAD_12, PAD_13, PAD_14, PAD_21, PAD_22, PAD_23, PAD_24` in `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib`. Use measured release-state resistors (nominal 10MΩ each) and calibrated, swappable contact/FSR elements if force response is desired. The 1kΩ in-source `R_ACT_GUARD_*` are **series electrical resistors**, not an arbitrary 1kΩ grounded perimeter guard. The 22kΩ sheet links and 220kΩ return paths in source must match actual wiring. Document mechanical footprint and pin orientation as built.

## Port interface and assembly stages

- Stage A: isolated low-voltage passive mesh, K05 DC witness, and three charge-node RC networks. Keep 24 V junction and output loads disconnected; compare measured passive results against independently derived circuit calculations.
- Stage B: attach nonlinear 1N4148 pair, bounded write electrodes and material/contact carrier, test charge transfer and relaxation with manual voltage inputs. Keep excitation in safe measured bounds.
- Stage C: independently power the K01 junction at current-limited 24 V and LED rail at 3.3 V, verify currents and load changes with analog instrumentation. Never drive piezo or LED from a probe output unless the source-defined stage is correctly assembled.
- Stage D: add buffered measurement, real ADC/DAC and protected host connection. Only then run physical-controller feedback with a watch-dogged actual device.

## Separation of measured, modeled and assumed quantities

The native `void_unified` CSV is source-driven numerical model output; `void_bench_ingest` accepts an *external physical acquisition file* and emits an evidence identity receipt. Neither automatically attests the provenance of an actual instrument. Record actual supply voltages, resistor values, capacitance, ambient temperature, probe impedance, contact geometry, calibration IDs and load changes. Sign-off requires independent readings, causal perturbations and repeat sessions.
