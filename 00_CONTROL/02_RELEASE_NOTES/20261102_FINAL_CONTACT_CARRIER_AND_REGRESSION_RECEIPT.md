# VOID release follow-through — material carrier and full software regression

This receipt belongs to the canonical `VOID/` tree and does not rewrite historical R06/R08, HX89, EntropyAVX, AC/DC, or CPU batch source. Original uploaded archives and earlier successful/failed logs are preserved in their own branches.

## Corrections independently checked against the real material library

`VOID_PRIMITIVE_MATERIAL_INTERFACE.lib` SHA-256: `ae7f5d7ac9e1255d77d58d779150470e433d71925f4191f46b7ecc2f83558839`.

- Eight nominal `10meg` `R_ACT_*` contact devices go from VREF to each PAD node.
- Eight **different fixed `1k`** `R_ACT_GUARD_*` resistors go from PAD to the corresponding F node. Despite the identifier `GUARD`, none creates a grounded perimeter loop.
- Six horizontal + four vertical `22k` sheet links join F nodes.
- Eight independent `220k` resistors connect F nodes to RET.
- Three other functions of the material interface, including FIELD, AXIS, and charge/mesh coupling, remain in the original source and editable full-circuit KiCad capture; the two illustrated carrier sheets are a partial, electrically exact view of 34 parts, not a replacement for the full source.

The new `verify_material_contact_carrier.py` independently compares the `.lib` declarations against the 175-device flattened K06 BOM, reports cross-source names, values and exact pin mappings, and generates two assembly CSVs. The `render_material_carrier_circuit_sheets.py` directly renders the exact 34 source parts on sharp editable SVG drawings with separate 26-contact/sheet and eight-return views. No invented guard ring was added.

## Executed acceptance evidence (November 2, 2026)

The three runners were freshly executed against the current release worktree, with full standard output and exit codes under `07_FRESH_TEST_EVIDENCE/FINAL_REVALIDATION_20261102/`:

| Executed program | Checks | Exit |
|---|---|---|
| `00_CONTROL/run_canonical_unified_acceptance.py` | 72 passed, 0 failed | 0 |
| `00_CONTROL/run_integrated_validation.py` | 36 passed, 0 failed | 0 |
| `00_CONTROL/run_physical_preflight.py` | 30 passed, 0 failed | 0 |

The unified tests rebuild and execute original binary-identity checked HX89 and the source-integrated native AC/DC, CPU batch, scalar/AVX2 and BVH controller; software ablation results are recorded separately. The physical preflight checks nine source-derived schematics, 216 declarations, 459 source pin mappings, 175 K06 flattened primitives, 2×4 source carrier map, vector-card names and the compiled ingestion rejection tests, along with reconstructed original upload fragment hashes. It is a *source/host quality gate*.

## Acceptance scope

The native circuit simulation, controller and negative tests passed in this environment. No physical measurement session, fabricated board, vendor-footprint verification, KiCad ERC/DRC, calibrated ADC/DAC round-trip or manufactured-device claim is included. The physical build and full K06 nonlinear device measurements remain conditional on actual assembled hardware and instruments. Keep nominal simulation values clearly separated from physically acquired samples.

## How to reconstruct on Mac

Use the included `reconstruct_void_parts.py` and SHA-256 manifest; all release ZIPs are self-contained parts under 200,000,000 bytes, not segments requiring `cat` or binary concatenation. Run `--verify-only`, then `--output ./EXTRACTED` on an empty directory. File hashes and ZIP CRCs are rechecked during reconstruction.

## Packaging regression caught by cold reconstruction

An initial newly created independent-ZIP package inadvertently bundled the historical `VOID_SPLIT_ARCHIVE_V1` single-archive-piece reconstructor. That older script expects a different JSON format and refused `--parts-dir`; the refusal was observed rather than hidden. Its exact source is preserved under `90_HISTORY/03_ALTERNATE_SEALED_ARCHIVE_RECONSTRUCTOR/`. The active `00_CONTROL/reconstruct_void_parts.py` has been restored to the independent multi-ZIP format used by `00_CONTROL/build_portable_release.py`. The builder now executes the **bundled** reconstructor in `--verify-only` mode on every generated package and aborts if it does not accept the generated manifests and ZIPs. The final release must additionally pass actual extraction to an empty directory with per-file checksums. Do not use the superseded package created before this correction.
