# VOID — Unified physical/digital research release

This tree retains original R06/R08 experiments, exact uploaded source archives, HX89 source and Linux x86-64 binary evidence, C11 AC/DC, both EntropyAVX lineages, native CPU batch/cache/AVX tests and historical watchdog receipts. No historical source/failed experiment has been silently removed or renamed as a success.

**Working digital controller:** `05_HX89_K06_BRIDGE/03_UNIFIED_NATIVE_CLOSED_LOOP` with native GNU Fortran/C/C++/OpenSSL and actual archived executable. Rebuild/test via `python3 00_CONTROL/run_canonical_unified_acceptance.py`. Its native R/C network is a source-selected K06 subset, not the complete nonlinear physical board.

**Physical design:** `01_PHYSICAL_CORE/08_EDITABLE_SOURCE_SCHEMATICS` contains KiCad 9 source captures; `09_PHYSICAL_PROTOTYPE_AND_GATEWAY` contains flattened physical K06 BOM, core+four subsystem build sequence, independent power/probe test instructions, and native file-ingestion security checks. No populated board or physical proof is declared from software evidence.

**Source truth and provenance:** Active nine R08 files are under `01_PHYSICAL_CORE/01_R08_ACTIVE_SPICE`; older copies and input archives are in `90_HISTORY` and `91_EXACT_UPLOADED_INPUTS`; original fail history in `08_HISTORICAL_TESTS_AND_WATCHDOG`. The legacy bridge and its 36-check suite remain for compatibility, but are not the canonical unified acceptance gate.

**Mac reconstruction:** archive part bundle contains a standalone `reconstruct_void_parts.py` and `PARTS_SHA256.tsv`. Extract parts under a new directory to reproduce identical `VOID/` tree bytes; this reconstruction is independent of running x86-64 Linux executables on Apple Silicon.

A checksum detects changes to an archived file. It is not a cryptographic signature by itself and is not physical proof. See `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/01_SYSTEM_DESIGN/QUALITY_AND_RELEASE_GATES.md` for the exact acceptance matrix.

**Added source-linked board interfaces:** `09_PHYSICAL_PROTOTYPE_AND_GATEWAY/04_VERIFIED_BOARD_INTERCONNECT` now contains four editable KiCad electrical **interconnect** sheets and four SVG/DOT pin diagrams that reproduce all 15 original source-derived connectors and 78 exact pin-to-net labels. Independent structural verification and three wiring-negative tests are included in the physical preflight acceptance. The same package includes independently checked instrument-loading calculations and official vendor references for suggested analog front-end options. These interface drawings do not claim unbuilt analog-front-end components, PCB routing, Gerbers, or bench measurements.
