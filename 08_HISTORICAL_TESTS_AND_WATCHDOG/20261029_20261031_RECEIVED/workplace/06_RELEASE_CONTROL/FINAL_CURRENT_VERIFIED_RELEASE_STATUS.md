# VOID/HX89 — current verified cumulative release status

**Project snapshot:** cumulative `workplace` as packaged after the 2026-10-29 corrected verification run. Preserve the original uploaded archives, all old source snapshots, and the earlier failed regression logs.

## Newly completed native whole-machine verification

- Accepted run: `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793289015588851085.json`.
- Result: **21/21 named executable gates PASS**, **0 FAIL** on this run, checked from the actual JSON receipt.
- Original M00–M115 canonical ledger: **116 distinct ordered IDs**, all historical-preservation flags YES. This does not certify the corresponding proposed physical functions.
- Existing source/archive SHA256 and K01–K06 includes, original HX89 native suite, standalone watchdog, EntropyAVX, real CPU native batch, CPU→HX89→subsequent CPU feedback, actual cache interventions, native AVX2 history probes, reversible **digital C lattice gas** and executed HX89 Polyform all have corresponding gate receipts in the accepted run.
- Extended full-stack run: 8 cycles and 32 actual native CPU interventions, with source/trace and subsequent-command linkage checked. Independent randomized 3-intensity history path: 144 native history trials through 8 integrated HX89 cycles.
- Last power/timing crossover is a *processor timing contrast*, not an independently measured voltage/temperature/current signal; it must not be cited as thermal analog computation.

## Failure retained and actual defect correction

- Before repair: `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793288682150218356.json` recorded **20/21 PASS**, 1 FAIL: standalone EntropyAVX BVH stress test returned `Permission denied` during overlapping builds; old output filename was shared between native runs. This failed source test is retained.
- Repaired derivative `00_CONTROL/run_workplace_watchdog.py` creates a **per-run unique BVH executable name**, validates that the file is executable and runs all **3,003 build/refit cases**. The standalone post-fix log `04_TESTS_AND_LOGS/20261029_RESUMED/FINAL_BVH_RACE_FIX_WATCHDOG.log` records 11/11 named tasks passing.
- `00_CONTROL/execution_guard.py` adds **exclusive process-level locking** around native whole-machine verification (nested watchdog inherits the lock); conflicting runs refuse to execute instead of racing. This is development tooling, not a novel physical computing operator.

## Source and research integrity

- 116 historical milestone records and K01–K06 original netlists retained, not rewritten to show false physical completion.
- All historical archives, recovered HX89 source, EntropyAVX originals and derivative, actual CPU batch toolchain and K06 source remain present. The root map is `WORKPLACE_START_HERE.md`.
- Original hardware-measurement ledgers have not been filled with inferred or fabricated measurements. All failed attempts remain recoverable in `04_TESTS_AND_LOGS/`.

## Physical acceptance (not established)

The project presently demonstrates an *actually executed digital/native host control loop*, authentic CPU cache/timing observations, and reversible HX89 software semantics. **It does not yet show an independently calibrated physical continuous on-die computing operator, controllable MOSFET weak-inversion analog state, verified collective charge memory, electrically attached K06 device, or complete nonbinary CPU-native machine.** Those are not passed by the 21 software/native verification gates.

## Reproduce and verify

```
cd workplace
python3 00_CONTROL/run_whole_machine.py --cycles 8 --cache-causal --history-causal
```

Review the newly emitted `WHOLE_MACHINE_ACCEPTANCE_<runid>.json` for named gate status and original physical-false fields. The folder-release kit's SHA-256 manifest verifies the entire as-shipped tree, including failures.


## 2026-10-29 CPU-material acceptance extension

Full restored source SHA audit: 8,122 preserved input files verified before derivative changes. A fresh native whole-machine regression is recorded at `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793293053849210191.json`: **21/21 PASS** after preserving and repairing the first 18/21 failure.

An extended actual machine path executed original 4-cycle HX89 5D/Q²/reversible gas/AVX/cache/history -> 288 cross-core CPU measurements (5 ms and 50 ms hold) -> executed HX89 result -> subsequent native CPU command. Independent schema/hash/control tests passed 7/7. Full raw results and candidate falsification report: `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/FINAL_PHYSICAL_GATE_EXECUTION_20261029.md`.

The experiment **did not show statistically consistent multi-level physical memory**. It did not measure die temperature, analog subthreshold gate current, or a physically assembled K06 interface; physical Gate K is still NOT VERIFIED. The native/full-stack tests are not a substitute for these missing material measurements. Failures and repairs were preserved. New tools: `cross_core_material_gate.py`, `cpu_cross_core_history.c`, and `00_CONTROL/repair_restored_native_build.py`.
