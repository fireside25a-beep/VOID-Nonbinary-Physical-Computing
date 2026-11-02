# VOID K — Physical topology and deployment

Electrical node connectivity is literal in the .cir files. `.INCLUDE` supplies a shared resistor/capacitor physical network; it does not provide simulation-generated or digital inputs. K01–K04 use the identical physical mesh, capacitor and amplifier input load representation. Their source impedances deliberately differ and cannot be treated as identical for uncalibrated noise-power comparison.

Physical diagram, same route for every source:

External SOURCE JCT → 10 nF series DC block → AC_IN → 1 kΩ series → INPUT
INPUT → (10 kΩ || 1 nF) → PROBE_A → (22 kΩ || 2.2 nF) → PROBE_B
PROBE_A → (33 kΩ || 4.7 nF || 1 MΩ instrument || 30 pF instrument) → analogue ground
PROBE_B → (47 kΩ || 3.3 nF || 1 MΩ instrument || 30 pF instrument) → analogue ground
INPUT → 1 MΩ → analogue ground.

K01 source: isolated 24 V bench supply → 3.3 kΩ physical limit resistor → 100 Ω Kelvin current-sense resistor → real diode cathode. Diode anode → analogue ground. Power and diode I-V are physically monitored. The series coupling capacitor prevents DC bias at mesh input only if it is intact; check leakage and breakdown rating. K02 has identical wiring with the connected supply set to 0 V. K03 replaces the source with 100 kΩ unpowered thermal resistor to ground. K04 with 50 Ω unpowered termination to ground. A dedicated manual physical connector can select the source; it must not connect multiple sources together.

Place diode and shunt with short loop and separate analogue readout from the bench supply return. Guard and shield the high-impedance node. Use low-leakage rated coupling capacitor, rated bias resistor, physical return plane, guarded probe pads, and mechanically keyed test connectors. Do not infer line impedance, RF isolation or thermal source quality from the netlist. The instrument's 1 MΩ+30 pF is an explicit nominal example: substitute measured properties for a final production layout.

No electrical trace is allowed to a speaker or an unprotected computer audio input. Add separately characterized external isolation/limiting/amplification for future audio experiments and account for its energy; do not silently claim it exists here. Output dynamic failure cannot be assumed to self-collapse to zero; verify stability under real loads before feedback closure.

## R04 as-built K05 circuit correction

The K05 circuit's old Vxm3 had no conducting connection to y0/y1 and is removed. Four fractional-Ohm resistor literals are replaced with paired physical parallel branches; exact connectivity and nominal equivalent conductance are in `VOID_K05_R04_PHYSICAL_ASSEMBLY_AND_CONTINUITY.md`. The matrix is regenerated from every actual circuit element, including both instrument-equivalent 10-MΩ inputs. The 10-MΩ inputs are properties of actual connected meters, not additional shunts to solder onto an already-loaded circuit. Existing K01–K04 are byte-identical to R03.
