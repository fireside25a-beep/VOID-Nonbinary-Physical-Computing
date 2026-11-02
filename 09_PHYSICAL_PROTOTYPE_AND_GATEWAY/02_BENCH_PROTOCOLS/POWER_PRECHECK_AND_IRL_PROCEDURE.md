# VOID K06 physical bench procedure (lab checklist)

## 0. No software claim is a substitute for the bench

Use current-limited isolated power. Confirm earth/return strategy with a competent operator. Never attach a direct ground-referenced scope clip to an unknown floating high-voltage node, or an ADC GPIO to unverified positive/negative analog voltages. This design includes a nominal 24V biased junction; the cheap initial passive experiment can be done entirely at ≤1.8V and does not need a PC connected.

## 1. Assemble de-energized and test continuity

Compare every resistor/capacitor/diode/transistor orientation and net to the KiCad capture and SPICE source. Verify no supply shorts. Check BZX55C7V5 polarity in the active `D_REAL 0 JCT` SPICE orientation; check actual device datasheet lead markings. Measure actual component values (especially 1MΩ, 10MΩ, 100nF, 220nF, 10nF). Avoid flux contamination on ≥10MΩ paths. Record open-circuit probe loading and actual instrument serial.

## 2. Independent power and material dynamics

Energize 1.8V separately; measure both sides of 100Ω `R_UI_CURRENT` for input current. Energize 3.3V display supply separately only after BJT/LED wiring checks. With the host unplugged from the circuit, demonstrate actual analog relaxation with a scope and the correct probe load on `PROBE_A/B`, `CHARGE_A/B/C`. Capture paired time/voltage data and independent supply current records. Compare no-excitation, write A, write B, inverted and disconnected electrode cases.

## 3. K01 24V junction only after low-voltage checks

Use isolated, voltage- and current-limited external 24V supply through source's 3.3kΩ and 100Ω resistors, not a mystery converter. Check resistive 3.3kΩ drop at bias and that the zener power and resistor temperatures remain within their ratings. Junction source model is only nominal (BV 7.5V, IBV 5mA); characterize actual I-V and external noise rather than inferring it from a model.

## 4. Instrument loading comparisons

Document DMM/scope mode and its input resistance/capacitance. For a 10MΩ design meter already represented by `R_MEM_METER_A`, adding another 10MΩ meter in parallel produces 5MΩ effective loading. For the `1MΩ||30p` mesh probes, an extra 1MΩ probe produces 0.5MΩ before capacitive effects; correct the simulation before comparing. Measure at least two different known loading configurations to expose sensitivity.

## 5. External acquisition and native validation

Do not invent data to fill historical header-only TSVs. Export authentic measured time series to the exact `sample_index,time_ns,instrument_serial,calibration_id,charge_a_v,charge_b_v,charge_c_v,probe_a_v,probe_b_v,write_a_v,write_b_v` CSV header, in volts and nanoseconds with monotonic timestamps and original instrument metadata. Validate via `make -C 09_PHYSICAL_PROTOTYPE_AND_GATEWAY/native_bench_ingestion && .../void_bench_ingest real_input.csv new_append_only_receipt.txt`. The validator rejects incomplete, nonfinite, out-of-bounds, duplicate-time and missing instrument records; its receipt stores SHA256 and ranges. An actual instrument operator's session details and calibration sheet must accompany the file. No claim of physically closed feedback until the actual actuator's drive, readback and real input identity are independently evidenced.

## 6. Physical criteria (measured, not fabricated)

Verify polarity and monotonicity for deliberately applied small, safe inputs, repeat charge relaxation across independent runs, compare oscilloscope channels against a second meter at agreed load, and make sure `WRITE_A` and `WRITE_B` have distinct, causal effects on measured charge nodes. Record actual times, source noise, ground connections, and control toggles. Do not claim numerical solver equality at unmeasured high frequencies or general-purpose CPU instruction replacement.
