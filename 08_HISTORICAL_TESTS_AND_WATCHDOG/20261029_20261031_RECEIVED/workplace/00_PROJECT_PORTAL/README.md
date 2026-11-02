# Canonical project portal

**There is one active native execution path:** `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE` orchestrates the original `03_NATIVE_TOOLCHAIN/HX89`, the independently developed `EntropyAVX` derivative, the R08/K06 source contracts, and the physical candidate experiment.

- `00_CONTROL/run_canonical_release.py` — main repeated integrated test entry point (development/verification tooling).
- `00_CONTROL/run_whole_machine.py` — full suite executable with `--material-history`.
- `00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv` — original M00–M115, same IDs and historical fields.
- `02_ACTIVE_R08/02_PHYSICAL_CIRCUITS/` — actual circuit netlists and linked libraries (not fabricated CPU silicon).
- `04_TESTS_AND_LOGS/` — historical and fresh receipts (successes and failures).
- `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/` — raw cross-core trials, accepted and rejected traces.

No duplicate live application, no renumbered milestones, and no replacement of original versions. Archived source snapshots are deliberately preserved as historical artifacts.

Read the [latest two complete native whole-machine runs](../06_RELEASE_CONTROL/CANONICAL_FINAL_REPEAT_AND_RELEASE_20261029.md) and [current native plot](../09_RESULTS_VISUALS/native_repeated_acceptance.png). Original material proof remains unverified.

## New acquired two-input CPU physical response

Read `../08_DOCUMENTATION/10_DUAL_INPUT_PHYSICAL_CAUSAL_INTERVENTION.md` and run the current whole-machine coordinator with `--dual-physical --dual-blocks 16`. This runs actual simultaneous CPU threads, independently reads timings and passes them through HX89. Nonbinary analog silicon operation is not declared proven.
