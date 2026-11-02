# VOID R06 single-core MATERIAL INPUT / OUTPUT physical primitive specification

## Authoritative source, retained sources and no detached core

`02_PHYSICAL_CIRCUITS/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir` is THE ONE active integrated circuit. Its material interface is exactly one `.INCLUDE "VOID_PRIMITIVE_MATERIAL_INTERFACE.lib"` and one `X_MATERIAL` instance. The earlier, conflicting 6-key and 44-key alphabet-oriented netlist modules are preserved byte-for-byte under `01_PRESERVED_INPUTS/R06_SUPERSEDED_UNSEALED_HUMAN_IO/`; neither is in the active netlist's include graph. This is one corrected R06, not a new standalone competing machine.

## Computing substrate

Original K01 reverse-breakdown design -> AC coupling -> original 2-node RC mesh. Original K05 five-electrode conductance network -> two DC outputs -> AC coupling into that same RC mesh. An independent, actual inductor/series capacitor and resistor joins the two mesh nodes. Existing coupled CHARGE_A/B capacitors, leakage and bidirectional feedback remain connected. A pair of opposite-orientation switching diodes via one 47k series current limiter forms an additional real, physically nonlinear path between those charge-state nodes. It is a nonlinear conductance primitive, not an invented 3-state RBit, software qubit or verified physical learning cell.

## Physical input class primitives (no alphabet encoding)

**ACT_01–ACT_08:** eight independently mounted two-terminal VARIABLE-IMPEDANCE physical actuation elements, each with its own contact terminal. Example actual devices: force-sensitive resistor, conductive rubber, pressure-variable contact, strain-resistance element. Each element connects the same isolated current-sensed 1.8V rail to its own analogue junction, and each junction connects by two physical resistors to the common FIELD_A/B electrodes. Multiple simultaneous force/contact events physically superpose and interact through the shared Kirchhoff network; there is no character identifier, time-scanned keypad, binary register, ROM table or ASCII lookup in the material. **10 megohms on each R_ACT is ONLY the unactuated nominal source card**; the as-built sensor's actual force/resistance must be measured. Eight is the demonstration interface count, not a theoretical limit on mechanical control count.

**AXIS_A/B:** two physically actuated three-terminal 10k resistive wipers, mechanically positioned. 5k/5k source cards describe the centered reference, not artificial motion. These are analog lever/trackball/position input primitives, not software USB HID signals.

**BOUNDARY_A/B:** two independent physical analog-voltage input terminals for an electrical sensor or a separate isolated D/A boundary interface. The source cards show 0V test reference until an actual physical source is connected. Each terminal feeds the same mesh via its own 470k resistor. The external controller never executes the material's charge-state transitions. No special or undocumented x86 register mapping is assumed.

**POTENTIAL TEXT/KEYBOARD INPUT:** A conventional mechanical keyboard could physically actuate multiple such material elements; the pressed material changes the shared field. No glyph, character or language representation is assigned to the elements. A computer keyboard supplying digital events would require an explicit external voltage/force transduction boundary, which is not a separate VOID compute core. A user's keypress is an INPUT PHYSICAL EVENT, not automatically a character decoded by the substrate.

## Physical output class primitives (not software rendering)

**DISPLAY_X / DISPLAY_Y:** explicit analog charge-voltage output terminals with 100k series output resistance and nominal 10M instrument load, intended for an actual high-input-impedance analog X-Y visual monitor. An external powered X-Y scope/deflection instrument provides the visual surface; there is no raster/framebuffer/character-font simulation.

**D_LED_A / D_LED_B:** actual two light-emitting diode component sites driven by separately powered 3.3V analog BJT stages Q_LIGHT_A/B. Each stage receives a physical charge-state voltage via a high-resistance sensing path. Brightness and threshold are consequences of the material and actual transistor/LED characteristics, never an asserted measured image. These implement a pair of genuine analog display-output primitives, not a complete text display.

**Nonlinear physical selection:** the anti-parallel charge coupling diodes and the BJT base-emitter response provide material nonlinear response. They do not claim to decode binary tokens or specific letters. For meaningful machine-level decoding, establish a task-specific physical discrimination experiment, not a software precomputed alphabet.

## Real assembly differentiation and power

Keep the 24V breakdown supply physically current-limited and isolate accessible low-voltage operator controls. Supply rails are 24V junction, five K05 electrode sources, 1.8V material actuation and 3.3V light-output rails (plus original analog write potentials). Document supply current separately; neither the 1.8V nor 3.3V supply is a claimed x86 internal rail. Input interfaces, visual output drivers, and measurement equipment consume energy and cannot be omitted from total energy accounting. Verify intended isolated return compatibility before connecting a grounded oscilloscope. Observe current-limited power-up and appropriate overcurrent protection. Every instrument-only 1M/10M resistance in the SPICE representation must map to ONE actual instrument input, not a second soldered shunt.

## Physical verification operation in sequence

On an assembled, powered material circuit: check unpowered real contact continuity and each connected pin; record as-built sensor force/resistance, capacitor and inductor values; power only the separately protected low-voltage input/output rails first; measure single and simultaneous actuation on FIELD_A/B and AXIS_A/B; document corresponding direct physical changes at PROBE_A/B and CHARGE_A/B; characterize each nonlinear diode conduction threshold and BJT optical response including current draw; test external analog input and high-Z X-Y output. Repeat under source-off, terminated and noise-source controls. Preserve true instrument trace files and calibration in the existing raw evidence register. Do not fill any empirical measurement fields with computed SPICE values.

## Scientific and historical treatment

The historical DACB 2.0 software CPU-entropy interface, SNN and HX87 Q2 archives remain preserved. On-chip physical entropy inside supported CPUs is real; `RDRAND`/`RDSEED` outputs are conditioned digital data, not directly wired raw analog junction pins for this circuit. This release neither duplicates that program nor substitutes it for the real material network. Stable multilevel RBits, spike/reset neurodynamics, text decoding and full display rendering remain separate candidate experiments, not renamed as already measured operations.

## In-place material primitive correction and live-source proof
The current canonical K06 (this directory) has eight spatially independent variable-impedance material contacts, two mechanical axes, three directly cross-coupled charge-storage nodes, its inherited current and inductor flux paths, one nonlinear antiparallel diode barrier, two raw protected external analog connector inputs, and four current-modulated optical emitters driven by the same core. These are *material device primitives*, never text signs, Roman digits, bits, qubits or instructions. No lookup encodes an input alphabet; no buffer is passed off as language. `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib` is the only active tactile input module; the old six- and 44-letter versions are preserved exclusively under `01_PRESERVED_INPUTS/R06_SUPERSEDED_UNSEALED_HUMAN_IO/`.

The unused zero-volt `V_BOUNDARY_A/B` placeholders were removed. `BOUNDARY_A/B` are externally accessible low-voltage sensor contact pads with real protection diodes, guarded shunts and high-impedance coupling to the existing mesh. Host digital peripherals (USB keyboard, USB optical mouse, text sources) are *input adapters to be engineered*, not an imaginary native analogue property of these contacts. The optical branches are direct current-to-photon output, providing material-state visualization rather than text/video raster rendering. The two PANEL X/Y physical ports allow connection to a compatible external analogue X-Y monitor with input loading characterized.

Use a physical test fixture to change actual contact resistance and actual axis potentiometer positions; the static `.cir` source expresses only nominal component selection. The third capacitor is not an automatically stable ternary memory or an independently proven RBit. Actual noisy electronic dynamics, readout power, temporal response, and simultaneous coupling require measured raw traces.
