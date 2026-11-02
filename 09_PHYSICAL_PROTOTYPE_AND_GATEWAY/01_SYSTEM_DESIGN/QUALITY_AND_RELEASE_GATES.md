# Release quality matrix: no hidden PASS states

| Gate | Real executable/check | Acceptance target |
|---|---|---|
| Original archive identities | 00_CONTROL/01_PREVIOUS_READONLY_AUDIT / original ZIP SHA-256 manifests | Distinct originals preserved byte-for-byte |
| Active R08 source | 06_ENGINEERING_VALIDATORS/validate_r08_source.py | Six source circuit decks, all instance/model references valid |
| Exact editable capture | generate_editable_spice_schematics.py | Nine files, 216 elements, 459 source pin mappings, structural S-expression validation |
| K06 actual hierarchy | expand_r08_k06_hardware.py | 175 flattened primitive cards, unique actual SPICE net map |
| Native integration | 00_CONTROL/run_canonical_unified_acceptance.py | Fresh rebuild, seven 96-epoch scenarios in six modes, native command/oracle, causal ablations |
| Historical native regression | 00_CONTROL/run_integrated_validation.py | Original 36 checks (superseded release gate), preserved logs and failures |
| Native AC/DC | analog_core.c `--test` | All 4,099 deterministic reference vectors and independent network/AC response tests |
| Original CPU batch | cpu_batch.c | Real hardware-gated SIMD/cache loops, bounds-negative tests, no synthetic results |
| Repaired EntropyAVX | BVH 3,003 cases and ownership | No original BVH defect; historical failing source remains as evidence |
| Hardware ingestion | native_bench_ingestion/void_bench_ingest.c | Real file, immutable receipt, rigorous rejection of malformed/incomplete data |
| Physical DUT and full K06 | actual populated circuit, measured waveforms and full nonlinear SPICE simulator | Real proof remains to be furnished by bench, not replaced by digital tests |
| Reconstructable release | 00_CONTROL/reconstruct_void_parts.py | Every extracted release file SHA-256 matches manifest, all ZIP member names safe, no duplicated paths |

The KiCad source captures are **not** substitutes for fully routed KiCad PCB layouts. Vendor datasheet review is essential for component selection, op-amp common-mode range and supply headroom, DMM input impedance and ADC voltage limits. Never label a byte hash as a physical device attestation.

## Added verified four-module interconnect gate (2026-11-02)

`python3 06_ENGINEERING_VALIDATORS/build_verified_board_interconnect.py` generates **four physically scoped KiCad electrical interface sheets** covering all 15 K06 board connectors and 78 pin-to-net connections. `python3 06_ENGINEERING_VALIDATORS/verify_board_interconnect_independent.py` verifies the actual KiCad S-expression electrical connectivity by independent parsing and rejects three corruption mutations. `python3 06_ENGINEERING_VALIDATORS/build_probe_loading_budget.py` validates 32 named source cards and nine actual local shunt scenarios. All three now participate directly in `00_CONTROL/run_physical_preflight.py`, so no optional engineering artifact can silently drift from the canonical source. Read `04_VERIFIED_BOARD_INTERCONNECT/README_BUILD_AND_ELECTRICAL_SCOPE.md` before assembling the four supporting modules.
