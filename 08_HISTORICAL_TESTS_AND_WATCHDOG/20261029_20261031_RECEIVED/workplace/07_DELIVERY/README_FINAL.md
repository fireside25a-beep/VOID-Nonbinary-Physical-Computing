# VOID / HX89 cumulative workplace — executable release handoff

## Precise recorded status
- Historical milestones: **116 unique M00–M115**; original fields preserved in `00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv`.
- Latest completed whole-machine acceptance: run `1793285275455087426`, **9/9 stages passed**, 0 failed.
- Highest completed closed-loop run: **64 HX89 cycles, 256 CPU interventions, 54 changed CPU commands**.
- Native tests include 20 positive/negative unittest cases on CPU/HX89 feedback and trace verification.
- Full native HX89 `make check`, AVX BVH/launcher checks, real EntropyAVX 60-frame execution, research cache checks and bounded watchdog were executed and retained as logs.
- K01–K06: nine as-found circuit/library files inventoried and linked, **not assembled or measured as physical circuitry**.
- The active CPU batch bridge is **executed x86 native instruction and software control**, not evidence of a controllable on-die analog computation or physical nonbinary memory.
- Physical weak inversion access, analog write/hold/read, native nonbinary computation, independent K06 physical coupling, and full novel physical machine are **NOT VERIFIED**.

## Authoritative folders
- `00_CONTROL`: unmodified master input, single 116-milestone planner/ledger, source/circuit inventory, bounded runners.
- `01_SOURCES_VERIFIED`: verified originals, full historical master and extracted source snapshots.
- `02_ACTIVE_R08`: derivative application tree, all K01–K06 netlists and supporting libraries, earlier connector.
- `03_NATIVE_TOOLCHAIN`: HX89, EntropyAVX, ResearchCache and actual native CPU/HX89/CPU closed-loop code.
- `04_TESTS_AND_LOGS`: raw stdout/stderr, failure records, every feedback round and whole-suite receipts.
- `05_EVIDENCE`: historical and newly recorded source/verification receipts.
- `06_RELEASE_CONTROL`: earlier cumulative handoff/README.
- `07_DELIVERY`: this handoff, SHA-256 file manifest.
- `90_PRESERVED_PROVENANCE`: preserved earlier planner and unmodified historical material.

## Run from extracted volume
```bash
cd workplace
python3 00_CONTROL/run_whole_machine.py --cycles 64
```
Requires x86-64 with AVX2, gcc/g++, cmake, Python 3, make and the included native binaries/build dependencies. Host instrumentation is real instruction-level only. Every stage logs its actual status; do not promote a run to PASS when any stage fails.

## Historic status and scientific scope
Original historical statuses remain unchanged; execution status is separately logged. The netlists describe candidate external analog networks; no direct physical coupling to a real CPU transistor gate is established by the native instruction tests.

## Reassembly
Download EVERY `.part-###` file into the same folder as `PARTS_MANIFEST.json` and `reassemble.py`, run:
```bash
python3 reassemble.py --verify-only
python3 reassemble.py --output VOID_HX89_WORKPLACE_COMPLETE.tar.zst
tar --use-compress-program=zstd -xf VOID_HX89_WORKPLACE_COMPLETE.tar.zst
```
The split parts are a **single archive**, not independently extractable pieces. Compare the full SHA-256 and member SHA-256 inventory. Never execute unknown source as privileged code.

## Current continuation
The real HX89 → native CPU intervention feedback chain is executed. Future machine-physics work must establish actual controllable silicon/material state dynamics and physically verified collective nonbinary operations, while preserving the entire established software execution and historical evidence chain.

---

## 2026-10-29 continued native full-machine execution (latest)

The authoritative worktree, source archives, original milestone identifiers and underlying historical fields were preserved. The previous HX89 output-format mismatch had been fixed before this continuation; a new real failure was independently reproduced: with relative `--out`, the HX89 `--resume` state path was resolved under the snapshot working directory a second time, so the native executable rejected the state. The original failure outputs remain in `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/` (including `13_FULL_STACK_DIAGNOSTIC.stderr.log`). The derivative `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/full_stack_cycle.py` now resolves the requested output directory once to an absolute path. The native error reporting also retains command, stdout and stderr; the regression `test_cli_relative_output_executes_and_resumes_real_hx89` exercises the real HX89 executable and a saved snapshot.

**Executed tests:** 11/11 full-stack adversarial/real tests PASS (`15_RELATIVE_PATH_AND_FULL_STACK_TESTS.log`). A fresh 64-cycle whole-stack invocation ran 256 native CPU intervention trials, 64 C reversible six-channel lattice-gas executions, HX89 execution of all 64 generated Polyform results and 57 actual changes to subsequent CPU commands. Independent bytewise and causal verification PASS (`16_FULL_STACK_FIXED_64_EXECUTION.log`, `17_FULL_STACK_FIXED_64_VERIFICATION.log`). The full bounded watchdog-backed canonical runner completed **12/12 gates PASS**, with an additional 16-cycle CPU→HX89→reversible gas→HX89→CPU run and complete provenance checks (`WHOLE_MACHINE_ACCEPTANCE_1793285859996322383.json`, `21_DETACHED_SAME_TURN_ACCEPTANCE.log`). Earlier runner attempts interrupted before acceptance are preserved and are not classified PASS.

**Scientific status:** The C lattice gas is a reversible discrete software model; HX89 native machine and AVX executions are real instructions. This is NOT evidence of a controlled physically continuous MOSFET weak-inversion operator, raw quantum-noise compute path, nonbinary physical storage, physically connected K06 circuit, or a bootable non-von-Neumann computer. All 116 physical completion gates remain NOT VERIFIED. The code is a tested reproducible development and control path toward those goals; it is not their substitute.

**Run after extraction:** `python3 workplace/00_CONTROL/run_whole_machine.py --cycles 16` from the parent of `workplace`, or `cd workplace && python3 00_CONTROL/run_whole_machine.py --cycles 16`. Run `python3 -m unittest discover -v -s workplace/03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE -p test_full_stack.py` to reproduce the path/negative suite. The complete separate 64-cycle trace lives under `workplace/04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/FULL_STACK_FIXED_64_1793285661/`.
