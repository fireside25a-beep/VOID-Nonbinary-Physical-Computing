# VOID / HX89 Scientific Research Cache — Pre-intake Checkpoint

**Research date:** 2026-10-29. **Artifact class:** isolated scholarly knowledge and deterministic development tooling. **Not a runtime computation engine.**

**Canonical existing application baseline:** sealed `VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip` whose SHA-256 is in `06_R08_REFERENCE/R08_ORIGIN.txt`. The source archive is unmodified. Three exact text-only R08 readback files are copied into `06_R08_REFERENCE` to make source provenance easy to audit without duplicating the 62.5 MB volume.

**HX89 intake state:** latest HX89 source has NOT yet been provided in this turn. The historical descriptions of HX89/HX87 are hypotheses to examine against exact source, not declarations of a machine running nonbinary computation inside a CPU. No HX89 source file is invented or substituted.

## What this cache contains

- `01_SOURCE_CATALOG/sources_seed.tsv`: 31 individually attributed papers/books/reviews dated 1990–2026, with DOI or verified landing page, evidence depth, relevance, risks of mistaken inference and milestone references.
- `01_SOURCE_CATALOG/void_research.sqlite3`: searchable offline, read-only-by-convention SQLite index with 116 milestone IDs and 160 source-to-milestone mappings.
- `02_SCIENTIFIC_SYNTHESIS/`: technical synthesis of physical dynamics, reversible cycles, measurable physical computing, native machine integration, and nonbinary primitive identification, plus math/evidence matrix.
- `03_HX89_INTAKE/`: requested artifacts and deterministic inspection sequence, ready when the genuine latest HX89 package arrives; deliberately not a new architecture roadmap.
- `04_TOOLING/`: deterministic database rebuild, one-shot layered watchdog, opt-in Crossref bibliographic metadata refresh, offline mock API **metadata fixture only**. Nothing generates waveforms, sensor readings, state evolution or experimental performance.
- `05_AUDIT/`: executed test logs, source completeness/manifest and evidence-status records.
- `06_R08_REFERENCE/`: three byte-identical readback records extracted from sealed R08, plus original sealed archive hash and CRC receipt.

## Reading status is explicit

The source set was researched via public scholar/publisher landing pages, abstracts, university technical-report descriptions and select open accessible sections. **This package does not contain, and does not claim to have fully read, 31 copyrighted complete books/papers**. Full chapter-by-chapter analysis requires access to each complete permitted text. The source catalog records exact depth for every entry. Do not treat a book's publisher overview as a full-book review.

## Scientific distinction

VOID explores whether physical degrees of freedom can perform causal transformations, not whether a program can label a numerical representation as 'X', 'V', 'I', 'RBit', 'quantum', or 'hyperdimensional'. HX89 cyclic semantics must be examined from its source then matched, where possible, to physical changes that can be independently observed and altered. Analysis equations in this cache never constitute computed physical outputs.

## Deterministic use

```bash
python3 04_TOOLING/build_research_cache.py
python3 04_TOOLING/watchdog.py
python3 04_TOOLING/refresh_crossref.py --fixture 04_TOOLING/test_fixtures/crossref_fixture.json
# Optional manual online metadata-only refresh when executed on an internet-connected host:
python3 04_TOOLING/refresh_crossref.py --network
```

Online refresh is deliberately **not** run on a timer or in the background. It writes isolated metadata snapshots only, never modifies source citations or VOID circuitry. The development environment creating this ZIP has no external network access; the scientific browser retrieval used to prepare it was external and reviewed manually. Tool tests are in `05_AUDIT/`.

**Next exact intake:** user-supplied newest HX89 archive, any matching HX89 validation logs and known source chronology. Verify bytes, inventory, source proof, cycle mechanics and test semantics, then update the complete canonical scientific synthesis and roadmap without overwriting any historical release.
