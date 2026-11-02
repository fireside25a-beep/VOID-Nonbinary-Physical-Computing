# VOID/HX89 control epoch and source-code traceability

## Executed, current compiled digital path

In `05_HX89_K06_BRIDGE/03_UNIFIED_NATIVE_CLOSED_LOOP/src/void_native.f90`, each 4ms **software model epoch** reads `CHARGE_A` and `CHARGE_B` from the native linearized RC model. `void_acdc_observe` (C interface from *actual* preserved C11 `analog_core.c`) calculates 2-node DC/AC values and KCL residual. `void_entropy_bvh_observe` (C++ native BVH/procedural source) supplies source-conditioned bounding-box features. Previous `cpu_cycle` digest, preserved source CPU `cpu_batch` work digest, and CPU feedback checksum supply the controller's next CPU bit. The input bit is XOR-composed with AC/DC and geometry decisions and supplied to the SHA256-validated original HX89 binary. HX89 returns its native sum and bit, which the real CPU scalar/AVX2 cycle and CPU batch kernels consume. The chosen drive enters the source-derived K06 RC step, and the experiment repeats.

`integrated-control`, `integrated-no-cpu`, `integrated-no-acdc`, `integrated-no-entropy` are executed causal *ablations*. Each disables one dependency and demonstrably changes HX89 input/decisions. CPU RDSEED/RDRAND success and RDTSCP timing are separately logged as nondeterministic telemetry and excluded from deterministic checksum comparisons. The CPU model schedules the next iteration; there is no observed control over the processor's internal physical clock generator.

## Hardware path uses the same coordinate system

Actual high-Z `CHARGE_A/B/C`, `PROBE_A/B` are sampled by a calibrated instrument and mapped into native control inputs with the same units, epoch sequence and invalid-measurement refusal policy. The control output maps to *protected real* `WRITE_A/B`, `BOUNDARY_A/B` electrodes. An acquisition-only software parser is provided for this stage; physical stimulus selection and driver certification require a named attached instrument. Do not relabel the physical target as done when only the mathematical RC solver was executed.

## Causal tests are required, not ornamental

Source K06 hashes, HX89 executable hashes, negative tests, repeated native runs, decoded HX89 oracle, workload-derived digest, AC/DC KCL residual, actual BVH bounds and selective AVX2 instructions all participate in the canonical gate. Read `00_CONTROL/run_canonical_unified_acceptance.py` and the machine-readable evidence under `07_FRESH_TEST_EVIDENCE/UNIFIED_CANONICAL_ACCEPTANCE_20261102`. The historical 36-test suite is retained as the original bridge regression and must not be substituted for the newer unified suite.
