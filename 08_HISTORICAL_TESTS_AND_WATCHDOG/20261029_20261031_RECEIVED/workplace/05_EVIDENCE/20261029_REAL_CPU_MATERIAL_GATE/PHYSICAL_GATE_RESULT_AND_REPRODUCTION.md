# VOID / HX89 — Physical substrate acceptance attempt (2026-10-29)

## What was executed

The sealed original nine-folder `workplace` was reconstructed and all **8,122** original files passed SHA-256 comparison, with **1,196,257,830** bytes confirmed. The material experiment is an additive derivative. Original uploaded archives, R08 circuit sources, HX89 original source, and historical ledger fields were preserved unchanged.

The new `cpu_cross_core_history.c` uses actual CPU affinity and 3 randomized stimulus levels. A workload is executed on CPU 0, held for 5 or 50 ms, and then the same timed observation is executed on CPU 4. It uses actual native scalar/AVX2 instructions and RDTSCP/CLOCK_MONOTONIC_RAW, not calculated temperatures.

`cross_core_material_gate.py` ingests these *raw acquired* observations, validates six crossover permutation schedules, feeds a measured contrast into the original HX89 Q² machine, and actually executes the next native CPU batch command from the resulting HX89 state. Input and output source hashes are recorded. The gas engine and HX89 Q² remain digital computations.

## Actual higher-sample evidence

| Hold | Actual trials | Median observation ns: idle / mid / high | High minus idle median, ns | Paired high>idle / high<idle | Exact two-sided sign p |
|---|---:|---|---:|---|---:|
| 5 ms | 144 | 88325411.0 / 91124783.0 / 90072650.5 | +1747239.5 | 23 / 25 | 0.8854 |
| 50 ms | 144 | 118204754.0 / 115985984.5 / 120633616.5 | +2428862.5 | 26 / 22 | 0.6655 |

The order direction was inconsistent and paired signs were close to chance. Processor scheduling, virtualization, voltage/frequency changes, cache and execution-port dynamics remain possible contributors. **No repeatable distinguishable three-level material state, retention effect attributable to charge/temperature, or native nonbinary operation was demonstrated.** Do not turn this into a positive physical Gate K record.

## Actual tests and failures

- Initial compiler run refused a C `PRIu64` argument type mismatch; corrected and compiled with `-Wall -Wextra -Werror`.
- First cross-core wrapper run generated real observations, but its schedule verifier failed due a missing permutation entry. Failure preserved. Corrected and rerun.
- 72 and 288 genuine timing samples were independently verified; both yielded real HX89 Q² execution and next CPU workload.
- Seven adversarial tests passed after repairing a test-harness `run` member that shadowed `unittest.TestCase.run`. The failing first run is retained.
- Original `workplace` release-restoration problem: a historical CMake cache held absolute paths to `/mnt/data/workplace`, which failed after restoration; a sealed build tree was preserved under `build_workspace_cache_from_sealed_20261029/` and native binaries reconfigured and rebuilt for the derivative copy. Restored executable permissions were also absent for some copied binaries. Original releases unchanged.
- A Python subprocess bound test was tripped by unrelated Python startup instrumentation; derivative test now invokes Python `-S` with a bounded 15-second timeout, and 11/11 affected test methods passed.
- Full native runner acceptance receipts and the final corrected run are in `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/`. Never replace a failed run with a later successful receipt.

## Source-to-physics gate still required

A claim of **physically native nonbinary computation and material memory** requires independent causal discrimination of a *nonbinary physical state* from a purely digital/software intermediary.

For an internal CPU mechanism, the next decisive experiment must identify an actual controllable physical bias or excitation and an independently interpretable sensor/response (e.g. chip-local temperature/frequency/power with calibrated errors, or directly accessible charge/current). In addition, it must reproduce at least three independently distinguishable states at a specified hold interval on several test sessions, demonstrate a useful nonlinear transformation with multiple interacting physical input dimensions, and survive controls for scheduling, caching, digital feedback and virtualization. 
An HX89 command changing CPU workloads is not sufficient if the alleged analog state only exists as a timing number later manipulated digitally.

No on-die user-directed weak-inversion gate electrode, analog current monitor, independently sampled K06 probe, or assembled analog material path was found or fabricated in this session. No analog voltage/current records are synthesized.

## External independent anchors

1. Intel Digital Random Number Generator implementation guide (2018) describes a physical thermal-noise entropy source, **followed by digital conditioning**: https://www.intel.com/content/www/us/en/developer/articles/guide/intel-digital-random-number-generator-drng-software-implementation-guide.html
2. Masti et al., Thermal Covert Channels on Multi-core Platforms (USENIX Security 2015), provides independent thermal-channel evidence using measured core temperatures: https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/masti

## State of the final requested milestone

**NOT ACCEPTED: the final nonbinary physical machine has not been established by this experiment.** The new source, raw evidence, executed HX89/native feedback, adversarial tests and full release provenance have been preserved for further falsifiable work.
