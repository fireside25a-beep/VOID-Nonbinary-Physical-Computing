# VOID/HX89 physical material gate continuation

This incremental working copy extends the previously sealed nine-folder VOID workplace. Do not discard or overwrite the nine original source archives.

**Actual results:** source restored; 21/21 whole native software/hardware-instruction gates PASS after source-local build-cache repair; full HX89 model -> native cross-core intervention -> HX89 feedback chain executed with 288 independent timing samples; 7/7 adversarial tests PASS. The final physical nonbinary/material-memory proof did **not** pass.

Review `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/FINAL_PHYSICAL_GATE_EXECUTION_20261029.md` and the raw receipts before running anything.

Rebuild native EntropyAVX after moving between directories:

```sh
python3 -S 00_CONTROL/repair_restored_native_build.py
```

Run exact genuine extended 4-cycle whole-machine and CPU state-history experiment into a NEW directory:

```sh
python3 -S 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/cross_core_material_gate.py --out NEW_UNUSED_DIRECTORY --blocks 8
```

Independently check the real raw trace:

```sh
VOID_REAL_CROSS_CORE_RUN=NEW_UNUSED_DIRECTORY python3 -S -m unittest -v test_cross_core_material_gate
```

The last command runs from `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/`, or with `PYTHONPATH` set to that directory. The physical proof registers remain unpopulated without real calibrated analog measurements. Status flags are deliberately conservative, never synthesized as positive results.
