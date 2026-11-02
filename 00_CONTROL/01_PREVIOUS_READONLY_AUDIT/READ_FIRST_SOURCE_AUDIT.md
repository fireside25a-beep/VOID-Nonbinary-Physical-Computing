# VOID / HX89 — strict source-and-evidence audit

**Audit date:** 2026-11-02  
**Mode:** READ-ONLY investigation of 8 user-uploaded ZIP archives and their nested ZIPs. Original archives and files were not renamed, extracted into an application worktree, modified, compiled, executed, or repackaged. This document is an *audit derivative*, not a new VOID release.  
**Important limit:** All ZIP member payloads were streamed through SHA-256 and CRC validation. All accessible nested ZIPs were inspected and CRC checked. The author also examined selected authoritative source, documentation, manifest and run receipts. This is **not** a claim that every script was semantically reviewed line by line, that every numerical result was independently recalculated, or that native binaries were rerun.

## 1. Inventory and integrity

| Source archive | Top-level file members | Purpose |
|---|---:|---|
| `04_R08_VERIFIED_TREE_AND_MASTER_R08.zip` | 226 | R08 physical topology, static-design checks, physical acceptance plans and preserved historical R01–R07 / DACB / BCSE input archives. |
| `06_MASTER_HX89_RESEARCH_AND_HANDOFF.zip` | 603 | Earlier master, HX89 source/research and evidence, original EntropyAVX trace, and historical handoff duplicates. |
| `07_HX89_AVX_CPU_NATIVE_EXECUTABLES.zip` | 403 | HX89 native source/binaries, EntropyAVX *derivative* with repair, native x86 CPU experiment, research cache. |
| `08_ALL_TESTS_LOGS_PLANNER_WATCHDOG.zip` | 10,947 | Cumulative planners, ledgers, execution/watchdog scripts, execution logs, failed and successful receipts, CPU material-gate experiments, release control and graphics. |
| `09_ACDC_AVX_SEPARATE_SOURCE_SNAPSHOTS.zip` | 41 | Separately preserved AC/DC solver and EntropyAVX reconstructed source trace. |
| `VOID_HX89_K06_BRIDGE_20261031_PART_01_01_RUNTIME_BINARY_ORIGINAL_K06_AND_CODE.zip` | 22 | HX89↔K06 co-simulation source, original model copies, Linux native HX89 binary, manifest, optional full-SPICE deck. |
| `VOID_HX89_K06_BRIDGE_20261031_PART_02_02_NATIVE_EXECUTIONS_AND_ANALOG_TRAJECTORIES.zip` | 2,037 | Seven modeled feedback scenarios, synthetic *model* voltage trajectories, generated HX89 polyforms and captured native stdout/stderr. |
| `VOID_HX89_K06_BRIDGE_20261031_PART_03_03_NEGATIVE_TESTS_AUDITS_AND_SUPERSEDED_DIAGNOSTIC.zip` | 2,065 | Bridge negative tests, independent readback reports, causal comparison, and explicitly invalid superseded sign-error run. |
| **Total** | **16,344** | **6,799 distinct byte payloads** identified by length and SHA-256. |

- All 16,344 top-level members could be decompressed and hashed without error. No ZIP CRC/read errors, encrypted entries or obvious ZIP path traversal were observed.
- There are 682 groups of exact duplicate file content across/within the eight archives. Their repeated payloads account for approximately **192,641,037 redundant uncompressed bytes**; do not assume removing historical duplicates is permitted.
- There are **39 embedded ZIP occurrences**, corresponding to **16 unique embedded ZIP byte streams**. Recursive inspection reached depth two, covering **812 file entries across unique embedded ZIPs**, with **no embedded CRC failures**.
- This is an audit of **the archives supplied in this chat**, not a verification that every file from the previously reported 1.2 GB / nine-folder historical research volume is present. Some sources, records and historic split volumes are referenced by paths/manifest records but are not independently present as separate top-level archives here.
- Two UI upload notices for `08_ALL_TESTS_LOGS_PLANNER_WATCHDOG.zip` resolved to one actual mounted path; it was audited once, not counted as two different archives.

The accompanying `ARCHIVE_MANIFEST.json` includes all eight whole-archive SHA-256 digests and sizes. `MEMBER_INVENTORY.csv` and `CATEGORIZED_MEMBER_INDEX.csv` index every top-level member with content hash, archive and path. `RECURSIVE_NESTED_INDEX.csv` inventories embedded ZIPs. `CONTENT_DUPLICATE_GROUPS.json` preserves exact-duplicate group membership.

## 2. Source of truth: authoritative versus preserved material

1. **VOID physical core**: use `04_R08...zip` → `workplace/01_SOURCES_VERIFIED/R08/02_PHYSICAL_CIRCUITS/` as the currently supplied, source-grounded R08 circuit specification. It has **nine active SPICE circuit/library sources**: `VOID_K01_BIASED_BREAKDOWN_WITH_MESH.cir`, `VOID_K02_DIODE_ZERO_VOLT_WITH_MESH.cir`, `VOID_K03_PASSIVE_JOHNSON_WITH_MESH.cir`, `VOID_K04_TERMINATED_RECEIVER_WITH_MESH.cir`, `VOID_K05_DC_ADMITTANCE_WITNESS.cir`, `VOID_K05_WEIGHTED_NETWORK.lib`, `VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir`, `VOID_K_MESH_V1.lib`, `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib`. Older R06 K06 sources exist within `01_PRESERVED_INPUTS/R06_SUPERSEDED_UNSEALED_HUMAN_IO/` and **must not** replace the active K06 file.
2. **HX89**: the archived `HX89_FINAL_REPOSITORY` in `06_MASTER...zip` and the `07...zip` → `workplace/03_NATIVE_TOOLCHAIN/HX89/` tree contain source, native code and tests. HX89 is implemented software/native x86-64 execution with Polyform / Q² / reversible digital gas functionality; no path here demonstrates a physical nonbinary CPU substrate.
3. **EntropyAVX**: `09...zip` → `workplace/01_SOURCES_VERIFIED/AVX/entropy_engine_source_trace/` is the source trace reconstructed from historically pasted file contents, **not** guaranteed to match an undisclosed external private original. `07...zip` → `workplace/03_NATIVE_TOOLCHAIN/EntropyAVX/` is a *later repaired derivative*, not an identical original. Both belong in provenance.
4. **AC/DC passive analog mathematical experiment**: `09...zip` → `workplace/01_SOURCES_VERIFIED/ACDC/AC_DC_Passive_AI_Proof/`; this comprises a C11 complex/nodal solver, several SPICE decks, test code and recorded math/simulation results. It is **not** the K06 netlist and its output is **not** bench measurement.
5. **CPU/AVX tests**: `07...zip` → `workplace/03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/` contains x86 CPU scalar/SIMD/cache/history experiments and HX89 control interfaces. These use real digital CPU instructions but do **not** export a K06-like analog device from on-die transistors.
6. **Planner, watchdog, run evidence**: `08...zip` provides `workplace/00_CONTROL/`, `04_TESTS_AND_LOGS/`, `05_EVIDENCE/`, `06_RELEASE_CONTROL/` and other execution/runbook areas. `CANONICAL_MASTER_PLAN.md` / `CANONICAL_IMPLEMENTATION_LEDGER.tsv` retain historical milestone IDs M00–M115. **116 milestones listed does not mean 116 physically completed milestones.**
7. **HX89↔K06 bridge**: the three `VOID_HX89_K06_BRIDGE_20261031_PART_...` archives are **parts of one newer, limited RC co-simulation research package**. They share the `VOID_HX89_K06_CAUSAL_BRIDGE_20261031/` root and assemble by extracting each ZIP to the same *new* folder. This does **not** supersede original R08 source nor replace full K06 physical validation.

## 3. Byte-level relationships proven in this audit

- **Active K06** `VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir`, 7,601 bytes, SHA-256 `ccfd7ab640ecc54fee5a2414eaca56c920f6c3dd4d1299f1e7f3b61f9c80d161`, is byte-identical in the active R08 folders, HX89 handoff copy and October 31 bridge's original/testbench source copies.
- The older preserved `R06_SUPERSEDED_UNSEALED_HUMAN_IO/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir` is **5,795 bytes with a different hash**. That is expected historical divergence, **not** evidence that the active R08 source is corrupt.
- The source hashes for `VOID_K05_WEIGHTED_NETWORK.lib`, `VOID_K_MESH_V1.lib` and `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib` match across active R08, HX89 reference copy and bridge original/testbench copies.
- **HX89 executable** SHA-256 `50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451` matches between the earlier archived `HX89_FINAL_REPOSITORY/bin/hx89` and the bridge's `03_HX89_BINARY_ONLY/hx89`. This is a Linux x86-64 executable, not a native Apple Silicon/Mac executable.
- The extracted **AC/DC** package in `09...zip` has all ten actual files byte-identical with the source contents of `AC_DC_Passive_AI_Proof(2).zip` embedded in R08 (an extra ZIP directory entry is not a file mismatch).
- All **31 files** of the extracted original **EntropyAVX source trace** in `06...zip` match the `09...zip` AVX snapshot byte-for-byte.
- Comparing the 15 correspondingly named original EntropyAVX reconstructed source files from `09...zip` with the later native derivative from `07...zip`: **10 identical, five changed**. Changed files: `build_engine.sh`, `bvh_spatial.cpp`, `engine_core.cpp`, `main.cpp` and `microkernel.py`. This is a documented repair lineage, not a source merge to perform silently.
- The bridge's own three-part `ALL_RELEASE_FILE_SHA256.csv` lists **4,123 non-manifest members**. All **4,123 actual paths, sizes, and SHA-256 digests** match. Zero missing, zero extra, zero hash mismatches. The fourth thousand includes the invalid superseded diagnostic, which is *present for provenance*, not passing evidence.

## 4. What the actual R08 source describes

The active `VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir` is a SPICE electrical specification, **not a KiCad manufacture-ready schematic**. Its nominal design includes a current-limited **24 V** supply for a nominal **7.5 V BZX55C7V5** breakdown diode; a shared RC probe mesh; a weighted five-input/two-output network; capacitors `CHARGE_A`, `CHARGE_B` (100 nF each) and `CHARGE_C` (220 nF); finite leakage/coupling/feedback resistors; a 10 mH inductor; and antiparallel nominal 1N4148 diodes with series resistance.

Its R08 change adds externally driven `WRITE_A` and `WRITE_B` input contacts using **1 MΩ bleed, 10 nF series film capacitor, 100 kΩ series limit and nominal diode clamps to the 1.8 V material rail**. The material interface contains eight nominal variable material contacts, two analog pointing axes, boundary inputs, analog X/Y/Z observation headers, two nominal piezo electrical loads and four transistor/LED optical response channels powered from a separate **3.3 V rail**.

**Critical qualification:** model parameters, physical sensor variability, component tolerances, high-voltage bias isolation, source/return architecture, instrument loading, and analog coupling are not verified by an image or a completed board. R08's `VOID_GATE_K_PHYSICAL_TRANSIENTS.tsv` and `VOID_K05_PHYSICAL_ACQUISITIONS.tsv` each contain **header only**, not captured measurements. The source itself states that the physical circuit has not been assembled or measured. The attractive diagrams supplied separately therefore must be treated as **non-authoritative** until recreated directly from this netlist and independently connectivity-checked.

## 5. Status of software tests and what they do not prove

| Branch | Evidence actually found in archive | Supported interpretation | Unsupported interpretation |
|---|---|---|---|
| R08/K01–K06 | Static component/connectivity and negative-check reports, 9-source circuit contract; history and design calculations. | The archived design has undergone named static tests. | Measured analog circuit, stable memory, source noise or full SPICE transient verified. |
| AC/DC | `test_log.txt` reports **4,099 deterministic input vectors**, both outputs, DC/AC nodal KCL and agreement with C11 numerical solver and parsed decks. | Historical mathematical/simulation test receipt. | Physical AC/DC hardware or proof of a manufactured analog computer. |
| Original EntropyAVX | Audit records native 60-frame execution, sanitizer test and a **failed original BVH 8-vertex bounds case** (expected X=7, observed X=3). Its original launcher could report shell success despite not finding the executable. | Historical original reconstructed source trace and known failures. | That the original was fully correct or was a verified source snapshot of a private third-party project. |
| EntropyAVX repaired derivative | Separate patched files; reported **3,003 BVH build/refit stress tests** and native watchdog checks. | Historical repair and tests on x86 hardware, distinguishable from original. | That AVX is an analog nonbinary substrate. |
| HX89 native | Source, assembly, executables, deterministic tests and saved Q²/lattice-gas evidence. | Actual compiled/software Polyform machine and native execution history. | Material K06 functionality occurring inside a CPU or a new physical instruction-set architecture. |
| Native CPU batch / watchdog | Earlier log receipts include **11/11**, **21/21**, **24/24**, and two later **27/27** full-stack gate passes, each for its named software/instruction checks. Original failures also preserved. | Historical real x86 instruction tests and software feedback; specific bounded gate passes. | 27/27 physical gates or general-purpose analog CPU readiness. |
| CPU material-history experiments | 288 native cross-core timing observations, two durations and randomized intensity conditions, with recorded statistical testing. | Genuine digital CPU work and timing readback experiment, as described by archived receipts. | Direct thermodynamic measurement, stable three-level analog memory or physical K06↔CPU connection. |
| October 31 HX89↔K06 bridge | 24/24 independent unit test result in report; **7 scenarios × 96 HX89 native run records = 672 captured outputs**, **8,064 RC-model voltage samples**, and controlled negative comparisons. | Bounded *software co-simulation* using a passive R/C subgraph of source R08 plus HX89 native outputs. | Full nonlinear SPICE K06 verified, built ADC/DAC link, physical analog trajectory or real HX89-driven circuit. |

### Failure and run-lineage cautions

- Eight `REPEATED_MACHINE_RESULT.json` summaries are present in the `08...zip` canonical runs. **Three** report all their native suites passed, while **five** do not (including missing/invalid receipts and partially failed attempts). A release must not cite later successful reruns as proof that earlier failed runs never occurred.
- The final later two-run canonical record reports **27/27 per run** and explicitly classifies the outcome `NATIVE_FULL_STACK_DUAL_INPUT_PASS_PHYSICAL_GATE_UNVERIFIED`.
- The separate CPU material test reports all explicitly reject nonbinary physical memory. Some **distinct run summaries contain different numeric medians/sign-test p-values**: the `PHYSICAL_GATE_RESULT_AND_REPRODUCTION.md` table reports 5 ms p≈0.8854 and 50 ms p≈0.6655, while `FINAL_PHYSICAL_GATE_EXECUTION_20261029.md` reports 5 ms p≈0.1114 and 50 ms p≈0.3123. Do not splice them into one dataset; identify the exact raw session and run/receipt behind each before publication.
- The October 31 bridge records **3 native positive decisions in 96 cycles** for the corrected `closed_loop` case. Other scenarios include zero excitation, disconnected simulated writes and forced/inverted digital decisions. Voltages in `analog_waveforms.csv` are *solver output*, not oscilloscope output.
- The bridge preserves `05_TESTS_AND_AUDITS/superseded_wrong_sign_run/INVALID_DO_NOT_CITE.txt`. Its earlier sign-error waveforms must be retained but **explicitly excluded from scientific positive evidence**.
- Its generated `EXTERNAL_BENCH_FULL_K06.cir` was **not executed by ngspice** according to `GENERATION_SCOPE.json` and the bridge claim matrix. The actual full nonlinear K06 model, with diode, transistor, inductor and material interface, remains untested by that bridge evidence.
- No text member or archive entry matched the exact term **`ACSC`** in this investigation. **AC/DC** appears as a well-defined subsystem. `ACSC` remains **unresolved terminology**, not something to invent or silently rename.

## 6. Scientific proof boundaries (non-negotiable)

**Established from archived bytes:** the supplied ZIPs are readable and internally consistent; specific original/derivative sources match or differ exactly as described; previously saved native execution receipts, circuit-design tests and model-only bridge datasets exist.

**Previously reported by saved log receipts, not freshly run here:** HX89 and CPU execution, historical unit passes, EntropyAVX repair tests, 672 captured native bridge executions, and numerical AC/DC/RC experiments. Log inclusion is not a substitute for external reproducibility.

**Not demonstrated:** a powered assembled R08/K06 board; calibrated current/voltage/temperature measurements; full nonlinear K06 SPICE transient; a physical ADC/DAC/USB/UART closed loop; controllable, retained, distinguishable nonbinary physical memory; a physically native new CPU ISA; and a general-purpose computer that computes directly in physical multilevel material rather than in software.

In particular, the diode's internal noise, an Intel RDRAND/RDSEED entropy result, HX89 Polyform's semantics, cache timing, and K06 capacitor voltages are **four different things**. Correlation or an analogy is not proof that one implements the other. Keep the physical source, software-native ISA/VM, CPU material screening, and experimental analog interface as separate scientific layers.

## 7. Proposed future open-source tree — NOT created or migrated

```text
VOID/
  00_RELEASE_CONTROL/           exact intake, release plan, SHA-256, licenses, proof gates
  01_ORIGINALS_IMMUTABLE/       unchanged supplied archives and nested historical versions
  02_PHYSICAL_R08/             current nine authoritative SPICE sources
  03_CIRCUIT_ENGINEERING/      source-derived KiCad sheets, ERC, net mappings, BOM, revision notes
  04_ANALOG_EXPERIMENTS/       AC/DC solver, RC research, independently scoped results
  05_HX89_REFERENCE/           versioned HX89 provenance and permitted bridge interface
  06_NATIVE_CPU_RESEARCH/      original and repaired AVX branches, CPU tests, cache, watchdog
  07_HX89_K06_BRIDGE/          original K06 copies, controlled model, generated full SPICE deck
  08_TEST_EVIDENCE/           passing and failing histories, invalid superseded clearly quarantined
  09_PHYSICAL_BENCH/           unfilled real ADC/scope records, safety, calibration, acceptance gates
  10_DOCUMENTATION/           architecture, limitations, glossary, reproduction, electrical diagrams
  90_HISTORICAL_ARCHIVE/       preserved R01–R07, DACB/BCSE and other independent research
```

This is **a classification proposal, not a claim that missing files have been reconstructed**. The correct future workflow is: source authority ledger → source-level topology diff → explicit low-cost board partition → independent SPICE/ERC → separately assembled and measured prototype → HX89-interface falsification experiments → platform-specific builds → reproducible checksums, frozen source archive and professionally split deliverable. For a MacBook with Apple Silicon, rebuilding or cross-compiling HX89 is a separate technical task; unpacking Python scripts alone does not make Linux x86-64 ELF binaries run natively on macOS.

### Strict continuation policy

1. **Read-only checkpoint after this audit.** Do not migrate or rename active source, overwrite historical archives, delete duplicates, execute prebuilt binaries, fabricate schematics or insert measurements without explicit next authorization.
2. Maintain a per-artifact ledger: `RECEIVED / EXACT_DUPLICATE / ORIGINAL / DERIVATIVE / HISTORICAL_SUPERSEDED / INVALID / REPORTED_TEST / INDEPENDENTLY_REPLAYED / BENCH_MEASURED`.
3. Name authoritative versions by exact SHA-256 rather than optimistic `VERIFIED`/`LATEST` filenames.
4. No source assumptions: if an included testbench or claim references an absent part of the historical 1.2 GB workspace, mark **NOT PRESENT IN THESE UPLOADS**.
5. Preserve all previous failed, negative, incomplete and invalid outputs under clearly separated headings. Never count saved artifacts as independent experiments without matching run IDs.
6. Do not claim a final open-source release is complete until restoration, license checks, source builds, exact manifests, real schematics and evidence-class acceptance have passed on a fresh tree.

## 8. Reproducible audit data files

- `ARCHIVE_MANIFEST.json`: exact 8 whole-archive sizes, SHA-256 digests, member counts, per-extension counts and errors.
- `MEMBER_INVENTORY.csv`: all 16,344 archive member records with name, SHA-256, CRC, bytes, file extension and nested indicator.
- `CATEGORIZED_MEMBER_INDEX.csv`: same index plus **conservative path-derived family/subsystem/lineage labels**. These labels are for sorting and **are not independent test outcomes**.
- `CATEGORY_COUNTS.json`: classification totals.
- `CONTENT_DUPLICATE_GROUPS.json`: exact duplicated content; never delete historical copies on this basis alone.
- `NESTED_ZIP_INDEX.csv`, `RECURSIVE_NESTED_INDEX.csv`: nested archive fingerprints, CRC status and internal entry counts.
- `ISSUES.json`, `NESTED_ZIP_ERRORS.json`, `RECURSIVE_NESTED_WARNINGS.json`: audit warning/error registers (empty for the specific checked conditions).
- `audit_inventory.py`, `categorize_inventory.py`, `nested_index.py`, `recursive_nested.py`: read-only regeneration scripts, included as audit code, **not integrated into VOID**.

**Final scientific status of this checkpoint:** archive and cross-source audit complete at byte/structure level; historical experiment statuses classified, with no new runtime or physical acceptance claimed. The original research files remain untouched.
