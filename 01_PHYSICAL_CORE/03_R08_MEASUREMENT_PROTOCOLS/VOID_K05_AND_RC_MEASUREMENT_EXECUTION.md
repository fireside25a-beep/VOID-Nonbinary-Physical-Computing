# VOID R03 — physical K05 acquisition and real settling-time measurement

This file continues the existing VOID K05/DC and K01–K04 RC hardware. It is NOT a request to synthesize traces, run SPICE in place of a physical device, or invent new hardware branches. TSV evidence files deliberately contain **header rows only**. There are no measured entries in this release.

## K05 — practical voltage measurement

1. Preserve original R02/R03 release ZIPs intact. For the active R04 K05 hardware, physically verify R01–R13 physical branches including R03A/B, R11A/B, R12A/B, RG1A/B, RG0, source polarities, terminal names and the as-built connection of each of the FIVE real supply references with power disconnected. Record every actual resistor value and source voltage in `VOID_K05_AS_BUILT_COMPONENTS.tsv` and the source measurement record. Never overwrite the nominal netlist with a measured value merely to force agreement.
2. Record the model, serial, calibration state, measured or certified input resistance and grounding arrangements of both independent voltmeters. **The two `R_METER_*` elements in `.cir` represent the instrument's input loads; never install additional physical 10 MΩ shunts if the meters themselves supply that load.** Conversely, substitute the true instrument impedance for a comparison made from measurements, without falsifying the immutable R02 reference.
3. With separately powered actual physical source references, no host needed to calculate node results, use safe unpowered continuity check, then an operator-supervised power-on. Read both physical voltmeter indications and uncertainty. Preserve the original instrument export and assign its SHA-256 in the acquisition and evidence registers. Do not prefill measurements.
4. Only under the *ideal nominal sources, R04 equivalent resistances and exactly 10 MΩ meter loading* does R04 preserve R02 reference outputs y0=+0.324983750812 V and y1=-0.199990000500 V. These are **analytic estimates, not hardware pass/fail universal thresholds**. An appropriate pass band must be derived from actual component, input-resistance, source and instrument uncertainties before comparing observed readings.
5. Demonstrate continued physical output while the host command/data path is physically severed and real independent source references and voltmeters stay connected. Document the physical disconnection and external equipment power. Merely stopping a software process is insufficient.

## Physical RC transient and network scaling record

1. This is a separate, *real bench acquisition* using the existing K01–K04 passive mesh; K05 has no capacitor and is NOT the time-constant experiment. Never claim that the current two-node topology establishes a mesh-size scaling law.
2. Measure a controlled physical boundary transition with an identified calibrated physical signal generator or controlled bench bias step, after independent assessment of safe voltage, component ratings, isolation, grounding, node loading and connector bandwidth. A scope stimulus pulse or power-supply transition is not an uncontrolled noise trace. A noise trace alone cannot establish a conventional 10–90% rise time.
3. Capture independently the applied actual stimulus and the observed PROBE_A / PROBE_B analog voltage on a standalone scope/DAQ. Record real instrument timing, input capacitance/resistance and noise floor, plus ambient temperature and source impedance.
4. Define settling as sustained entry inside the stated **1% of measured final step amplitude** after the last threshold excursion over a recorded, declared observation window; record the window and uncertainty externally. The 10–90% rise interval uses measured steady levels, not arbitrary synthetic estimates. If fluctuations exceed the measurement threshold, report that settling under this definition was *not resolved* rather than force a time value.
5. A claim about dependence on built-node count requires independently built, wired and photographed topology variants with complete component and readout characterization. Do not alter K01–K04 silently or construct a numerical-only scaled lattice.
6. Enter actual values only in `VOID_GATE_K_PHYSICAL_TRANSIENTS.tsv`. Register and hash the untouched original instrument trace. Missing evidence stays BLANK, not zero, NA-as-measured, or replaced by a predicted number.

## Status

K05 physical reading: **AWAITING BENCH DATA**. K01–K04 physical transient: **AWAITING BENCH DATA**. Gate K finite Koopman inference: **LOCKED UNTIL REAL TRACES**, Gate F/H: **LOCKED**. A circuit topology or reference calculation does not advance a physical-evidence status.

## R04 note
The formerly unused `Vxm3` source is removed. See R04 physical assembly register and independent exact-rational KCL reference. Neither change changes the nominal y0/y1 reference.
