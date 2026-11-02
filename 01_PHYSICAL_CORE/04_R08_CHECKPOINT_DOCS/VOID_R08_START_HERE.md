# VOID R08 — current single-core hardware continuation

Authoritative worktree: `/mnt/data/VOID_PHYSICAL_GATE_K_20261029/`.

The immutable R07 sealed ZIP is included under `01_PRESERVED_INPUTS/`. The active K06 `.cir` remains the one integrated physical core; no new software computing engine, text decoder, alternative primitive stack, hypervisor or VM backend has been added.

R08 repairs two formerly unreachable nominal hardware write contacts. Their controls were fixed at 0V beneath the 2V switch threshold. They are now passive, physically realizable **AC-coupled write electrodes** (resistor + film capacitor + clamp diode) tied into the existing CHARGE_A and CHARGE_B circuit nodes. No software-generated waveform, CPU-math operation or direct on-die wiring is invented. The real interface must physically supply charge/displacement stimulus. This is a circuit-design repair, not a completed physical demonstration.

The 116 original roadmap milestones remain immutable in `MASTER_M00_M115_READBACK_UNCHANGED.md`. A new 116-row R08 crosswalk updates only milestones materially changed by this amendment. The R07 and earlier release files remain byte-preserved. Unfilled physical evidence logs remain unfilled.

Read `03_CONNECTION_AND_LAYOUT/VOID_R08_EXISTING_MACHINE_AND_PHYSICAL_IO.md`, `04_MEASUREMENT_AND_PROOF/VOID_R08_PHYSICAL_WRITE_VALIDATION.md`, `06_INTEGRITY/R08_RELEASE_AND_NEGATIVE_TEST_LOG.txt` and `VOID_R08_FULL_116_MILESTONE_CROSSWALK.tsv` for exact scope/evidence.
