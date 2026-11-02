# VOID/HX89 workplace — final cumulative handoff (2026-10-29)

## This is an intact working tree, not a new isolated demonstration

Restore all nine logically separated ZIP modules using the included `RESTORE_VERIFY.py`. Everything extracts to the SAME `workplace/` root; all existing source identities, historical archives, K01–K06 circuit netlists and libraries, native HX89, repaired EntropyAVX derivative, CPU batch, cache and history probes, original experimental and negative logs, and the 116-milestone ledger are retained. Nothing was intentionally dropped or removed. The original 301,454,742-byte combined historical master ZIP is reconstructed byte-exact from its two 150,727,371-byte parts to obey each transport file's sub-200-MB limit.

## Execution order and source map

1. `WORKPLACE_START_HERE.md` and `00_CONTROL/VOID_HX89_EXPANDED_MASTER_INPUT_COPY_PASTE_20261029.txt` — authoritative project intent and historical constraints.
2. `00_CONTROL/CANONICAL_MASTER_PLAN.md`, `CANONICAL_IMPLEMENTATION_LEDGER.tsv`, `ACTIVE_NETLIST_INVENTORY.tsv` — original M00–M115 IDs, dependencies, evidence gates, circuit source inventory.
3. `02_ACTIVE_R08/02_PHYSICAL_CIRCUITS/` — exact preserved original K01–K06 SPICE sources, all `.lib` dependencies. These are circuit designs, **not** measurements or on-die hardware connections.
4. `03_NATIVE_TOOLCHAIN/HX89/` — original native 5D, Q², reversible chiral/hex-gas digital source and binary execution, Polyform, snapshots and test suite.
5. `03_NATIVE_TOOLCHAIN/EntropyAVX/` — repaired derivative, original preserved separately under `01_SOURCES_VERIFIED/`, including BVH regression and launcher.
6. `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/` — native scalar/AVX2/AVX-512/cache interventions, CPU→HX89→CPU feedback, physical cache-residency timing, real 3-intensity AVX2 history candidate and corresponding independent trace verifiers. These operations are CPU instructions and digital telemetry; NOT proven physical analog nonbinary computing.
7. `04_TESTS_AND_LOGS/`, `05_EVIDENCE/` — original receipts, raw traces, statistical results, adversarial tests, failed and interrupted runs preserved.
8. `00_CONTROL/run_whole_machine.py`, `run_workplace_watchdog.py`, `execution_guard.py` — reproducible bounded native verification. The exclusive-run file lock prevents overlapping watchdogs/rebuilds from corrupting native executable reads. Run one at a time.

### Executable native verification

From the restored `workplace/` root on x86-64 Linux with Python 3, GCC, G++, make and CMake:

```
python3 00_CONTROL/run_whole_machine.py --cycles 8 --cache-causal --history-causal
```

All relevant tests are actual executed source paths; they may fail depending on current host and timing. Read the newly generated `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_*.json` instead of trusting a previous report. The 11-gate watchdog is nested inside the whole-machine runner and inherits the single exclusive lock. **Do not start multiple tests simultaneously:** the preserved release attempts include a real `[Errno 13] Permission denied: './bvh_extended'` failure caused by concurrent rebuild and execution, followed by the lock repair and a negative concurrency test.

A preserved earlier complete 12-cycle cache+history execution `WHOLE_MACHINE_ACCEPTANCE_1793288555943855094.json` shows **21/21 stages PASS**; the preservation of that receipt does not certify subsequent interrupted/failed attempts. Physical silicon analog acceptance remains false.

## Physical proof boundary

Native instruction execution, cache effects and digital HX89 feedback are real executed host behaviors. The lattice gas remains a reversible **software model**, and R08 K06 is an electrical **netlist**. No actual weak-inversion gate-bias access, independently measured multilevel analog on-die memory, assembled K06 CPU coupling, or full physical nonbinary machine was proven. Preserve physical evidence registers unfilled until raw as-built measurements exist. The original 116 milestones remain historical IDs, not a 116/116 implementation pass.

## Release integrity

The separate delivery folder contains nine ZIP modules smaller than 200,000,000 bytes each, `RESTORE_VERIFY.py`, an exact per-file SHA-256 inventory, module hashes, and a fresh-restoration test receipt. A genuine source/binary mode is preserved for POSIX executables by the updated restore tool. All originals are retained under their original directories; modules are transport divisions, not forks.
