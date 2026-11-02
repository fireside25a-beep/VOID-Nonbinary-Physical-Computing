# VOID/HX89 — final combined CPU/cache/history native execution and release record

## Identity and immutable source policy

This is a continuation of the original R08/M00–M115 architecture. All original archives and historical ledger fields are retained; source fixes apply only to derivative tools in `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/`. No physical CPU gate-bias or K06 on-die connection is claimed.

## Exact interrupted failure

The original simultaneous cache + 3-intensity HX89 acquisition failed in the saved run `04_TESTS_AND_LOGS/20261029_FINAL_FULL_COMBINED/CYCLE_12` because an actual low-intensity active interval exceeded the observed duty limit (host scheduling delay). `01_full_stack_native.log` records `Low intensity did not leave idle period`; the run has no complete execution acceptance and is preserved. The earlier 21-gate rerun `WHOLE_MACHINE_ACCEPTANCE_1793288682150218356.json` recorded **20 PASS, 1 FAIL** due to a concurrent watchdog runner/build lock, rather than being silently counted as passing.

## Repair and executed verification

The derivative `history_causal.py` can retry only that precisely recognized scheduling-contaminated acquisition, with a maximum of four genuinely fresh native acquisitions. Rejected raw CSV/stdout/stderr remain on disk, accompanied by failure type and cryptographic hashes in the accepted report. No failed values are edited or replaced with generated numbers. `verify_full_stack.py` independently rereads every accepted CSV and, where retry was required, hashes every rejected CSV and requires it to fail for exactly the recorded reason. Other measurement failures remain fatal. The source-based historical case and this fresh final run stay separately identified.

Executed **18/18 tests** in `04_TESTS_AND_LOGS/20261029_FINAL_FULL_COMBINED/03_real_negative_regression_tests.log` with exit code 0, including real native HX89 snapshot/resume, actual 3-intensity acquisitions, corrupted timestamp, CPU migration, altered Polyform and digital-physical claim refusals.

Executed simultaneous 16-cycle live native run `04_TESTS_AND_LOGS/20261029_FINAL_FULL_COMBINED/CYCLE_16_FIXED` with both `--cache-probe --history-probe`, 64 native CPU intervention trials and 288 three-intensity timing observations; 16 following CPU commands changed. `04_combined_16_actual_native.exit` and `05_combined_16_independent_verify.exit` both equal 0. The independent verifier replays source identities, all native traces and HX89 outputs, lattice images, measured raw cache and 3-intensity CSVs, and the exact next-command derivation. This accepted 16-cycle run needed **no scheduling retries**, but retry support was added to handle the actual preserved original failure.

**Latest post-repair cumulative acceptance:** A separate exclusive final whole-machine execution completed **21/21 stages PASS, 0 FAIL**, including the nested 11-gate watchdog, HX89 native suite, EntropyAVX, real cache and three-intensity feedback plus source-integrity and failure controls. Executed log: `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/FINAL_UNBOUNDED_EXCLUSIVE_21_GATE.log`, exit status `FINAL_UNBOUNDED_EXCLUSIVE_21_GATE.exit` = **0** and accepted JSON `WHOLE_MACHINE_ACCEPTANCE_1793289015588851085.json`. A prior concurrently interrupted attempt remains recorded and is not a PASS. Original historical failures and all native raw data remain in the volume.

## Demonstration boundary

Native CPU instructions, cache memory operation, and HX89 execution are real instructions running on the host. The HX89 generated Polyform and reversible 6-channel lattice gas are a discrete digital model. Measured TSC delay does not establish a continuously controlled thermodynamic charge/phase device or independent nonbinary computing substrate. The K06 netlist is not an installed on-die circuit. The physical nonbinary completion claim for every milestone remains NOT_VERIFIED.

## Reproduction

From `workplace` root (GNU/Linux x86-64 with hardware features and toolchains):

```sh
python3 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/full_stack_cycle.py --rounds 16 --base-work 4 --cache-probe --history-probe --out A_NEW_EMPTY_DIRECTORY
python3 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/verify_full_stack.py A_NEW_EMPTY_DIRECTORY
python3 -m unittest discover -v -s 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE -p 'test_history_causal.py'
python3 00_CONTROL/run_whole_machine.py --cycles 8 --cache-causal --history-causal
```

Always use a new directory; do not overwrite original measured data, logs or archives. In response to scheduling or missing ISA support, preserve the failure and report it, not a fabricated success. Transport ZIP verification and full tree SHA checks are independent of native runtime acceptance.
