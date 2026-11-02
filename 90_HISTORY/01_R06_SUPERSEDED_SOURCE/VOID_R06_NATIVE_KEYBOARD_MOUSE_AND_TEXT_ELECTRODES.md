# VOID R06 — native physical keyboard / pointing transducer, single core

## Actual implemented schematic

The *only* active material core remains `02_PHYSICAL_CIRCUITS/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir`.
It includes **one instance** `X_HUMAN_IO` of `VOID_HUMAN_TRANSDUCER_V1.lib`.
Its four output/coupling ports join the **same** `PROBE_A`, `PROBE_B`, `CHARGE_A`, and `CHARGE_B` already shared with K01's junction, K05's weighted network, the RLC branch, and the two volatile charge capacitors. K01–K04 and original mesh source remain unmodified. No CPU state update, pseudorandom generator, digital character parser, new parallel neural core, or algorithmic numerical step is present in this new netlist.

## Physically interpretable inputs

**Six pressure-sensitive mechanical keycaps**, labeled `A`, `E`, `I`, `O`, `SPACE`, `ENTER`, each place an actual *variable two-terminal force-sensitive resistance* between independent `UI_POS` and its own sense junction. Each junction drives two distinct resistive paths into `KEY_ELECTRODE_A/B`. Those two electrode voltages, not an ASCII code, drive the existing mesh and charge state **simultaneously** through resistors. Holding or pressing more than one key affects both electrodes by Kirchhoff-coupled physical currents; a single analog amplitude does not uniquely decode all possible chords.

**Two mechanically adjustable 100 kΩ potentiometers** act as X and Y pointing axes. Their physical wipers are between `UI_POS` and `UI_NEG`. The SPICE representation shows two 50 kΩ halves **at the nominal centered position only**. The *built part is a three-terminal mechanical potentiometer*, not four fixed 50 kΩ resistors, and when moved its wiper impedance changes physically. The wiper electrodes couple into `PROBE_A/B` and `CHARGE_A/B` using real resistors.

**Power boundary:** independent analog +0.9 V and -0.9 V source rails, common *local analog* return, each behind a 100 Ω current-monitor/safety series resistor. Never directly connect this return to a computer chassis or USB ground without the chosen isolation design and electrical review. The 24 V reverse-breakdown supply remains a separate existing current-limited rail; verify independence and grounding before assembly.

## Actual input and output mapping

| Device | Physical connection | Observable | Inside K06 coupling |
| --- | --- | --- | --- |
| Six pressure-sensitive keycaps | `R_PRESS_{A,E,I,O,SPACE,ENTER}` between `UI_POS` and sense junctions | `KEY_ELECTRODE_A`, `KEY_ELECTRODE_B` | Both original mesh ports and both charge caps |
| Mechanical X pot | `R_POINTER_X_UP/DOWN` as two portions of one three-terminal wiper track | `WIPER_X` | `PROBE_A` plus `CHARGE_A` |
| Mechanical Y pot | `R_POINTER_Y_UP/DOWN` as two portions of one three-terminal wiper track | `WIPER_Y` | `PROBE_B` plus `CHARGE_B` |
| Prior K05 voltage banks | Five independent bipolar analog source rails and reused K05 weighted subcircuit | `y0`, `y1` | Capacitive CR paths into original mesh |
| Prior K01 diode | Current-limited 24 V reverse-breakdown junction source | `JCT` | AC-blocked path into original mesh |
| Existing output | high-impedance instrument ports | `PROBE_A/B`, `CHARGE_A/B`, `y0/y1` | Actual analog outputs; no text-rendering display claimed |

## Meaning of text and mouse

A keycap marked `A` can cause a characteristic analog two-electrode pressure waveform. This is **physical acquisition of a tactile text-key action**, not general natural-language understanding, text rendering, or a six-bit character representation. Sequential key actions enter the existing capacitor dynamics in physical time. Whether they can be discriminated or remembered by the material requires as-built evidence.

These pointer axes are an **analog mechanical pointer/trackball interface**. A conventional USB optical mouse, standard HID keyboard, and normal text files use digital protocols outside this board. They may later drive the *same physical electrode pins* through a separately identified transduction interface; doing so would not transform the digital input protocol into an analog computation, and none has been invented here.

The existing output terminals are analog. Creating a conventional typed-text visual display requires a physical decoding/display interface; it is not claimed as built by this hardware revision.

## Assembly, physical evaluation and safeguards

1. Install real FSR sensors under mechanical keycaps, not static 10 MΩ resistors. The 10 MΩ SPICE cards describe one unloaded physical reference. Measure actual open pressure and pressed resistance individually over force/temperature; replace *reference* values with as-built data later, not hand-picked target outputs.
2. Use two actual 100 kΩ three-terminal analog pots on a mechanical two-axis pointing control. Map endpoints/wiper correctly; verify resistance and absence of wiring errors unpowered.
3. Attach each sensor to its specific node using the unique part names in the electrical component matrix. Keep the KEY electrode guard returns; avoid unintentionally tying `UI_POS` to the 24 V diode bias.
4. Before power, measure every low-ohmic connection, each intended isolated rail, and polarity. The 100 Ω rail monitor resistance is nominal; log meter/instrument input load and actual component tolerance.
5. Verify the pressure keys produce an analog electrode response and that both `PROBE_A/B` and `CHARGE_A/B` change when appropriate. Check X and Y motion independently and simultaneously. Power/thermal/timing measurements require physical instrumentation, not netlist output.
6. Record multi-key chords, adjacent-key crosstalk, release recovery, drift/hysteresis, false activation, open-wire faults, and repeated physical stimulus. These are test categories, not completed bench results.
7. High-impedance probes must match the impedance modeled in the inherited mesh; do not install a second equivalent shunt when the actual instrument already supplies that load. Do not drive an unprotected computer input or audio speaker directly from these analog electrodes.

## Component-class verification references

Interlink Electronics FSR 400 Series official datasheet: https://www.interlinkelectronics.com/downloads/datasheets/fsr-400-series-datasheet.pdf . A two-terminal sensor varies resistance with applied force; the curve depends on mechanical integration. This is not a calibrated textual-symbol receiver by itself.

Bourns 3590 precision potentiometer official product/datasheet: https://www.bourns.com/products/potentiometers/product-detail/precision-pots-multiturn/3590 and https://www.bourns.com/docs/Product-Datasheets/3590.pdf . A real 100 kΩ linear three-terminal wiper is available. A 10-turn bench control is a possible manual input demonstrator, not a high-speed computer mouse; a faster purpose-built analog mechanism would require separate mechanical selection and evaluation.

The *electrical hardware descriptions* are created and structurally verifiable. No fabricated, powered, or measured device has been claimed. K01 source mechanisms, stable RBits, SNN-like spiking, complete keyboard support, and actual text output are distinct unresolved physical hypotheses/tasks, not renamed component parts.
