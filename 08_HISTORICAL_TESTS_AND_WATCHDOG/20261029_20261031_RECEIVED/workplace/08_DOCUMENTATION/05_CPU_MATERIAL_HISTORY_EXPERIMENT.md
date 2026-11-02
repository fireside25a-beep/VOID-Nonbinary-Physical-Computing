# Actual CPU material-history candidate: experiment and results

The goal is not timing software for its own sake, but to test whether prior CPU electrical/thermal activity leaves a useful continuously varying physical state that influences a later computation. Such a result requires causal controls, not just a clock counter.

## Actually executed protocol

A 4-cycle original HX89 native/Polyform/AVX/cache/history loop executes first; its actual emitted command becomes the input to a cross-core experiment. A pinned heater CPU performs one of three workload intensities (idle, partial scalar work, high AVX2). The readout CPU runs the same native computation after a fixed 5 or 50 ms delay. Permutation balance is validated from genuine raw CSV rows. The measured runtime contrast is fed back into the original Q² execution and then a changed next native CPU command. Negative tests corrupt the acquired real records and require rejection.

## Historical executed 288-sample receipt

| Delay | Idle median readout | Partial median | High median | High vs idle paired signs | two-sided sign p |
|---|---:|---:|---:|---|---:|
| 5 ms | 90.496 ms | 89.445 ms | 86.707 ms | 18 positive / 30 negative | ≈ 0.111 |
| 50 ms | 86.660 ms | 87.132 ms | 86.166 ms | 20 positive / 28 negative | ≈ 0.312 |

The sign tests and lack of independent thermometric readback prevent a meaningful claim of stable three-level material memory. The time differences can result from virtual CPU placement, cache residency, frequency control and scheduler behavior. The CPU state is physically instantiated, but **the experiment has not shown a new nonbinary substrate performing a reusable computation**.

## Graphs and raw input

`09_RESULTS_VISUALS/cpu_three_intensity_hold_5ms.png`, `cpu_three_intensity_hold_50ms.png`, `cpu_history_paired_5ms.png`, `cpu_history_paired_50ms.png`. Source `09_RESULTS_VISUALS/build_graphs.py` regenerates them from original raw files in `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/04_whole_machine_288_native_cross_core/`.

## Real physical acceptance

The mandatory next evidence would include a calibrated independently observable current/charge/temperature (or demonstrably equivalent material state), controlled intervention, retention, causal nonlinear material operation and deliberate exclusion of a purely digital/postprocessed effect. No code in this release fabricates those signals.
