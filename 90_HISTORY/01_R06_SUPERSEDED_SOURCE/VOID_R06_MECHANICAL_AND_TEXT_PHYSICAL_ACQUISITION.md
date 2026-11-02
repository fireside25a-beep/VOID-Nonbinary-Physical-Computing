# R06 physical proof requirements — same VOID core

Production PCB or breadboard test fixture is required; all records are initially empty. The provenance-controlled original headers in the four earlier Gate K ledgers remain untouched. The new multimodal extension does not turn static SPICE into physical readings.

- **Keycap electrical operation:** independently measure source rail, force-sensor resistance, and `KEY_ELECTRODE_A/B` voltages for each of six keys, including no-force, graded force, release, drift and simultaneous two-key operation.
- **Causal mesh coupling:** record on the same timebase `KEY_ELECTRODE_A/B`, `PROBE_A/B`, `CHARGE_A/B`; compare physically open and physically connected key sensor (including energy/current drawn from the separate `UI_POS` rail). A keycap voltage by itself is input transduction; material computing requires a measured *useful* input/output transformation.
- **Mouse/pointing:** record independently moved X/Y physical potentiometer wipers and response of all four core nodes; compare centered, extremes, combined movement, repeatability and history after release.
- **Charge dynamics:** follow actual `CHARGE_A/B` relaxation after key release and after independent manual charge preparation. Verify observable multilevel separation, retention and crosstalk before referring to a physical RBit, neuron, or memory mechanism.
- **Control experiment:** power the analog board from independent rails; compare with input sensors removed and with remote digital host lines physically absent. Document powered source current, analog device power, readout energy, and calibration.
- **Instrument noise:** calibrate real receiver noise and input loading before classifying stochastic physical source. Never generate fake capture data to fill the ledgers.
- **Fielded build identity:** capture dated assembly photos, board layout revision, diode lot, sensor/pot device part numbers, actual resistance, calibrated scope inventory, raw traces and SHA-256. Record negative outcomes rather than recoding expectations.

This is a connection-and-acquisition implementation milestone, not a completed physical experiment.
