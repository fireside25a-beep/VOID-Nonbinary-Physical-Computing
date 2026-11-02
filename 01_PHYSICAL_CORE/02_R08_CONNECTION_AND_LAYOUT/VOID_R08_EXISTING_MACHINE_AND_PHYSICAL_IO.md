# VOID R08 — existing-machine coupled physical inputs, one active K06 core

This is a build specification, not a new processor, operating system, byte language, numerical backend, or invented CPU register map. `VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir` remains the only integrated material core. The R07 release and the original DACB ISA experiments remain available unchanged under preserved inputs.

## Corrected physical write electrodes

The R07 `S_WRITE_A/B` devices required a 2 V control differential but were driven by grounded control sources. Thus the proposed write path was electrically inactive at the nominal condition. R08 removes those ideal switches, the four hardcoded write/control voltage sources, and the now-unused switch model. Two external WRITE electrodes are connected by independent 10 nF film capacitors and 100 kOhm current-limiting resistors to CHARGE_A and CHARGE_B. Each external electrode has a 1 MOhm bleed to reference and opposite clamp diodes to the existing 1.8 V analog rail and ground. These pads require a **physical external stimulus** for charge injection. No synthetic pulse is provided.

Capacitive coupling transfers displacement charge during physical voltage changes; DC alone cannot be relied on for persistent writes. The unforced state is determined by real leakage, feedback and the attached measurement impedance. This is not a claim of nonvolatile memory, stable multiple states, neural spike semantics or a useful text processor. The existing shared RC/RLC networks and optical/electromechanical output stages remain connected exactly once.

## Existing machine connection, without forcing CPU instruction semantics

Host audio bias, an available analogue sensor, a genuine potentiometer, a board diagnostic analogue pin or optically captured light from the existing machine are possible **physical sources of excitation** through already existing BOUNDARY_A/B or WRITE_A/B. Only a documented electrical interface with measured voltage, impedance, reference and physical protection should connect. A machine's `RDRAND`/`RDSEED` samples establish an accessible silicon entropy path, not an external physical pin carrying the full raw on-chip noise state and not a prewired K06 substrate. There is no direct reinterpretation of those digital instruction results as continuous voltage.

The two AXIS positions are actual *three-terminal 10 kOhm physical potentiometer footprints* to be assembled. Their four 5 kOhm series resistors in the static model represent **only the physical midpoint**; it is not an automatically moving mathematical wiper. The material sheet's 10 MOhm released nominal sensor resistance likewise does not generate a changing force profile in a netlist file: mechanical motion changes the selected real variable resistors.

The existing machine's display, keyboard, pointing device and visual I/O remain legitimate external human interfaces, but their standard binary protocols are not silently reclassified as a nonbinary computing substrate. The physical alternative is material interaction and parallel electrical propagation through the existing K06 topology. Native machine-level attachment is an engineering connection task, not evidence already established by the netlist.

## Board pins and safety

Keep analog power rails independent of host digital rail noise, ensure a common reference only where required by the selected measurement topology, and physically label isolation boundaries. No uncontrolled live-cable disconnect under hazardous load; the unpowered connection/continuity audit precedes powering. The per-port table `VOID_R08_NATIVE_WRITE_AND_MACHINE_PORTS.tsv` lists all newly activated WRITE connections and existing physically meaningful I/O. Instrument loads already specified in the netlist are measurement-equivalent loads and should not be soldered as duplicates if the instrument itself supplies them.
