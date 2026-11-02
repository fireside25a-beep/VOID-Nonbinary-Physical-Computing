# Verification, failures and claim hierarchy

## Claim levels

| Level | Required evidence | Project state |
|---|---|---|
| Archive integrity | original SHA-256, ZIP CRC, manifest counts | Verified in recorded restorations |
| Native machine execution | actual HX89 and CPU instruction logs, source/binary identity | Verified in saved accepted runs |
| Closed digital feedback | observed HX89 outcome changes subsequent real native CPU workload | Verified in saved traces |
| Reversible lattice mathematics | finite GAS/C model and HX89 emission, independent replay checks | Verified as a **digital model** |
| CPU physical-state perturbation | actual native stimulus/readout and cross-core timing | Acquired; thermodynamic attribution unresolved |
| Distinguishable retained analog states | physically measured 3+ states, calibrated intervals, negative controls | **Not verified** |
| Coupled analog material computation | useful transformation arises from interacting material states | **Not verified** |
| Physical K06↔CPU transduction | assembled device, safe electrical stimulus, independent analog readback | **Not verified** |
| Complete nonbinary native material machine | physical arithmetic, memory, I/O, persistence, scale and recovery | **Not verified** |

## Historically preserved failures

The source release retains the original EntropyAVX BVH bounds failure, launcher defect, concurrent BVH executable build race, stale CMake cache after relocation, interrupted/failed verification attempts, and CPU three-intensity schedule and test-harness corrections. These are historical evidence, not passing results. Later repairs have their own new tested receipts.

Failures from a run are never silently erased by later success. The canonical runner checks that every claimed pass corresponds to an actual accepted JSON receipt for that invocation.

## Physical falsification and negative controls

The real cross-core candidate applies idle, partial scalar and full AVX2 work; subsequently an identical readout runs on a different pinned CPU after 5 or 50 ms. These samples include scheduler, virtualization, cache, voltage/frequency and thermal confounders. The saved 288-sample run did **not** establish a reliable three-level physical memory effect.

Direct CPU thermal/current/charge sensor readings were unavailable in the recorded virtualized host, and no assembled physical K06 device is present. This is a recorded *scientific result*, not a reason to fill calibration ledgers with estimates.

## Acceptance not waived by a software PASS

The original 116 milestone IDs and historical columns remain unchanged. A source/build milestone may be real without qualifying as physical Gate K completion. The final release does not mark M115 achieved without actual independent physical evidence.

See raw CSVs and false/negative controlled runs in `05_EVIDENCE/20261029_REAL_CPU_MATERIAL_GATE/`.
