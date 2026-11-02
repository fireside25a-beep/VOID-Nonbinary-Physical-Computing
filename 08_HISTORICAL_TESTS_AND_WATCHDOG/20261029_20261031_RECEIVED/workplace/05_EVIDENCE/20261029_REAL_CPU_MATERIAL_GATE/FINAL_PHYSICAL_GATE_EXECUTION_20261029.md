# VOID HX89 physical nonbinary gate: executed final attempt, 2026-10-29

## Actual live results
- Complete source restored from sealed nine-folder release: 8,122 file SHA-256 comparisons passed before any changes to this derivative.
- Original full 21-gate execution **21/21 PASS** after correcting absolute-path stale CMake cache, the restored executable, and subprocess startup timeout. Receipt: `WHOLE_MACHINE_ACCEPTANCE_1793293053849210191.json`. The prior 18/21 run and its failures were preserved.
- New full connected experimental chain **PASS** for 4 actually executed HX89/native CPU/Q²/reversible digital gas/cache/history cycles, then **288 genuine cross-core CPU history observations**, executed HX89 result, and a subsequent native CPU command. Source and raw receipt identities checked independently.
- New adversarial evidence tests: **7/7 PASS** after fixing test script; all prior failed attempts retained.

## Material test falsification
The 288 samples are 144 native hardware readbacks at 5 ms hold and 144 at 50 ms. The real stimulus used idle, partial scalar and full AVX2 activity on CPU 0; the identical readout ran on CPU 4, with independently timed work.
| Hold time | Readout median in nanoseconds: idle/mid/high | High - idle median ns | Positive vs negative paired differences | two-sided sign p |
|---|---|---:|---|---:|
| 5 ms | 90495724.0 / 89445088.5 / 86706716.0 | -3789008.0 | 18 / 30 | 0.1114 |
| 50 ms | 86659882.5 / 87131902.5 / 86166176.0 | -493706.5 | 20 / 28 | 0.3123 |

Results do **not** reproducibly establish three independently distinguishable retained analog states. Significant confounders remain: virtual CPU mapping, uncontrolled temperature, voltage/frequency policy, scheduling, cache interactions and digital state. The host exposed no readable sysfs CPU temperature, RAPL energy or current frequency gauges during screening. This is an executed falsification attempt, not measured transistor voltage.

## Truth boundary
**Passed:** actual native CPU execution; full HX89 5D/Q², emitted gas Polyform and native return; real cache/history probes; entire command feedback; provenance and tampering checks.
**Unproven:** physical MOSFET weak-inversion bias control in the CPU, direct analog readout, identified analog current-driven useful computation, physical multilevel write/hold/read memory, a real assembled K06-to-CPU physical causal connection and a complete nonbinary computing substrate.
No synthesized analog voltages, fake power/temperature measurements or fabricated Gate K TSV rows were written.

## Next decisive science
A direct silicon-material proof requires *one physical state with calibrated controllable stimulus and independently measured response*, three-level discriminability/retention, an input-output operation driven by the substrate rather than a digital postprocessor, and negative controls that eliminate timing-only cache/scheduler alternatives. Existing CPU instructions and source netlists alone do not verify that claim. Candidate routes remain CPU thermal/clock/power physical coupling or externally accessible analog elements, but they must have actual measured causal access. This is a physical gate, not a software PASS to be forced.

Sources: 2015 thermal covert channel experiment (Masti et al., USENIX Security) and Intel Digital Random Number Generator Software Implementation Guide (physical thermal source followed by digital conditioning).
