# Physical HIL control, real timestamps and fail-closed hardware phases

The native controller's existing 4 ms epochs are **digital model iteration intervals**, not promises of analog relaxation time. Real physical sampling and actuation must use timestamps obtained from the chosen instrument, alongside monotonic acquisition counter, command receipt, calibrated readback, rail current/voltage, device serial and run ID. Physical evidence is accepted only under an explicit physical source identity; digital model CSV is never an instrument session.

## Required end-to-end transaction

1. `POWER_OFF`: driver does not permit stimulus; inspect actual independent supplies and check reference isolation, current limits and disconnected-host physical power operation.
2. `CALIBRATED`: collect instrument identity, current calibration ID, probe input load, zero and gain verification, supply rails, series component values and a source file/hash manifest; refuse absent fields.
3. `ARMED`: measure ADC input polarity and bounded signal levels with the output *disabled*; verify output-disable electrically and with a real readback. Test unplugged or timed-out device behaviour. No arbitrary MMIO or guessed device address.
4. `MEASURE`: record `t_acquired_ns`, `sample_index`, `PROBE_A/B`, `CHARGE_A/B/C` and (where instrument permits) the actual electrode/rail feedback. Samples with missing fields, non-monotonic time or out-of-range voltages cause refusal.
5. `DECIDE`: supply the physically acquired state to **the same native HX89 + CPU/AVX/ACDC observation contract** used in the verified digital tests. Store source file identity and digest as input provenance, not as a substitute for analog data.
6. `ACTUATE`: only after independent current/voltage gates, send a *bounded protected* WRITE_A/B/BOUNDARY_A/B command through an actual known driver. Record `t_command_ns`, `t_applied_ns`, measured electrode voltage and measured current. The presence of a function call is not proof of actuation.
7. `SETTLE / MEASURE AGAIN`: derive waiting and sample rates from separately measured RC relaxation/slew behaviour, amplifier bandwidth and anti-alias filtering, not a predeclared CPU instruction cycle. Any lost device or stale/noisy/readback-mismatched sample triggers `FAULT → output inhibited`; the trial is rejected, its raw bytes retained.

## Adversarial experimental controls

Two physical sessions with the same nominal command are not assumed byte-identical. Repeat with one contact changed at a time, all contacts fixed, write electrode disconnected, host unplugged, alternative independent meter and two calibrated readout loads. Compare model-versus-measurement residuals only after sampling rate, analog input impedance and applied voltage have been recorded; publish the residual distributions, sample counts, conditions and failure logs. Separate software repeatability from physical stochasticity in the provenance receipt.

## Native file entry point already present

`09_PHYSICAL_PROTOTYPE_AND_GATEWAY/native_bench_ingestion/void_bench_ingest.c` is a real compiled C/OpenSSL input-validation boundary for **externally acquired** CSV data. The physical preflight tests missing source files, nonfinite quantities, duplicate timestamps, overvoltage, changed calibration, sample-index gaps and incomplete headers. A full HIL actuator driver must not be asserted unless connected to a specific actual piece of instrumentation and independently read back. The current design release provides complete net/pin contracts, bench procedure and controller reference against which that real driver is to be validated.
