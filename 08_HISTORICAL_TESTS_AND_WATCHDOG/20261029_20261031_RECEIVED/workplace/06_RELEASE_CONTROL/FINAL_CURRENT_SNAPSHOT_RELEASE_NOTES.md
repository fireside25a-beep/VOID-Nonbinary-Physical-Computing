# VOID / HX89 — Current complete workplace release record

Scope: The entire as-found `workplace/` including original preserved user input bytes, R08 K01–K06 schematic source, historical release ZIPs, HX89 source and executable outputs, EntropyAVX source and repaired derivative, CPU batch experiment and full HX89 feedback toolchain, all test directories (including failures), physical-research references, canonical 116-milestone ledger and watchdog. Files have not been pruned, relocated or replaced to achieve the release.

## Entry point
`WORKPLACE_START_HERE.md` is the primary directory map and accurate invocation guide. `00_CONTROL/CANONICAL_MASTER_PLAN.md` and `CANONICAL_IMPLEMENTATION_LEDGER.tsv` are the single canonical 116-milestone plan. Individual scripts and native execution live under `03_NATIVE_TOOLCHAIN/`.

## Latest verified acceptance and attempted reproduction

- Preserved completed whole-machine acceptance: `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793288555943855094.json`, 21/21 PASS, real native x86/HX89/EntropyAVX/cache/three-intensity observation and verification gates, 12 connected cycles; all physical nonbinary proof fields `false`.
- New reproduction `WHOLE_MACHINE_ACCEPTANCE_1793288682150218356.json`: 20/21 PASS, one intermittent failure at the independent watchdog BVH binary execution (`Permission denied`), preserved unchanged.
- Subsequent watchdog derivative race repair: unique executable per watchdog run in `00_CONTROL/run_workplace_watchdog.py`; fresh complete 11/11 watchdog run PASS in `04_TESTS_AND_LOGS/20261029_RESUMED/FINAL_BVH_RACE_FIX_WATCHDOG.log`.
- Further combined verification attempts ended without a complete new acceptance record under tool time limits or overlapping-execution guard. Their partial logs are retained, NOT promoted to passing runs.
- The new exclusive native execution guard prevents overlapping source compilation and testing in the same working tree. It is **test-tool concurrency control**, not a novel computing substrate.

## Reproduction
From `workplace/`, on a compatible x86-64 toolchain:

`python3 00_CONTROL/run_whole_machine.py --cycles 12 --cache-causal --history-causal`

The command may require more time than a short interactive shell allows. Watch `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/` for its append-only journal and inspect the *latest completed* `WHOLE_MACHINE_ACCEPTANCE_<run_id>.json` for pass/fail counts. Do not claim success from an incomplete stdout log. Run only one watchdog/whole-machine test process at a time; do not run builds concurrently. Original compiled binaries and logs belong in this release as artifacts from the actual recorded environment; rebuild on your own machine when necessary.

## Scientific acceptance boundary
This is a complete retained engineering **workplace** and native execution/test suite, not certification of a physical nonbinary general-purpose computer. HX89 reversible gas is an executable discrete model; R08 K06 is a preserved electrical design and has not been wired to a verified processor analog substrate. Actual controllable weak-inversion, collective continuous-state storage, semiconductor physical material operations and bootable nonbinary machine remain unverified. No voltage/temperature/charge measurements have been invented. The manifest distinguishes preserved real native test evidence from those open physical gates.
