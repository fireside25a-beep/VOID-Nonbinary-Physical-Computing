# VOID K05 R04 — physical resistor assemblies and unpowered inspection

This replaces only the ideal-only fractional resistor cards in the **existing** K05 witness. The original R03 circuit and its SHA-256 remain available inside the unchanged sealed R03 ZIP under `01_PRESERVED_INPUTS/`. No separate computation branch has been created. The other K01–K04 netlists and shared mesh are unchanged.

## Directly wired, nominal passive assemblies

| R03 predecessor | Active R04 physical branch | Nominal equivalent | Connections |
|---|---|---|---|
| R03 1333.333... Ω | R03A 2000 Ω parallel with R03B 4000 Ω | 4000/3 Ω | xp3 ↔ y0 |
| R11 3333.333... Ω | R11A 5000 Ω parallel with R11B 10000 Ω | 10000/3 Ω | xm1 ↔ y1 |
| R12 1666.666... Ω | R12A 2500 Ω parallel with R12B 5000 Ω | 5000/3 Ω | xp2 ↔ y1 |
| Rg1 1428.571... Ω | RG1A 2000 Ω parallel with RG1B 5000 Ω | 10000/7 Ω | y1 ↔ return |

Each branch requires **actual measured physical resistance**, selected resistor networks or suitably composed conventional series/parallel resistor assemblies. These nominal values are NOT specifications of exact zero-tolerance commercial parts. The same physical source node xp3 feeds both output branches.

Five active externally supplied input source nodes remain: xp1 (+0.8 V), xm1 (−0.8 V), xp2 (−0.4 V), xm2 (+0.4 V), xp3 (+0.2 V). The older Vxm3 source at −0.2 V supplied an orphaned node, was not part of either output, and is removed from the authoritative K05 bill/diagram rather than fabricated as a sixth rail.

**Readout:** `R_METER_Y0/Y1` are the physical 10-MΩ input resistance of the two independently calibrated diagnostic instruments in the electrical netlist. They must **not** be duplicated on the assembled fixture if the meters already impose those loads. If real meter impedances differ, recompute the reference from measured values and keep raw readings unchanged.

## Continuity and actual assembly records

With physical power absent, identify input and output pins; measure component branches and both output-to-return paths while recognizing that parallel paths affect in-circuit ohmmeter readings. Record independently verified physical component resistance, instrument model/input resistance, connector continuity and actual source polarities. No supplied file substitutes a meter observation. Maintain calibrated separate supplies for both positive and negative input rails, protect test leads and ensure common reference wiring as specified by the fixture.

Record measurements only in existing `VOID_K05_AS_BUILT_COMPONENTS.tsv` and `VOID_K05_PHYSICAL_ACQUISITIONS.tsv` with original instrument file hashes. The data TSVs are intentionally header-only until bench observations exist.

### Source integrity and scope

No host-side evaluation loop or unknown MMIO address is introduced. The DC network performs the physical weighted sum when assembled and energized. Static Kirchhoff checks establish a reference for debugging the real circuit, not that any physical hardware ran in this environment. K01–K04 continue with the same source-to-mesh connectivity and independent noise controls.
