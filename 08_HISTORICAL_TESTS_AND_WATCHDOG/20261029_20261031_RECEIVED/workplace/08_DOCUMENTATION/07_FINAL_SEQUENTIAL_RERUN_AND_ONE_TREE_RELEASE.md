# VOID/HX89 complete project — final repeated execution and release handoff

The release is a **single** authoritative `workplace/` tree. Folder ZIPs are transports, not separate projects. All original uploads, historical snapshots, netlists, research cache, native code/binaries, test logs and failure records are preserved.

## Actual fresh repeated execution

- **Run 1: 24/24 gates PASS, 0 FAIL**, native exit 0. Receipt `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793297152848705731.json`; raw log `04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/canonical_1793297149910189732/01_complete_machine.log`.
- **Run 2: 24/24 gates PASS, 0 FAIL**, native exit 0. Receipt `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793297283801507383.json`; raw log `04_TESTS_AND_LOGS/CANONICAL_RELEASE_RUNS/canonical_1793297149910189732/02_complete_machine.log`.

Each run used the full native machine, not precomputed or substituted samples: original HX89 five-dimensional/Q²/Polyform and reversible **digital lattice model**, EntropyAVX rebuilt native executable, CPU scalar/SIMD/cache activities, randomized three-intensity and cross-core measured history, CPU→HX89→next-CPU closed loop, source integrity, negative tests and exact trace verification.

Native test success **does not** establish a functioning nonbinary material memory or physical K06-to-CPU link. The physical Gate K remains unverified in the ledger, and prior scheduling-related failed acquisitions are retained instead of replaced. Under a different host or OS load, measured timing is not bitwise deterministic; controlled code paths and integrity criteria are reproducible.

## Professional hierarchy

- `00_PROJECT_PORTAL/`, `README.md`: one project start.
- `00_CONTROL/`: active whole-machine runner, one 116-row ledger, independent watchdog and provenance gates.
- `01_SOURCES_VERIFIED/`: authoritative originals and sealed historical research archive.
- `02_ACTIVE_R08/`: K01–K06 and referenced physical circuit/source materials.
- `03_NATIVE_TOOLCHAIN/HX89/`, `EntropyAVX/`, `CPU_VOID_BATCH_CYCLE/`, `ResearchCache/`: executable toolchain and separate research infrastructure.
- `04_TESTS_AND_LOGS/`: repeated native runs and **all failures**, output and raw trace receipts.
- `05_EVIDENCE/`: original physical hypotheses, measured CPU candidate trials, falsification receipts.
- `06_RELEASE_CONTROL/`, `07_DELIVERY/`: full release instructions, file identities and transport proofs.
- `08_DOCUMENTATION/`, `09_RESULTS_VISUALS/`: architecture, results, diagrams and raw-data plots.
- `90_PRESERVED_PROVENANCE/`: prior versions, never silently substituted as active sources.

## Build and rerun from restored workplace

```sh
python3 -S 00_CONTROL/repair_restored_native_build.py
python3 -S 00_CONTROL/run_canonical_release.py --repeat 2 --cycles 4 --material-blocks 2
```

Use the ten-folder restore kit from the release root. Every ZIP is below **200,000,000 bytes**; the complete research master >200 MB is reconstructed byte-exact from its two original parts. Original versions are not removed.
