# Professional release readiness / limitations

**Source engineering readiness:** the complete tree, original provenance, source identity, active native path, runbooks, tests, negative controls and raw evidence can be packaged reproducibly. **Physical architecture readiness:** Gate K has not passed. Never call this a finished nonbinary silicon machine.

## Release checklist

- [x] One root worktree and one canonical milestone ledger M00–M115
- [x] All original uploaded source archive identities preserved
- [x] Active HX89 source + EntropyAVX derivative + CPU batch + K06 source retained
- [x] Actual machine test paths, failure logs and raw traces retained
- [x] Expanded physical-history candidate executed through HX89 feedback
- [x] Source path map and repeatable runner documented
- [x] Raw measurement charts clearly labeled as CPU timing, not analog current
- [ ] Confirm third-party license/redistribution obligations before publishing original archives
- [ ] Independent silicon analog/current readout with calibrated hardware
- [ ] Three-level physically retained memory and material operation
- [ ] Verified physical K06-to-CPU connection and full nonbinary system acceptance

## Safety

The native CPU probes impose finite CPU workloads and may change processor heat/power/frequency indirectly. Use reasonably cooled, monitored hardware. The x86 process is not permitted to write guessed MMIO addresses or claim direct transistor-gate access. If a raw hardware interface is later added, validate manufacturer-documented address maps, access permissions and safety first. The historical K06 netlists are source designs, not direct computer die wiring.

## Delivery invariant

The ten logical transport ZIPs must each be under 200 MB (decimal), must restore the same `workplace/` hierarchy, and the restoration script must reject changed module hashes, unsafe paths, duplicate files, omitted files and altered original master bytes. The complete uncompressed tree is the authoritative deliverable; ZIPs are only its transport.
