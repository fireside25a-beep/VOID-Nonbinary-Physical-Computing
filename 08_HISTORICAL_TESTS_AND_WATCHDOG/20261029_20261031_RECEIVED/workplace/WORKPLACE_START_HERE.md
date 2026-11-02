# VOID / HX89 — Cumulative workplace entry point

This is the **preserved cumulative source and experimental execution workplace**, not a rewritten machine. Start with `00_CONTROL/CANONICAL_MASTER_PLAN.md` and `00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv`; these retain the **116 historical milestone IDs M00–M115**, historical status and dependencies. Scientific release claims must follow the evidence, not the milestone count.

## Directory map (one source of truth)

| Folder | Purpose |
|---|---|
| `00_CONTROL/` | Authoritative master input, 116-row milestone planner/ledger, source inventory, independent bounded watchdog and whole-machine gate runner. |
| `01_SOURCES_VERIFIED/` | Original uploaded archive bytes, as-received extracts, historical master, untouched source provenance. The original split research ZIP is reconstructed byte-exact during folder restoration. |
| `02_ACTIVE_R08/` | Preserved VOID R08 architecture, K01–K06 netlists and included `.lib` circuits, physical hardware/evidence contracts. |
| `03_NATIVE_TOOLCHAIN/HX89/` | Original HX89 native five-dimensional / Q² / reversible execution, Polyform, snapshots, and original source tests. |
| `03_NATIVE_TOOLCHAIN/EntropyAVX/` | Separate, repaired EntropyAVX *derivative*, including native launcher/BVH checks. Originals remain in sources. |
| `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/` | Real CPU scalar/SIMD/cache intervention source, actual HX89 feedback bridge, reversible **digital** lattice gas and Polyform execution; timed cache and 3-intensity history probes. |
| `04_TESTS_AND_LOGS/` | Original and repeated integration runs, raw traces, negative tests, failures, output proofs, append-only watchdog events. Do not overwrite old run directories. |
| `05_EVIDENCE/` | Research sources, physical CPU mechanism screening, recorded observations and limitations. |
| `06_RELEASE_CONTROL/` | Runbooks, source and release inventories, exact executed status and packaging provenance. |
| `07_DELIVERY/` | Delivery notes; final transport ZIPs reside **outside** this tree. |
| `90_PRESERVED_PROVENANCE/` | Historical provenance retained without silently reconciling disagreements. |

## Reproduce the complete tested native execution

From this `workplace/` root on an appropriately equipped x86-64 host with Python 3, GCC/G++, Make and the original build dependencies:

```
python3 00_CONTROL/run_whole_machine.py --cycles 12 --cache-causal --history-causal
```

This invokes the independent source/archive/circuit gates, builds/tests original HX89 paths, tests EntropyAVX and native CPU batch, runs the real 12-cycle HX89 feedback paths, real cache eviction/readback and the actual 3-intensity history candidate, then independently verifies the recorded traces. **Read the terminal acceptance JSON**: a subprocess having run is not the same thing as a PASS; preserve its failure/negative logs. The full 116-milestone ledger is an inventory, *not* a 116/116 physical-accomplishment claim.

Additional repeated/extended execution entry points:

```
python3 00_CONTROL/run_workplace_watchdog.py --runs 1
python3 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/full_stack_cycle.py --rounds 64 --base-work 4 --cache-probe --out AN_UNUSED_NEW_DIRECTORY
python3 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/verify_full_stack.py AN_UNUSED_NEW_DIRECTORY
```

Do not reuse an output directory. New run arguments/host capability can yield different results; never copy results from historical runs as if newly measured. The watchdog is a **software-side bounded verification process**, not a continuously self-awakening ChatGPT agent or a physical VOID component.

## What is real, what remains unproved

Actual x86 instructions and cache operations, measured CPU timing, HX89 five-dimensional/Q² instructions, the native accelerator, emitted Polyform, reversible lattice-gas **software model**, feedback into next workload, and source integrity gates have executable source and saved evidence. The transistor weak-inversion effect, independently observed useful material memory, CPU-accessible analog state, and fabricated/connected K06 network have **not** been demonstrated as a complete nonbinary CPU-native computation. Conditioned random output, TSC clocks and lattice-model states are not analog voltage/current readouts. Physical proof ledgers must remain free of calculated or invented measurements.

## Multi-folder restoration

The distribution's nine folder ZIPs recreate the exact `workplace/` tree using `RESTORE_VERIFY.py` plus SHA-256 manifests. The two 150 MB original master byte-parts are **not separate extractable research ZIPs**; the restore script concatenates their original bytes into the full ~301 MB research master. Read the distribution's `README_START_HERE.md`, run `python RESTORE_VERIFY.py --verify-only`, then restore into a **new empty destination**. All historical input ZIPs and original source identities are preserved; no Git history is invented or silently updated.

## Final combined cache + 3-intensity machine and failure readback

`06_RELEASE_CONTROL/FINAL_COMBINED_NATIVE_AND_RESTORE_EVIDENCE_20261029.md` is the current definitive additional evidence. The interrupted scheduling-contaminated acquisition and incomplete 21-gate rerun are retained; a separate real 16-cycle simultaneous cache/history/HX89 run and independent verifier passed. For an exact simultaneous run use BOTH `--cache-probe --history-probe` on `full_stack_cycle.py`, not only the two separate watchdog stages.
