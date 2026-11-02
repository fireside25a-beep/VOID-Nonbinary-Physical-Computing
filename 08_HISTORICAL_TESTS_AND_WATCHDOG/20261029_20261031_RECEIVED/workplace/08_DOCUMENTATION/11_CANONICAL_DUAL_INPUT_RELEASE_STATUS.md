# VOID/HX89 — Native two-input physical-response integration and release status

## Scope and preservation

This project is one cumulative source tree with its unchanged original user archives. The execution path is the actual native CPU code, original HX89 5D/Q²/native accelerator, reversible **digital** gas Polyform, cache/history interventions, and feedback into a later real CPU workload. The new simultaneous A, B, A+B intervention runs *inside* that whole-machine acceptance, not in a substitute project.

## Independent whole-machine receipts

| Actual receipt | Passing gates | Failed gates | Physical analog computation proven |
|---|---:|---:|---|
| `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793300480089536534.json` | 27/27 | 0 | no |
| `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793300634445589892.json` | 27/27 | 0 | no |
| `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793300734907978502.json` | 27/27 | 0 | no |

## Two fully acquired four-condition CPU experiments

Each experiment ran an actual four-condition factorial intervention on two concurrently pinned virtual CPUs and timed an identical readback after predefined hold intervals. Every run checks real worker overlap and source provenance.

| Run | Hold (ms) | Native samples | Median factorial interaction (ns) | Positive / negative signs | Two-sided sign p |
|---|---:|---:|---:|---:|---:|
| 1 | 2 | 64 | -30,751.0 | 6 / 10 | 0.45450 |
| 1 | 20 | 64 | -27,632.0 | 7 / 9 | 0.80362 |
| 2 | 2 | 64 | +70,081.0 | 11 / 5 | 0.21011 |
| 2 | 20 | 64 | -28,458.0 | 8 / 8 | 1.00000 |

**Interpretation:** At a 2 ms hold the sign changed between independent acquisitions. At a 20 ms hold neither run demonstrated a statistically persuasive paired interaction effect. This does not establish a useful nonlinear physical operator, retained multilevel analog memory, or direct control of MOS gate bias. The measured values are genuine clock/time measurements on a virtualized host; host scheduler, CPU mapping and cache/power-frequency behavior remain confounders. This release therefore retains physical Gate K as **not verified**.

## Actual code and evidence

- Native two-worker three-core experiment: `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/cpu_dual_physical_response.c`.
- Authentic full-stack connection: `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/dual_reservoir_hx89.py`.
- Strict mutation refusal tests: `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/test_dual_reservoir_hx89.py`.
- Integrated verification: `00_CONTROL/run_whole_machine.py` and `00_CONTROL/run_canonical_release.py`.
- Native samples: `04_TESTS_AND_LOGS/20261029_DUAL_CPU_REPEATED/`.
- Full pass/fail receipts and earlier rejection logs: `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/`.
- Figures are generated from saved measurements by `09_RESULTS_VISUALS/plot_native_dual_acceptance.py`.

## Real scientific acceptance

Source and execution gates demonstrate a verified digital/native feedback system. Claiming a *different physical computing medium* requires an independent, calibrated material-state readout and a measured nonlinear/memory transformation with held-out reproducibility and controls separating physical state from the digital execution and observer. The original K06 netlist is preserved, not a fabricated or attached electrical device.

## Reproduce

```sh
python3 -S 00_CONTROL/repair_restored_native_build.py
python3 -S 00_CONTROL/run_canonical_release.py --repeat 2 --cycles 4 --material-blocks 2 --dual-physical --dual-blocks 16
```

These commands run actual source and preserve fresh failure receipts. Hardware telemetry capabilities and run durations differ among hosts.
