# Retrieval-loop correction and deterministic source checkpoint

**Issue corrected:** repeated invocations of retrieval on HX89 in a changing conversation were treated as fresh attempts without a resolved input artifact; no successful source readback or durable status record was produced.

**Current approach:**

1. Every requested artifact is either **located and inspected** or marked **NOT SUPPLIED / NOT LOCATED**; never promote an unfinished retrieval to evidence. Latest HX89 presently NOT SUPPLIED.
2. Source retrieval and citations are individually enumerated in `sources_seed.tsv`; the local database can be reconstructed without internet.
3. Three-level one-shot checker: immutable release provenance, research data integrity, and claim containment / runtime isolation. The checker terminates after bounded operations and does not invoke itself, create watchers, fetch the internet or compute substrate outputs.
4. When a newest HX89 source arrives, capture its exact file bytes first, calculate SHA-256, ZIP CRC, member count, file tree, reported version; only then identify what is already implemented. No automatic source family substitution.
5. Internet updates are explicit one-off bibliographic metadata refreshes through an allowlisted Crossref URL; they are recorded as content-hashed snapshots, never written into the physical compute path. Search and scientific synthesis remain separate from material operations.
6. Failed / interrupted ingestion must leave the original R08 and the latest HX89 upload unchanged. Resume from the last verified file-level checkpoint rather than resetting the project.

This procedure is a development tool and source-audit discipline, not a claim of independent ongoing AI cognition, access to arbitrary processor on-die devices or a self-running background agent.
