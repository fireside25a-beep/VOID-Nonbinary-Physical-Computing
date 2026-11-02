# VOID — physical and digital research release

This public-facing repository is a **lossless publication copy** of the verified
VOID research release. All 16,712 original release files are preserved under
this tree. Historical tests, failed runs, earlier versions, source-derived
KiCad schematics and original archive fragments are included as provenance.

Start at [release documentation](README_RELEASE_20261102.md) and
[release control](00_CONTROL/READ_FIRST_CANONICAL_RELEASE_20261102.md).

## Engineering areas

- [R08 source circuits and editable KiCad captures](01_PHYSICAL_CORE/)
- [AC/DC research solver](02_ANALOG_MATH/)
- [Native CPU, AVX and EntropyAVX experiments](03_CPU_NATIVE/)
- [HX89 source and archived native evidence](04_HX89/)
- [HX89 / K06 native integration](05_HX89_K06_BRIDGE/)
- [Fresh test receipts](07_FRESH_TEST_EVIDENCE/)
- [Preserved historical logs and watchdog runs](08_HISTORICAL_TESTS_AND_WATCHDOG/)
- [Physical-board interconnect, loading and assembly documents](09_PHYSICAL_PROTOTYPE_AND_GATEWAY/)
- [Original unmodified inputs](91_EXACT_UPLOADED_INPUTS/)

**Evidence status:** digital native software and source-derived electrical
interconnect checks have recorded passing tests; the release does not contain
physical K06 bench-acquisition measurements or fabrication-accepted Gerbers.
The four surrounding-board sheets represent verified interconnects, not
complete fabricated amplifier/regulator/ADC/DAC PCBs.

A root project license has **not** been selected by the publication helper.
Any embedded third-party licenses remain in their existing directories. Choose
and review a project-wide license before calling the repository open source.
