# Build and run — reproducible engineering instructions

## Required environment

Tested current development platform: Linux x86-64, GCC/G++, CMake, Make, Python 3 with original HX89 dependencies and CPU support for relevant AVX modes. Some native programs pin threads to real schedulable CPUs. Tests must FAIL cleanly when the host does not provide a required instruction or port; neither simulated timing nor fabricated CPU sensors are acceptable replacements.

### Bootstrap and verify

From the complete restored `workplace/` root:

```bash
python3 -S 00_CONTROL/repair_restored_native_build.py
python3 -S 00_CONTROL/run_canonical_release.py --repeat 2 --cycles 4 --material-blocks 8
```

The bootstrap preserves stale CMake cache trees by renaming rather than deleting them. The canonical runner sequentially executes the whole original machine and material candidate twice, with append-only logs and distinct accepted-run JSON receipts.

### Direct single integrated run

```bash
python3 -S 00_CONTROL/run_whole_machine.py \
  --cycles 4 --cache-causal --history-causal --material-history --material-blocks 8
```

It runs all original 21 active native gates and adds three gates: genuine connected material experiment, independent sample/control verification, and seven adversarial tests using real samples.

### Longer native stress and independent verification

```bash
python3 -S 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/cross_core_material_gate.py \
  --out NEW_EMPTY_DIRECTORY --blocks 8
```

A new output path is mandatory. The source itself executes the full four-cycle machine before cross-core acquisition. It refuses to overwrite original evidence. For the trace adversarial tests, in `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/`:

```bash
VOID_REAL_CROSS_CORE_RUN=/absolute/path/to/NEW_EMPTY_DIRECTORY \
python3 -S -m unittest -v test_cross_core_material_gate
```

### Determinism contract

- Fixed native program source and bounded mode permutations are verified by source hash and trace schema.
- Runtime receipt names are unique, and repeats never overwrite earlier acceptance JSON.
- Original archive SHA-256 values are computed before and after execution.
- Actual timing/current/noise observations are **not promised deterministic**; a statistically different value is data, not a reason to edit a row.
- The watchdog is local executable verification software, not an autonomous assistant working between turns.
- Any failure leaves a real log and is not upgraded to PASS when a later run succeeds.

## Where to find results

`04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_<runid>.json`, `04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/`, and `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/`.

The runbook and original historical sources remain unchanged, and the nine ZIP delivery is only a transport of this single tree.
