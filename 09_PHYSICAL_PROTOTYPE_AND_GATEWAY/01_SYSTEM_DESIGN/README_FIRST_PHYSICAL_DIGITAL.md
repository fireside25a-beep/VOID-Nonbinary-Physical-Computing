# VOID R08 + HX89: one experiment, two real execution modes

## One source of truth

The nine active R08 `.cir` and `.lib` source files in `01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE` define the physical circuit. Their archive hashes and historical R06 branches are preserved separately. The editable `*.kicad_sch` sheets under `01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS` capture every source component and SPICE pin connection through net labels. These sheets have not been KiCad ERC/DRC-verified in this environment, and have NO assigned production footprints or manufacturing claims.

## Integrated digital path, executed

Source-linked native RC subset and actual AC/DC C11 source -> charge observations -> real repaired EntropyAVX BVH -> native compiled HX89 decision -> CPU scalar/AVX2 batch/cache path -> previous work-state included in next HX89 input and K06 model drive. Cryptographic HX89 and circuit-source checks are in the native driver. Canonical executable: `05_HX89_K06_BRIDGE/03_UNIFIED_NATIVE_CLOSED_LOOP/build/void_unified`. Independent six-mode ablations and negative tests are under `07_FRESH_TEST_EVIDENCE/UNIFIED_CANONICAL_ACCEPTANCE_20261102`.

The RC runtime is explicitly a **selected K06 R/C network**. AC/DC was developed as a distinct passive nodal experiment, reused as a software conditioning feature. Its circuit is NOT a proven full K06 transistor/diode/inductor operating point. EntropyAVX geometry is derived from state and is a controller feature; it is not physical sensor acquisition.

## Integrated physical target, not falsely passed

K06 power -> material interface and nonlinear RC/diode network -> actual charge/force state -> independently calibrated high-Z measurements -> timestamped acquisition -> same HX89/CPU controller -> protected electrode excitation -> next physical measurement. The concrete source-node wiring, expanded procurement role inventory, and negative-tested native bench-file ingestion are in this folder. There is **no user-supplied real bench recording or connected ADC/DAC driver** in this release session. The physical loop cannot be marked verified until independent hardware and a source-bound acquisition/actuation path produce measured evidence. No test fixtures are counted as measurements.

## Why both are retained

The digital mode is an exact, reproducible software regression/reference. The physical mode tests nonlinear, leakage, tolerance, cross-coupling and instrument-loading effects on real parts; it will become authoritative for physical claims only with recorded actual inputs/outputs and instrumentation calibration. They share the R08 terminal map, HX89 binary identity, epoch and decision schema, error handling, and provenance policy. They never substitute one another's evidence.

## Hard invariant

Original sources and historical failures are retained. Hardware-origin samples never come from the digital solver, and a synthetic CSV is never accepted as experimental evidence. A hash detects later file changes; a hash alone cannot authenticate whether the original data came from physical hardware. Independent power and unplugged-host tests must precede host gateway operation.
