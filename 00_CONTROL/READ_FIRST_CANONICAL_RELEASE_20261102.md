# VOID / HX89: canonical open-source scientific worktree (2026-11-02)

## What the current release DOES establish

The release is **one cumulative research volume** with eight preserved uploaded archives (where oversized originals are losslessly fragmented and independently SHA-256 reconstructable), R06/R08 original source and history, all nine R08 source circuit files, the substantial original HX89 native executor and tests, preserved standalone AC/DC reference and repaired/original EntropyAVX lineages, native CPU batch/cache and CPU instruction tests, current unified source-and-executable integration, trace files, errors and negative tests.

**Fresh code execution acceptance:** `python3 00_CONTROL/run_canonical_unified_acceptance.py` => **72/72 PASS** for the compiled native integrated path (six digital modes, seven scenarios per mode). `python3 00_CONTROL/run_integrated_validation.py` => **36/36 PASS** for the preserved earlier integration suite. `python3 00_CONTROL/run_physical_preflight.py` => **30/30 PASS** for editable source captures, independent KiCad AST cross-check, K06 hierarchy, 15 source-mapped connectors plus four new KiCad electrical interconnect sheets and corrupted-net negative tests, source-derived local loading analyses, native measurement-ingestion compile and fail-closed negative tests, and the exact eight original archive identities. Machine-readable test evidence is under `07_FRESH_TEST_EVIDENCE/` and source tools under `00_CONTROL/` and `06_ENGINEERING_VALIDATORS/`.

**Native digital loop:** the compiled GNU/Fortran + C/C++ source uses original HX89 executable and SHA256 integrity checking, native AC/DC C11 calculations, repaired EntropyAVX BVH, original CPU batch work, scalar/feature-gated AVX2 CPU execution, feedback digests and a K06-specific numerical RC circuit model. Causal ablations establish that selected source computations influence subsequent software decisions. Hardware instruction telemetry and clock counters are not used as reproducible seeds in comparisons.

**Physical hardware engineering evidence:** nine generated editable `.kicad_sch` files capture 216 source SPICE cards and 459 device-pin-net assignments, cross-checked by an independent S-expression graph verifier against the original `.cir`/`.lib` text. K06 hierarchy expands to exactly 175 primitive device cards on 74 distinct nets; separate build-contract source produces 15 proposed connector groups with 78 numbered net-backed pins. The package includes a buildable low-cost staged experiment guide, original component provenance, contact and instrument-load policy, exact material 2×4 pinout and protection/rails ownership. Neither SVG images nor KiCad source capture are silently relabeled as verified finished PCB production schematics.

## What must be measured during the physical build

All historical acquired physical TSVs are preserved as they were: empty headers are not filled with artificial readings. Fabricated physical state, oscilloscope waveform evidence, custom EEPROM/CPU fabric control, actual closed loop ADC/DAC actuation, KiCad ERC/DRC/Gerber sign-off and certifications are NOT inferred from native software acceptance. `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/native_bench_ingestion/void_bench_ingest.c` is a genuine C11/OpenSSL program that refuses missing, malformed, unsafe-voltage or unauthenticated-schema measurement inputs and writes a SHA256 file-identity receipt only for an externally acquired CSV; physical instrument authenticity also requires the operator's calibration and source log. For low-cost physical assembly read `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/03_BUILD_REFERENCE/REAL_K06_LOW_COST_ASSEMBLY_GUIDE.md`.

The compiled numerical model is source-derived but computes a bounded K06 R/C subgraph, NOT every nonlinear BJT/Zener behavior of the full circuit. Do not infer subnanosecond physical clock-cycle control or general purpose CPU instructions from the observed software feedback loop. Physical source-contact interventions and complete SPICE/bias-corner verification remain distinct acceptance gates.

## Open-source release navigation

- `00_CONTROL`: authoritative reproducible validators, completeness evidence, and archive reassembler
- `01_PHYSICAL_CORE`: source-authoritative R06/R08 circuits, KiCad editable captures, actual source-rendered sheets, and historical connection measurements
- `02_ANALOG_MATH`: independent AC/DC original sources linked to native integration by C ABI
- `03_CPU_NATIVE`: original CPU batch/AVX/cache studies and preserved original/repaired EntropyAVX versions
- `04_HX89`: native HX89 source/executables and mathematical/semantic evidence
- `05_HX89_K06_BRIDGE`: historical archived receipts, current integrated Fortran/C/C++ controller, source-based native path
- `06_ENGINEERING_VALIDATORS`: KiCad source extraction, independent pin-net validation, K06 physical hierarchy and proposed assembly contract checks
- `07_FRESH_TEST_EVIDENCE`: logs/results of native real source tests and physical preflight (software source audit, NOT fake physical data)
- `08_HISTORICAL_TESTS_AND_WATCHDOG`: archived passes, failures, milestones and watchdog output
- `09_PHYSICAL_PROTOTYPE_AND_GATEWAY`: power/probe/stimulus/material carrier construction, pinouts, receipts and measured-data ingestion
- `90_HISTORY`: earlier and pre-integration states
- `91_EXACT_UPLOADED_INPUTS`: SHA-256-reconstructable original upload archive material

`00_CONTROL/02_RELEASE_NOTES/HISTORICAL_ZERO_LENGTH_LOGS_INDEX.csv` records intentionally preserved zero-length historical test/log/lock artifacts. It does not cover any empty implementation source (none observed in current supported source-extension scan), and it does not imply those historical runs passed.

## Reconstruct on a MacBook

For the GitHub-friendly 64 MB split-archive edition, use the **reconstruction kit shipped beside the four `VOID_DELIVERY_PART_*` files**. This kit intentionally contains the matching single-archive reassembler; the separate `00_CONTROL/reconstruct_void_parts.py` inside the unpacked release is for a second independent-ZIP packaging format and must not be mixed with the 64 MB edition. Copy `RELEASE_PARTS_MANIFEST.json`, the kit-provided `reconstruct_void_parts.py`, and every `PART_nn/` directory into one Mac directory and run:

```sh
python3 reconstruct_void_parts.py RELEASE_PARTS_MANIFEST.json --output "$HOME/Desktop/VOID_RECONSTRUCTED"
```

The script validates every part size/SHA256, the complete assembled archive identity, every internal release file's size/SHA256 and ZIP CRC, and refuses existing destination paths or unsafe extraction entries. This operation needs only Python3 and does not assume a working Intel Linux HX89 executable on Apple Silicon. To publish to GitHub, upload the **reconstructed `VOID/` source/evidence tree in properly sized commit batches** or preserve the numbered parts as downloadable GitHub release assets; GitHub ordinary Git repository file-size limitations should be checked before pushing large binary archives. Do not delete original failing historical tests.

## Additional source-derived 2×4 carrier verification

`06_ENGINEERING_VALIDATORS/verify_material_contact_carrier.py` and `render_material_carrier_circuit_sheets.py` (if present in the sealed input) independently validate the eight 10 MΩ replaceable contact elements, the separate eight fixed 1 kΩ series resistors and the 22 kΩ sheet topology. `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/03_BUILD_REFERENCE/MATERIAL_CARRIER_PHYSICAL_WIRING_AND_SOURCE_VALIDATION.md` documents the rendered contact sheets and actual material nodes. The latest physical preflight uses 30 source/host checks (not bench data).

## Four verified hardware interconnect sheets and HIL transaction contract

`09_PHYSICAL_PROTOTYPE_AND_GATEWAY/04_VERIFIED_BOARD_INTERCONNECT` contains four native KiCad 9 pin-network schematics, four matching DOT/SVG diagrams, independent source-net verification with three corruption tests and a netlist-derived probe-load/current-limit budget. `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/01_SYSTEM_DESIGN/SEVEN_LAYER_RELEASE_EVIDENCE_REGISTER.md` records precisely which hardware and software layers are real, source-verified or require physical measurement. `PHYSICAL_HIL_EPOCH_AND_FAULT_CONTRACT.md` identifies real output-inhibit and timestamped-measurement acceptance conditions; no fictitious hardware driver or fabricated instrument source is included.
