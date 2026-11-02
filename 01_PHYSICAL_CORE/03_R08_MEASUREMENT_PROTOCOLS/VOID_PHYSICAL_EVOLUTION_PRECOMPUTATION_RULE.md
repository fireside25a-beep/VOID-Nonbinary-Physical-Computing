# VOID physical evolution versus deterministic preparation — binding rule

The last packaged VOID release is an immutable R01 source baseline. This R02 amendment is incorporated into the SAME active VOID hardware worktree. No competing runtime or digital substitute is introduced.

**The hardware performs:** spontaneous electrical thermal fluctuations, physically biased-junction transport, passive RC admittance dynamics, and real DC voltage summation in connected resistors. The fixed netlists describe what must be assembled; they are not evidence that an actual device was assembled.

**Allowed prior computations:** circuit component values and limits, independently derived Kirchhoff constraints, wiring/footprint checks, expected nominal external meter loading, physical test ordering, safe power-envelope estimates, and calibration factors derived from real instrument certificates. Their purpose is to check the physical experiment, not generate its output.

**Forbidden substitution:** stored or synthesized future thermal noise samples, a pseudo-random data stream as the junction, CPU-calculated 'physical' node voltages offered as measured voltages, numeric DMD predictions used in place of a wired mesh, and claims that changing output sampling creates a native analog instruction.

**Measurement principle:** repeat identical externally imposed boundary conditions in independent runs. Raw waveforms can vary even with unchanged connections; the measured distribution can be stable. Non-repeatability alone does not certify entropy, information security, useful computation or the absence of interference. Explicit source-off, instrument-termination, Johnson-reference and channel-interchange controls are mandatory.

**Hardware-only isolation test:** physically disconnect any host computer and any DAC/controller digital command lines while leaving the independently powered substrate and analog observation instruments operating. Test the observable response and independently account for rail and instrument power. 'Host CPU usage = 0%' is not a valid criterion when a host is used for capture or analysis; unplugging the host is a much stronger boundary test. Avoid an unverified 500MS/s requirement until measured bandwidth justifies it.

**Time and scale:** absence of a logic clock does not imply size-invariant latency. Physical propagation and RLC/RC time constants, lead parasitics and readout loading can change with mesh scale. Test settling time as scale changes on real, separately constructed devices before making scaling claims.

**Current gate:** Gate K requires acquired physical traces and held-out fit on different acquisitions. The other mathematical regimes remain independent and locked. DMD/TLS-DMD fits, if later used, are external analyses of measured data, not a source of physical computation or a certification of infinite-dimensional dynamics.
