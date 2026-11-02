# Release source freeze receipt — 2026-10-29

The delivery is constructed from a **separate immutable packaging copy** of the cumulative `/mnt/data/workplace` source tree, so ongoing development or release-note edits cannot corrupt checksums while ZIPs are created.

Before adding this receipt, the packaging copy contained **8,121 files and 1,196,256,299 file bytes**, and each of those 8,121 files was independently SHA-256 compared against the live source tree: **8,121 exact matches, 0 mismatches**. This receipt is packaging metadata and is the only extra file intentionally added to the frozen tree.

The authoritative machine run before freeze completed the 21/21 named native integration gates in `04_TESTS_AND_LOGS/20261029_WHOLE_MACHINE_RESTART/WHOLE_MACHINE_ACCEPTANCE_1793289015588851085.json` (8 cycles, all physical-nonbinary fields false). An earlier overlapping-build failure, its repair and negative test evidence are preserved. Keep historical originals unchanged.

The source directory will be distributed in nine logical ZIP modules under 200,000,000 bytes per module. Folder manifests are hashed from this frozen copy, not a live mutable tree; the recipient must run `RESTORE_VERIFY.py` and compare every source file before trusting the release.

**Physical-science status:** a real CPU/HX89/EntropyAVX native test suite passing does not establish sub-threshold controlled analog computing, a material K06 attachment or a physically nonbinary full CPU machine. These gates remain pending empirical evidence.
