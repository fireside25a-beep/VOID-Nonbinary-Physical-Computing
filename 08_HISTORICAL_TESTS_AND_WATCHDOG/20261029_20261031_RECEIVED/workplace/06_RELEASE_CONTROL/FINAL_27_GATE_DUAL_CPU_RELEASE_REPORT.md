# VOID/HX89 — Final native dual-input research execution status

**Entire native application re-executed**, including original HX89 5D, Q², native accelerator, reversible digital lattice, AVX/CPU batch, cache/history, K01–K06 source contract, and new two-core A/B/A+B physical-response test.

Full two-run canonical acceptance receipt: `04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/canonical_1793300628425394394/REPEATED_MACHINE_RESULT.json`.

| Final whole-machine run | Native executed gates | Result | Run receipt |
|---|---:|---|---|
| 1 | 27/27 | NATIVE_FULL_STACK_DUAL_INPUT_PASS_PHYSICAL_GATE_UNVERIFIED | `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793300634445589892.json` |
| 2 | 27/27 | NATIVE_FULL_STACK_DUAL_INPUT_PASS_PHYSICAL_GATE_UNVERIFIED | `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793300734907978502.json` |

The execution is real x86 software/hardware activity, not a pre-recorded demonstration. Both runs acquired new raw traces and checked their SHA-256 identities. The original five uploaded source archives were identical before and after these runs.

Independent source-preservation comparison: **1,288 protected source files exactly matched** the previous sealed canonical tree across originals, R08 netlists, original HX89 and preserved provenance.

## New repeated physical-interaction candidate

Real simultaneous two-CPU factorial workloads (four conditions per randomized block) and third-CPU readback. The acquired response is measured `RDTSCP`/monotonic elapsed time, not direct transistor charge or thermal sensor output.

| Separate acquired experiment | Readout hold | Recorded trials | Median four-way interaction (ns) | Sign-test p |
|---|---:|---:|---:|---:|
| 2 | 2 ms | 64 | -30,751.0 | 0.4545 |
| 2 | 20 ms | 64 | -27,632.0 | 0.8036 |
| 3 | 2 ms | 64 | +70,081.0 | 0.2101 |
| 3 | 20 ms | 64 | -28,458.0 | 1.0000 |

The response is not yet reproducible as a physically native nonbinary operator. An electrical/thermal state and memory would require independent calibrated physical readout, consistent held-out nonlinear gain, and a stimulus-disconnect control. We did **not** fill the original physical proof forms with reconstructed analog measurements.

## New source, verification and documentation

- `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/cpu_dual_physical_response.c`: actual simultaneous two-core CPU excitation and third-core timed readback.
- `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/dual_reservoir_hx89.py`: full HX89 execution, native inputs, randomized factorial protocol, real HX89 Q² output and next executed CPU workload.
- `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/test_dual_reservoir_hx89.py`: eight independently checked positive/negative assertions from acquired raw observations.
- `00_CONTROL/run_whole_machine.py`: now includes `--dual-physical` and 3 added full-application validation gates.
- `00_CONTROL/run_canonical_release.py`: now executes repeated whole native sessions with the same dual-input physical probe enabled.
- `08_DOCUMENTATION/10_DUAL_INPUT_PHYSICAL_CAUSAL_INTERVENTION.md`: source-backed method, independent results, scientific interpretation and reproduction.
- `09_RESULTS_VISUALS/real_dual_cpu_physical_factorial_hold_2ms.png` and `_20ms.png`: actual acquired timing data charts.

## Reproduce from one restored tree

```sh
python3 -S 00_CONTROL/repair_restored_native_build.py
python3 -S 00_CONTROL/run_canonical_release.py --repeat 2 --cycles 4 --material-blocks 2 --dual-physical --dual-blocks 16
```

Current scope: this is a complete, repeatable **native CPU and HX89 engineering research implementation**. It does not yet establish the separate physical nonbinary silicon memory/device criterion. The earlier rejected raw acquisitions and all historical archives are retained.
