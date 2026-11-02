# Unified BCSE master roadmap M00-M115 — physical hardware investigation

Status: readback + proposed hardware-design extension. No new physical data, no completed hardware calculator, no hidden digital implementation.

## Preserved M00-M85

# Master milestones M00–M65: source-backed continuation, not a reset

**Acceptance invariant:** all tasks have `source_ref`, `inputs`, `outputs`, `dependencies`, `status`, `test_plan`, `evidence_ref` and `refusal_when_missing` in the milestone matrix. A historical log is evidence of a past run, never a fresh full integration PASS. `PROPOSED` is an honest status. Every block is independently falsifiable.

## M00–M12: retained DACB mathematical foundation (readback; never redo automatically)
- **M00 — Immutable provenance:** count, hash, CRC and copyright/license history of original DACB, hardened, experimental forks. **Gate:** byte-identical original archives, no untracked mutation; no destructive cleanup.
- **M01 — Canonical 32-bit affine map:** exact modulo 2³² semantics, Hull–Dobell full period, inverse multiplier. **Gate:** algebra + reduced exhaustive + independent native oracle.
- **M02 — Full-width time navigation:** 64-bit steps, zero/maximum boundaries, fast jump and reverse, cycle distance. **Gate:** inverse/composition identities on matched input state and seed.
- **M03 — Nonlinear conjugation:** bijection inverse, full-period via conjugation, explicit restrictions on coefficients. **Gate:** algebraic proof and reduced exhaustive; no crypto claim.
- **M04 — Other recurrence families:** separate quadratic, PCG and inversive behavior and parameter restrictions. **Gate:** documented limits; no inherited full-period assertion.
- **M05 — Spectral mathematics:** exact certified 2D dual vector; 3D+ remains proof target. **Gate:** independent lattice oracle, known weak controls.
- **M06 — State-recovery attacker:** full-state 3-output LCG attack plus bounded nonlinear recovery. **Gate:** recover planted cases and report precisely known parameters and attack budget.
- **M07 — ISA entropy intake:** authentic RDSEED/RDRAND/getrandom source-specific availability; no silent substitution. **Gate:** provenance/refusals; raw analog access not claimed.
- **M08 — Statistical logger:** real native state stream 2D/3D/4D, NN metrics, parity and histograms. **Gate:** independent coordinate oracle and seeded replay.
- **M09 — Stream partition and receipts:** nonoverlap/stride where mathematically warranted, SHA-256 state/event commitments. **Gate:** exact replay and tamper refusal.
- **M10 — Numerical cross-platform oracles:** native GCC/Clang historical, Nim/Fortran production research; no new production C/Python. **Gate:** compare equal semantics not matching printed scores alone.
- **M11 — Deterministic lab views:** viewer reads authoritative streams only. **Gate:** screen controls materially affect real upstream sources, screenshot/browser verification.
- **M12 — Baseline scientific release:** source-inclusive archive with full build/audit evidence. **Gate:** reconstruct exact final archive and verify every member.

## M13–M30: retained BCSE system-science track
- **M13 — One event ABI:** frozen typed protocol, unit/clock/provenance semantics, binary test vectors. **Gate:** cross-language serialize/parse byte identity and version rejection.
- **M14 — Real-time native I/O:** ALSA and Tauri/CPAL integration with allocation-free callback and safe halt. **Gate:** real capture/playback, XRUN tests, hardware-dependent results explicit.
- **M15 — Acoustic self-identification:** bounded excitation, measured impulse response and held-out predictions. **Gate:** actual microphone/speaker, independent calibration and zero/predictor baselines.
- **M16 — Passive/dynamical physical worlds:** AC/DC network predictions, wave digital/port-Hamiltonian model where applicable. **Gate:** analytic references and energy/passivity; physical proof separate.
- **M17 — Network cybernetics:** sparse Kuramoto/Chua/cellular coupling and deterministic interventions. **Gate:** independent integrator and synchronization controls.
- **M18 — Adaptive control/memory:** Ashby-style bounded regulation and reservoir-like temporal response. **Gate:** held-out prediction and controlled ablations.
- **M19 — Scientific offline UI:** scope, phase portrait, 2D/3D/4D views, connected graphs and status. **Gate:** real browser interaction, source-bound data.
- **M20 — Source/event recording:** causal journal, source timestamps, receipt chains, privacy controls. **Gate:** bit-exact software replay of actual recorded input and tamper refusal.
- **M21 — Cybernetic comparison:** exact same recorded stimulus into each software/physical comparator, equal compute budget. **Gate:** error/latency/energy held-out comparison.
- **M22 — Threat/claim ledger:** prespecify conjectures, adversary, conditioning and units. **Gate:** failed and negative outcomes published.
- **M23 — Dispersal logger expansion:** non-overlap statistics, streaming sample ingestion, uncertainty estimates. **Gate:** independent oracle, no "dispersion proves entropy" shortcut.
- **M24 — Higher spectral and nonlinear geometry:** exact lattice 3D/4D where defined; nonlinear Fourier/discrepancy separately. **Gate:** known adversarial counterexamples.
- **M25 — Entropy source characterization:** actual physical source metadata, bandwidth, health/failure; min-entropy bounds only supported models. **Gate:** calibrated raw observations and no substitute.
- **M26 — Acoustic adversary:** known-state, room-replay, injection, silence, clipping, side information. **Gate:** controlled failures reported not hidden.
- **M27 — Cryptographic isolation:** physical entropy research never auto-generates real keys; vetted construction separate. **Gate:** established vectors, compromise recovery model, review.
- **M28 — Equal-scope energy and speed:** end-to-end joules/answer and latency at matched precision, overhead accounted. **Gate:** measurement uncertainty and cold/warm evidence.
- **M29 — High-dimensional view:** 4D projector and meaningful 8D reduction, no false dimensionality/ergodicity claim. **Gate:** check displayed points against raw source.
- **M30 — Replication/publication:** adversarial reproducibility and separate theorem/measurement/speculation. **Gate:** independent cold build and physical repeat where warranted.

## M31–M45: previously proposed physical-computation / polyform expansion, now made concrete
- **M31 — Physical-device capability census:** identify reachable analog sensors/outputs, units, voltage limits, clocks, converters and permissions. **Gate:** actual enumeration/circuit inspection; no invented device.
- **M32 — Hardware-boundary and ISA test:** distinguish conditioned RDSEED words, ordinary CPU arithmetic and controllable analog state. **Gate:** direct instruction transcripts and negative capability controls.
- **M33 — Polyform algebra types:** formal finite semantics for typed operator, port, state, branch and composition; define rejection. **Gate:** independent referential interpreter and invariants.
- **M34 — Roman-inspired mixed-radix/ternary experiment:** evaluate useful digit hierarchies, arithmetic carry and addressing; not glyph magic. **Gate:** round-trip uniqueness, exhaustive small cases and fair binary baseline.
- **M35 — SNN/QEC extraction map:** isolate historical `PrimitiveQ` five-qubit syndrome and recovery from unrelated layers, check branch access before extraction. **Gate:** source hashes, tests and no unrelated implementation.
- **M36 — Genuine quantum/multilevel distinction:** classical d-state vs physically coherent d-level qudit, properties and measurement needs. **Gate:** distinct evidence taxonomy and fidelity requirements.
- **M37 — Physical passive arithmetic:** energize an actual network, measure two outputs for controlled inputs and AC phasors. **Gate:** independent voltmeter/DAQ truth and converter-cost budget.
- **M38 — Thermal fluctuation instrumentation:** Johnson/Nyquist tests and source-amplifier characterization. **Gate:** temperature, resistance, bandwidth response and controls.
- **M39 — Physically realized operator semantics:** map a measurable electrical transaction to a composable operation with error. **Gate:** repeats, calibration and causal port manipulation.
- **M40 — Nested tableau specification:** formal bounded hierarchy of state/frontier/constraint/certificate; no copying HX87 implementation. **Gate:** finite interpreter, canonicalization and decidable structural equivalence for supported fragment.
- **M41 — Precomputed deterministic kernels:** certified affine powers, branch transition lookup within bound, syndrome tables, measurement schedules. **Gate:** every table compared to independent direct semantics; no physical-result cache presented as physical compute.
- **M42 — Multiple substrate comparator:** CPU digital, ISA digital words, physically built device, opt-in SNN software reference. **Gate:** source category never conflated, identical tasks/precision.
- **M43 — Performance and energy instrumentation:** wall/cycle/energy/memory and device calibration uncertainty at matched workload. **Gate:** independent meters where necessary; total device costs.
- **M44 — Independent adversarial audit:** mismatched components, unplugged device, tampered journal, altered tableau, code/syndrome failures. **Gate:** every false claim has a deliberately failing control.
- **M45 — Phase-1 physical-science release:** source+instrument traces+certificates+limitations. **Gate:** release only proven sub-capabilities; unknown stays unknown.

## M46–M65: NEW physically grounded, multi-frontier and thermodynamic research track
- **M46 — HX87/HX89 history verification:** recover authentic read-only Q²/Polyform/multi-head source, disambiguate logical frontier vs physical parallelism, list exclusions. **Gate:** hash/CRC/source location and exact function inventory; no game engine imported.
- **M47 — New physical-operand ontology:** define physical carrier (voltage/charge/phase/conductance/thermal covariance), controllability, observability, uncertainty and valid ranges. **Gate:** reference equations plus actual calibrated sensor evidence before physical status.
- **M48 — Q²-inspired but NEW frontier calculus:** explicit split/merge/collapse semantics, causality and finite budgets, no borrowed instruction encoding. **Gate:** exhaustive finite-frontier confluence/termination/replay or explicit counterexample.
- **M49 — Hierarchical tableau composition:** tableau of typed physical ports, possible state sets, operator dependencies, observation obligations. **Gate:** type preservation, compositional determinism where promised, complexity and memory bounds.
- **M50 — Mathematical scale/embedding audit:** finite surreal fragments, generalized Hahn series or transseries only with defined embedding/operations. **Gate:** theorem statements with proved fragment, no 'entire surreal universe' implementation claim.
- **M51 — Real AC/DC nonlinear element search:** identify accessible tunable nonlinear electrical element beyond passive linear resistor/capacitor networks. **Gate:** measured I–V/phase curve and load/temperature hysteresis, no assumed device.
- **M52 — Fluctuation-computing candidate:** configurable physical covariance/energy landscape with at least two coupled controllable degrees of freedom. **Gate:** measured distribution changes causally with programmed coupling, independent raw data.
- **M53 — Stochastic physical operator:** define arithmetic/inference task computed by measured fluctuation/relaxation, not RNG-then-CPU postprocessing. **Gate:** physical I/O solves preregistered task against instrument controls and unknown data.
- **M54 — Physical state graph and frontiers:** map multiple measured devices/nodes to independent state/observation frontiers with explicit link dynamics. **Gate:** real cross-correlation and intervention proves coupled physical effects rather than software branch multiplication.
- **M55 — Physical multi-level operator:** create and characterize 3+ reliably distinguishable classical device states only when hardware permits. **Gate:** confusion matrix, read/write margins, retention, speed, drift, energy. Not a quantum claim.
- **M56 — Quantum-code generalization research:** only after authentic five-qubit test oracle is recovered, develop generalized d-level algebra and independent stabilizer checks; NOT call software a qudit. **Gate:** generalized commutation identities, exhaustive small-d syndromes and mutation tests.
- **M57 — Noise-assisted prediction/controller:** measure whether physical noise improves held-out target or escape time without increasing error. **Gate:** zero-noise, shuffled-noise, conditioned digital, and blind-held-out controls.
- **M58 — Reversible/dissipative physical accounting:** distinguish finite logical inverse, physical path replay and entropy production; measure losses/cycles under safe protocols. **Gate:** energy budget and correct applicability of fluctuation relations.
- **M59 — Novel native operation selection:** require demonstrated advantage in at least one real task; a symbol or ROM table is not an operation. **Gate:** primitive spec, physical witness, equal-scope CPU baseline.
- **M60 — One hybrid cybernetic closed loop:** real sensor -> measured physical operation -> supervised native controller -> bounded actuator -> next measured event. **Gate:** causal ablation and device-loss refusal, complete calibrated timestamps.
- **M61 — Full three flagship experiments with physical component:** room identification, distributed worlds, reproducible computation comparison tied to one provenance protocol. **Gate:** three independent dataset/task receipts and uncertainty intervals.
- **M62 — Robust failure/recovery tests:** thermal drift, clipping, weak signal, feedthrough, disconnected port, device reset, xrun, source failure, sample-clock skew. **Gate:** physical outputs never substituted by analytic reference.
- **M63 — Optimization without semantic drift:** cache-aware precomputations, sparse graph, event batching outside RT, optional ISA acceleration when genuine benefit. **Gate:** mathematical output invariance, stable real-time deadlines, watts/answer comparison.
- **M64 — External scientific replication:** source, circuits/BOM/schematic, calibration/raw data, blinding/negative results, verification scripts and licensing. **Gate:** independent operator reproduces relevant physical task; falsification records retained.
- **M65 — Conditional final system release:** only evidence-backed operations documented; speculative paths isolated and unclaimed. **Gate:** all accepted mandatory gates PASS, missing devices NOT_RUN, byte-exact archive + manifest, no unhooked routines or placeholders.

## Critical-path dependency graph
Preserve M00–M12 -> reconcile M13/M14/M20 -> produce measured event provenance. In parallel: M46->M48->M49 and M35->M56 are **research branches**, not runtime dependencies of M37. Physically demonstrable path: M31->M37->M43 and M31->M38->M51->M52->M53->M59. Integrate only after individual gates: M15/M17/M18 plus M54/M57 -> M60 -> M61 -> M62/M63 -> M64 -> M65. No hypothetical high-dimensional/state-count claim can bypass device evidence.

## Completion policy
A milestone can be `HISTORICALLY_TESTED` only if a specific earlier log exists and source identity is known. New `PASS` requires a fresh exact-input/evidence trail; `BLOCKED_NO_DEVICE` is an honest result, not a simulated success. Do not predeclare that 90% is complete or that physical speedup is exponential. Claim only observed scaling within tested resources.

## M66–M85: NEW Koopman observable, physical holonomy, and audited execution track (2026-10-29)
All milestones below are `PROPOSED` unless a specific new test receipt is attached. They ADD TO, and do not erase or complete, M00–M65.

- **M66 — Operator-theory applicability dossier:** distinguish deterministic Koopman composition, Markov stochastic semigroup, generator domain, nonautonomous forced systems and non-invertible dynamics. **Gate:** formal definitions with assumptions and at least two concrete counterexamples to overgeneralized claims.
- **M67 — Unit-typed physical observable registry:** physical channel, calibration, sampling, uncertainty, state domain, observable function and provenance for voltage/current/charge/power/phase/temperature/impedance/cross-node covariance. **Gate:** dimensionally valid registry, NaN/overflow/missing sensor rejection, no invented analog observation.
- **M68 — Stochastic Koopman generator oracle:** derive drift and diffusion using Itô's formula; handle deterministic versus stochastic expectation separately; physical noise cannot silently become additive post-operator output. **Gate:** analytically solvable Ornstein–Uhlenbeck and linear RLC reference identities with independent derivation and numerical regression only as a software theory test.
- **M69 — Finite exact Koopman oracle:** construct controlled small linear and nonlinear systems with known invariant observable subspaces where possible; verify semigroup composition and observable evolution. **Gate:** independent analytical solution, semigroup identity and explicit truncation error.
- **M70 — Data-driven finite observable estimation:** implement finite EDMD/ResDMD and optional validated dictionary selection outside the audio callback, not an 'infinite projector'. **Gate:** training/validation/test separation, rank/conditioning analysis, dictionary coverage and genuine held-out prediction.
- **M71 — Spectral-pollution and stability guards:** compare observable dictionaries, residuals, spectral estimates, pseudospectra and conditioning; detect spurious eigenpairs. **Gate:** adversarial known-spectrum controls and thresholds fixed before test outcomes.
- **M72 — Thermodynamic observable coupling:** measure/derive dissipation, impedance, correlation and fluctuation-dissipation consistency using actual calibrated analog acquisitions. **Gate:** temperature, bandwidth, component uncertainty, amplifier-background and load controls; models alone never equal measured devices.
- **M73 — AC/DC Koopman system-identification experiment:** identify a physical circuit's impulse/step/forced dynamics using observed node data, estimate finite Koopman model, then predict held-out excitations. **Gate:** real hardware data, blind comparison against RLC equations, linear state-space and static/null models.
- **M74 — Physical parameter-loop eligibility:** characterize an actually controllable multi-parameter loop (e.g. two tunable reactances/couplings), cycle closure and repeatability; ordinary node-waveform cycles alone are not proof of geometrical phase. **Gate:** measured parameter trajectories and timing error; invalid loops explicitly refused.
- **M75 — Geometric phase model selection:** choose Berry only for appropriate eigenstate bundles, classical Hannay only with relevant action-angle hypotheses, or a separately justified classical oscillator/network connection; derive A and curvature with gauge rules. **Gate:** physical parameter space, spectral gap/adiabatic assumptions if required, independent closed-loop calculation.
- **M76 — Phase measurement and subtraction:** instrument coherent phase readout and estimate ordinary dynamical phase, transport phase, instrument delay, drift and uncertainty. **Gate:** blind separation of geometric term using preregistered estimator; blank/no-loop control and calibration.
- **M77 — Holonomy falsification campaign:** reverse loop orientation; vary speed, dwell, deformation, initial phase, amplitude, load, temperature, noise and open/closed path. **Gate:** correct orientation/path signature under stated assumptions; dissipation or noise sensitivity documented rather than claiming immunity.
- **M78 — Persistence and write/read evaluation:** experimentally determine whether a measured path-dependent phase survives long enough to store distinguishable symbols across noise/drift/reset, without asserting topological protection. **Gate:** measured confusion matrix, retention, endurance, energy, adversarial perturbations and comparison against conventional references.
- **M79 — QEC/tableau/observable bridge:** maintain separate semantics for five-qubit software syndrome QEC, HX87-style *logical* frontiers and classical observable lifts; define any mapping explicitly. **Gate:** algebraic commutation/syndrome oracle, provenance trace, refusal for 'physical qubit' without qubit hardware.
- **M80 — Multiple observable-frontier coupling:** connect bounded Q²-inspired frontiers to observable ensembles, with sparse physically measurable coupling when devices exist; never treat logical frontier multiplicity as physical superposition. **Gate:** resource accounting, independent serial reference and conditional device intervention.
- **M81 — Observables-based cybernetic control:** compare Koopman-predictive regulation with original DACB, raw-state, linear Kalman and bounded nonlinear controls under matched work and held-out disturbances. **Gate:** prespecified error/latency/energy/stability acceptance plus equal-input controls.
- **M82 — Joint physical noise and path experiments:** explicitly separate conditioned RDSEED/RDRAND, directly measured Johnson noise, deterministic replay and potential path-dependent phase; measure causal interactions rather than conflate them. **Gate:** device-provenance matrix and separate raw physical / conditioned digital evidence.
- **M83 — Physical operator and performance acceptance:** treat analog Koopman/holonomy calculation as achieved only when controlled physical inputs yield measured, accurate, repeatable task results and hardware costs are included. **Gate:** instrument traces, no software result substitution, held-out tasks and equal-precision joules/answer comparisons.
- **M84 — Bounded self-checking multiscript watchdog:** implement reproducible preflight/inventory/milestone/dependency/source-integrity/citation checks with bounded self-reentry and immutable run logs. **Gate:** actual positive/negative tests, failure preservation, maximum rounds, timeout and no automatic hardware actuation or source modification.
- **M85 — Unified conditional release and handoff:** include complete original milestone readback, M66–M85 proof/counterproof dossiers, raw hardware status, executable watchdog evidence, versioned artifacts and falsifiable continuation instructions. **Gate:** archive CRC, per-file SHA-256, clean extraction, watchdog PASS; physical gates remain BLOCKED/NOT_RUN until actually measured.

## New dependencies and critical path
M66→M67→M68/M69→M70→M71→M73→M81. M31→M37/M38→M72→M73 and M31→M74→M75→M76→M77→M78. M35/M46→M79→M80 are separately isolated research branches. M20/M22/M25→M82; M72/M78/M81/M82→M83. M84 and M85 audit all prior work without pretending unfinished physical gates are complete. Original three flagship experiments M15/M17/M21 remain mandatory and unchanged. No cycle permitted in implementation dependencies.

## Meaning of a passing result
A mathematical identity can PASS after independent symbolic/exhaustive verification. A *software approximation* can PASS numerical and held-out tests but cannot be marked `MEASURED_PHYSICAL`. An *electrical computation* only passes with actual controlled devices, calibration, raw traces and independent readout. A *geometric phase* requires hypotheses and path tests. No claim of universal immunity, indestructible memory, unconditional cryptographic security or physical infinite-dimensional compute without direct evidence.


# New physical-first milestones M86-M115

All milestones below start as PROPOSED. A published SPICE topology is a design artifact, not a fabricated or measured circuit.
Dependency order is strict. No incomplete physical gate may be described as a completed computation.

## M86 — Immutable physical-only continuation
**Dependency:** M85. **Deliverable:** Preserve M00-M85 without renaming completed work; freeze source and geometry audits. **Gate:** Two archive hashes and exact copied baseline netlists; every new status starts PROPOSED. **Status:** PROPOSED.

## M87 — Domain-correct observables and phases
**Dependency:** M67,M86. **Deliverable:** Define volt/ampere/energy/dissipation/phase domains; reject invalid curl of scalar plus loop integral. **Gate:** Independent dimensional audit and explicit physical observables; no undefined Berry connection. **Status:** PROPOSED.

## M88 — Independent hardware access and safety
**Dependency:** M31,M86. **Deliverable:** Identify isolated supplies, physical meters, component ratings, grounds, calibration and operator authority. **Gate:** Instrument serials, calibration, voltage/current/power bounds or NOT_RUN_NO_DEVICE. **Status:** PROPOSED.

## M89 — Original DC physical weighted network
**Dependency:** M37,M88. **Deliverable:** Wire original analog_dc.cir conductance network without using numerical output as measurement. **Gate:** Two independently measured y-node voltages for polarity and load controls. **Status:** PROPOSED.

## M90 — Original loaded AC physical network
**Dependency:** M37,M88. **Deliverable:** Wire original analog_ac_loaded.cir topology and measure phasors against frequency. **Gate:** Phase/amplitude/bandwidth measurements and repeatability across several physical loads. **Status:** PROPOSED.

## M91 — Readout and loading calibration
**Dependency:** M88,M89,M90. **Deliverable:** Measure input/output impedances, probe loading, cable capacitance and ground arrangement. **Gate:** Repetition using second instrument and documented calibration uncertainty. **Status:** PROPOSED.

## M92 — Unpowered passivity and output safety
**Dependency:** M88. **Deliverable:** Check unplugged-state energy, discharge, passive attenuation and fuse/mute paths before any power. **Gate:** Human-approved electrical safety review; absolutely no direct speaker or medical-device attachment. **Status:** PROPOSED.

## M93 — Linear resonant AC hardware response
**Dependency:** M90,M91,M92. **Deliverable:** Measure RL/C resonance, transfer phase and energy loss at bounded excitation. **Gate:** Measured resonance/phase/Q or reported absence; independent meter and known-control response. **Status:** PROPOSED.

## M94 — Two physical control parameters
**Dependency:** M93. **Deliverable:** Measure actual reverse-biased diode C(V) and two independent tuning effects. **Gate:** Measured capacitance or frequency response for each tuning port and cross-couplings. **Status:** PROPOSED.

## M95 — Reverse-breakdown physical noise junction
**Dependency:** M88,M92. **Deliverable:** Characterize current-limited physically reverse-biased semiconductor over temperature. **Gate:** Real current/voltage spectra and source-off, non-breakdown and part-swap controls. **Status:** PROPOSED.

## M96 — Johnson-Nyquist resistor reference
**Dependency:** M88,M91. **Deliverable:** Measure thermally generated noise from characterized resistors, bandwidth and temperature. **Gate:** Measured mean-square noise with amplifier noise removed and uncertainty versus 4 kBT R bandwidth. **Status:** PROPOSED.

## M97 — Physical noise-to-resonator coupling
**Dependency:** M93,M95,M96. **Deliverable:** Connect current-limited noise junction by measured AC coupling; map loading and interaction. **Gate:** Before/after trace, matched impedance null and controlled source-disconnect comparison. **Status:** PROPOSED.

## M98 — Source/provenance attack and failure study
**Dependency:** M95,M97. **Deliverable:** Challenge source with shield/thermal/power changes, saturation, external interference. **Gate:** Instrumented negative controls; no entropy/security estimate beyond defensible source model. **Status:** PROPOSED.

## M99 — Physical-operation acceptance baseline
**Dependency:** M89,M90,M91,M97. **Deliverable:** Specify one useful task with raw physical input and independent measured output. **Gate:** Success or failure with total energy, control/readout costs, equal-error ordinary-compute comparator. **Status:** PROPOSED.

## M100 — Orientation and reciprocity campaign
**Dependency:** M93,M94,M99. **Deliverable:** Reverse excitations/ports and exchange instrument leads at equal device conditions. **Gate:** Hold-out reciprocity/hysteresis data, calibration and component-temperature controls. **Status:** PROPOSED.

## M101 — Directional nonlinearity vs conventional models
**Dependency:** M100. **Deliverable:** Compare nonlinear diode/hysteretic response to ordinary impedance and thermal models. **Gate:** Preregistered held-out prediction, fit dimension budget and negative results. **Status:** PROPOSED.

## M102 — Finsler/Randers representation only if needed
**Dependency:** M101. **Deliverable:** Fit a positive homogeneous, strongly convex directional path-cost model. **Gate:** Measured error improvement over ordinary constitutive models and regularity certificate. **Status:** PROPOSED.

## M103 — Finsler hardware claim eligibility
**Dependency:** M102. **Deliverable:** Check whether proposed directional physical operator is causal and repeatable. **Gate:** Direct measurable benefit; otherwise REJECT theory for this circuit, never relabel as hardware Finsler. **Status:** PROPOSED.

## M104 — Koopman physical observable contract
**Dependency:** M87,M93. **Deliverable:** Choose finitely measurable energy, current, dissipation, ring-down and phase observables. **Gate:** Repeatability, domains and sensor error estimated before any operator fitting. **Status:** PROPOSED.

## M105 — Koopman held-out observable evolution
**Dependency:** M104,M99. **Deliverable:** Infer and validate finite lifted observable dynamics outside physical computation path. **Gate:** Time-shift and perturbation tests against direct circuit dynamics, no infinite operator claim. **Status:** PROPOSED.

## M106 — Two-parameter closed control path
**Dependency:** M94,M92. **Deliverable:** Apply reproducible physical closed cycles with two independent bias signals. **Gate:** Record actual measured path, closure, amplitude, speed and drift controls. **Status:** PROPOSED.

## M107 — Phase-reference and dynamical subtraction
**Dependency:** M106. **Deliverable:** Calibrate independent phase reference and subtract ordinary resonator/delay contributions. **Gate:** Cycle-reversal/speed/null-loop controls; uncertainty below claimed residual phase. **Status:** PROPOSED.

## M108 — Holonomy physical identification
**Dependency:** M107,M87. **Deliverable:** Derive valid classical connection if evidence supports it; test geometric phase. **Gate:** Measured path-only residual with orientation/deformation signature; otherwise NO_HOLONOMY. **Status:** PROPOSED.

## M109 — Phase-based physical memory usefulness
**Dependency:** M108. **Deliverable:** Test retention, repeatable writing/reading, destructive readout and perturbation sensitivity. **Gate:** Confusion matrix, retention, power, endurance and measured failure rates. **Status:** PROPOSED.

## M110 — Measured relaxation hierarchy prerequisite
**Dependency:** M97,M99. **Deliverable:** Identify distinct physical metastable states and timescales without binning to force result. **Gate:** Repeatable physical state clusters and transitions with interventions and hidden validation. **Status:** PROPOSED.

## M111 — Ultrametric model competition
**Dependency:** M110. **Deliverable:** Compare p-adic/tree ultrametric predictors with Euclidean, rate and hysteretic baselines. **Gate:** Independent held-out data with predefined mapping and complexity penalties. **Status:** PROPOSED.

## M112 — Mathematically typed cross-domain bridge
**Dependency:** M103,M108,M111. **Deliverable:** Only if each branch independently passes, specify real-to-hierarchy measurement map, units and loss. **Gate:** New falsifiable prediction beyond separated models; do not multiply Qp and R values implicitly. **Status:** PROPOSED.

## M113 — Physical multilevel/polyform study
**Dependency:** M35,M46,M88. **Deliverable:** Investigate measured distinct analog state levels with physical set/reset and readout. **Gate:** Measured repeatability/confusion/energy; Roman symbols and software QEC not counted as quantum hardware. **Status:** PROPOSED.

## M114 — Independent analog safety interlock
**Dependency:** M92,M93. **Deliverable:** Design outer physical guard: current limit, temperature/fuse, attenuation and no-speaker direct route. **Gate:** Physical trip/reset tests with operator approval; fail-safe documented for stuck outputs. **Status:** PROPOSED.

## M115 — Hardware-only conditional release
**Dependency:** M86,M87,M99,M105,M108,M111,M113,M114. **Deliverable:** Seal source, topology, measured negative/positive evidence and continuing blockers. **Gate:** CRC/SHA provenance PASS; physical acceptance only with actual calibration traces; no simulated results. **Status:** PROPOSED.

