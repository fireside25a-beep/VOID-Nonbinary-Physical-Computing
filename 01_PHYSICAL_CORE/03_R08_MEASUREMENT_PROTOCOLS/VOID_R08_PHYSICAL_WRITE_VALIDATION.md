# VOID R08 hardware acquisition, no synthetic measurements

**Before power:** check physical continuity, diode directions, two distinct WRITE electrodes, charge-side series resistors and the 1.8 V clamp rail. With power safely isolated, confirm instrument input impedance independently. Physically verify the 10 kOhm three-terminal mechanical wiper footprint instead of mistaking the SPICE 5 kOhm + 5 kOhm nominal midpoint for a completed moving contact.

**Under qualified power:** use a current-limited external real electrode perturbation, observe the contemporaneous external WRITE potential and CHARGE_A/CHARGE_B voltages using real high-impedance probes, and preserve the entire unmodified trace. Repeat for second WRITE electrode and simultaneous real inputs; record rail current, supply voltage, timestamp, board serial, source origin, instrument model/calibration and temperature. Then remove excitation and measure spontaneous decay and coupling; record negative controls. Do not fill acquisition rows with nominal netlist values.

**Criteria:** A physically captured, time-aligned write stimulus and a causal charge-node change distinguish an operating charge transfer from the prior dead-switch source. Demonstrating physical charge transfer alone does **not** demonstrate general computing, nonvolatile memory, a quantum gate, RBit multilevel storage, a character decoder or processor entropy directly feeding the material. Further device properties require separately measured evidence.

**Machine use:** independent machine-side interface may physically produce signals, but no undocumented registers, arbitrary addresses or fictitious hidden CPU-silicon wiring are assumed. Reuse the recorded CPU ISA entropy observations only for their literal demonstrated scope.
