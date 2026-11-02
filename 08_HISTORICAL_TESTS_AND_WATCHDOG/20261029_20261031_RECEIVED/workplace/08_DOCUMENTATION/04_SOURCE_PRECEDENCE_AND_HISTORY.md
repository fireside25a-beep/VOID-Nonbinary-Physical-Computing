# Source precedence, version resolution and history

There is **one authoritative active worktree**, restored under `workplace/`. The project preserves original versions and does not hide duplicated historical artifacts.

## Authoritative roles

1. `00_CONTROL/VOID_HX89_EXPANDED_MASTER_INPUT_COPY_PASTE_20261029.txt` defines original purpose, authority and 116 milestones.
2. `00_CONTROL/CANONICAL_IMPLEMENTATION_LEDGER.tsv` is the single cumulative ledger; rows M00–M115 retain original IDs, dependencies and historical fields.
3. `02_ACTIVE_R08/` contains the active R08 K01–K06 physical circuit specifications and provenance.
4. `03_NATIVE_TOOLCHAIN/HX89/` is the existing HX89 native executable source, not an invented replacement.
5. `03_NATIVE_TOOLCHAIN/CPU_VOID_BATCH_CYCLE/` is the live integrated x86/HX89 experiment controller.
6. `03_NATIVE_TOOLCHAIN/EntropyAVX/` is the derivative with real BVH/launcher repair; the original reference archive remains separate.
7. `01_SOURCES_VERIFIED/` and `90_PRESERVED_PROVENANCE/` carry all archived R01–R08 and older worktree identities, originals and proof receipts.

## Historical duplicates are not multiple active machines

Original archives, extraction snapshots, previous release files and compiled cache outputs may coexist byte-for-byte. Those are provenance that must be retained, not separate authoritative implementations. `README.md` and the active source paths determine which executable is current. `04_TESTS_AND_LOGS/` carries distinct repeated runs, with append-only run IDs instead of overwriting or treating every log as a new version.

The 301,454,742-byte original research master is reconstructible from its exact two halves `.001` and `.002`. This is transport/provenance and does not imply all 116 proposed physical functions were implemented.

## Release methodology

1. Restore all source bytes in a single directory.
2. Merge new verified derivatives into the active tree without changing original archives.
3. Execute complete test suite repeatably and independently inspect receipts.
4. Generate diagrams, documentation and manifest from executed data.
5. Freeze the complete tree, compute exact SHA-256 inventory.
6. Split transport archives into meaningful folders, each less than 200,000,000 bytes.
7. Restore the full tree into a clean location, compare every path and file hash.

No silently upgraded physical milestones; no fake analog observations; no source deletions.
