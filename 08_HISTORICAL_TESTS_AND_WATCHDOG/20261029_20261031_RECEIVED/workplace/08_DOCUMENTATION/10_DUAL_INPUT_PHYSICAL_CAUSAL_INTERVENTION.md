# VOID/HX89 — Native, simultaneous two-input CPU intervention

## Executed material-candidate experiment

The actual HX89 native full-stack executes its existing CPU, 5D, Q², cache, reversible **digital** lattice gas, and Polyform steps. Its executed output sets the control input for the next intervention. Two genuine AVX2 worker threads then concurrently drive separately pinned CPUs. A third core runs an identical real workload at predetermined 2 ms and 20 ms readout delays.

Every four-trial randomized block visits `00, A, B, A+B` exactly once. We calculate the interaction contrast directly from actual counter readings:

`interaction = Y(A+B) − Y(A) − Y(B) + Y(0)`

The recorded values are **real processor time** measured using `RDTSCP` and `CLOCK_MONOTONIC_RAW`; they are neither generated voltage samples nor a silicon temperature monitor. A material-state claim requires an independent hardware measurement and repeatable causal separation from cache/scheduling/virtualization.

## Recorded, independently verified outcomes

| Experiment | Hold | Real samples | Interaction median (ns) | Paired interaction signs +/− | Exact sign-test p |
|---|---:|---:|---:|---:|---:|
| 1 | 2 ms | 64 | -30,751 | 6/10 | 0.4545 |
| 1 | 20 ms | 64 | -27,632 | 7/9 | 0.8036 |
| 2 | 2 ms | 64 | +70,081 | 11/5 | 0.2101 |
| 2 | 20 ms | 64 | -28,458 | 8/8 | 1.0000 |

Two complete independent experiment runs each acquired **128** real observations (256 total), executed the original four-cycle HX89 stack, and executed the following native CPU command derived from HX89. Both passed eight adversarial/data-integrity tests. Earlier rejected source/acquisition runs remain in the broader worktree.

### Predefined causal controls

1. Four randomized conditions, balanced per block.
2. Identical reader source, bound to a third virtual CPU; two workers are simultaneously active.
3. Identical input seed and stimulus type across runs; no tuning of experimental settings to the measured interaction sign.
4. Two predetermined hold times of 2 ms and 20 ms.
5. Full original HX89 feedback and native binary identities independently verified against raw execution.
6. Negative tests reject missing, shuffled, zero, non-overlapping, and altered hardware traces.

## Empirical decision

**Do not promote to physically nonbinary computation or physical analog memory.** The interaction sign is not stable across the two repeated acquisitions. A very low p-value from an isolated condition would not pass predeclared replication or multiple-comparison controls. The host has virtual CPU mappings and does not expose a calibrated independent temperature/voltage/current readback. Latency contrasts can reflect scheduling and cache effects rather than a useful material operator.

## Next decisive hardware experiment

Read an independent analog or calibrated hardware thermal/power/acoustic channel during simultaneous A/B/A+B stimulation and compare it against the same randomized design. Require nonlinear response with reproducible hold-time evolution across independent sessions, a held-out task beating an additive baseline, and a measured response that disappears when the physical channel is interrupted. No requirement to rewrite HX89 or delete its real native machinery.

## Independent scientific grounding

- Liang et al., **Physical reservoir computing with emerging electronics**, *Nature Electronics* 7 (2024), DOI: https://doi.org/10.1038/s41928-024-01133-z
- Masti et al., **Thermal Covert Channels on Multi-core Platforms**, USENIX Security (2015), https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/masti
- Intel CPU thermal monitoring architecture, via IA32_THERM_STATUS; physical access requires exposed, authorized sensor interfaces. Reference: https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html

## Reproduce

From `workplace/` after restoring the entire canonical source archive:

```sh
python3 -S 00_CONTROL/repair_restored_native_build.py
python3 -S 03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/dual_reservoir_hx89.py --out AN_UNUSED_NEW_DIRECTORY --blocks 16
```

Raw runs: `04_TESTS_AND_LOGS/20261029_DUAL_CPU_REPEATED/`. No fabricated analog measurement fields are populated.
