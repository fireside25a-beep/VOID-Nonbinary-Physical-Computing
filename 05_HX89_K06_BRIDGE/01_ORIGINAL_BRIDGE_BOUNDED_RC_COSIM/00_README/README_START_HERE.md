# VOID R08 K06 ↔ HX89 native causal bridge: independently checked co-simulation

**Scope:** A new, actual, reproducible SOFTWARE co-simulation bridge using the **unchanged recovered HX89 binary**, a new HX89 Polyform compiler/driver, and a **40-element source-extracted passive K06 R/C subnetwork** derived from the recovered 2026-10-29 VOID R08 netlist. The original K06 .cir and three referenced .lib files are preserved byte-for-byte. All native HX89 stdout/stderr, compiled Polyforms, numerical charge-node trajectories, and negative/intervention control results are saved.

**What is proven:** The actual native HX89 executable receives thresholded values of charge nodes calculated by a source-checked passive K06 R/C network; its NATIVE_ACCEL arithmetic and IFZERO_DIR produce a decision, which selects the next external simulated bench electrode signal. Closing the loop changes subsequent simulated state; physically breaking the modelled A coupling suppresses that response. A different selected electrode produces different outcomes. The native program is executed, not mocked. The complete repeat run's native stdout/stderr and numerical waveforms were byte-for-byte identical.

**NOT proven:** Physical K06 board operation, an analog electrical output from a computer's CPU pin, manufactured hardware, real ADC/DAC/instrument measurements, runtime integration with a complete nonlinear K06 circuit, actual physical multilevel memory, hardware-native analog computation, or any P-vs-NP/quantum performance claims. The work is not an integrated physical machine. The restored full K06 netlist includes nonlinear diodes and BJTs, inductor, K05 bias, sheet, clamps and display circuits; these were NOT solved by the limited R/C solver. A separate **FULL K06 ngspice testbench was generated but not executed**, because ngspice was unavailable. Its existence does not turn the R/C-only evidence into a full-circuit proof.

## Inventory

- `01_BRIDGE_CODE/k06_rc.py`: source-hash-enforced extract and linear passive R/C backward-Euler transient solve, 40 exact part IDs (30 from original `.cir`, 10 from the mesh `.lib`). This is *not* a full SPICE substitute.
- `01_BRIDGE_CODE/native_bridge.py`: 7 actual run scenarios (96 cycles each). Source-derived charge-node values are digitized at 6 mV, compiled as new HX89 Polyforms, executed with `--native` on the real HX89 binary, and used to select **simulated external** A/B voltages on the next 4 ms interval. A 1.2 V pulse occupies 3 ms per 4 ms interval. All 12 transient steps per interval are logged.
- `03_HX89_BINARY_ONLY/hx89`: **the only HX89 executable; no HX89 runtime source tree is packaged**. SHA256 `50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451`.
- `02_ORIGINAL_K06_NETLIST/`: unchanged VOID R08 `.cir` and three original `.lib` components including original nonlinear parts; no replacement physical netlist.
- `04_EXPERIMENT_LOGS/`: **672 actual native HX89 executions** (96 x 7 scenarios), each with its uniquely generated `.hx` file, raw stdout and stderr, process timing and SHA256 in `native_steps.csv`; plus **8,064 R/C numerical time samples**, every input pulse and all sensor outputs. These are synthetic simulator waveforms, NOT physically measured traces.
- `05_TESTS_AND_AUDITS/`: **24/24 independent tests PASS**, the independent 672-run readback, 96 exact repeat run stdout/stderr byte comparisons, numerical KCL residual and convergence checks, and controlled disconnect/forced-output tests. A **superseded initial diagnostic run** is preserved in `superseded_wrong_sign_run/` and clearly flagged **INVALID** because it preceded a corrected capacitor fixed-source sign. Never cite it as physical or model evidence.
- `07_REPRODUCIBILITY/FULL_K06_SPICE_TESTBENCH/`: original K06 full-circuit input models plus **generated** external-pulse test fixture. NO ngspice execution or hardware capture is claimed.
- `06_PHYSICAL_INTERFACE_PLAN/`: instrument and safety requirements before physical proof.

## Results from the corrected, independently read-back experiment

| Scenario | HX89 native launches | Source-derived charge samples | Meaning |
| --- | ---: | ---: | --- |
| closed_loop | 96 | 1152 | Real HX89 native result chooses external bench electrode |
| closed_loop_repeat | 96 | 1152 | Exact input and output replay, byte-for-byte |
| open_write_a | 96 | 1152 | Remove *simulated* C_WRITE_A_COUPLING; no machine activation |
| no_excitation | 96 | 1152 | Both simulated electrodes held at zero |
| forced_a | 96 | 1152 | Controller force-overrides native output to A after readback |
| inverted_action | 96 | 1152 | Inverts selected electrode despite native decision |
| open_write_b | 96 | 1152 | Remove B coupling branch, negative-control perturbation |

Controlled differences were read from the saved analog waveform CSVs; authoritative numerical values are in `05_TESTS_AND_AUDITS/causal_comparison.json`. The `closed_loop` run reached 3 native positive decisions in 96 cycles (not a made-up continuous CPU learning process). The other comparisons demonstrate finite causal intervention differences only.

## Independent reproduction

On Linux x86-64 with Python 3 + NumPy and the included binary, run **on a copy**:

```bash
python3 01_BRIDGE_CODE/independent_tests.py
python3 01_BRIDGE_CODE/native_bridge.py
python3 01_BRIDGE_CODE/readback_verify.py
```

`07_REPRODUCIBILITY/reproduce_in_fresh_copy.sh` runs all three commands on a temporary copy, without altering the evidence archive. `01_BRIDGE_CODE/generate_full_k06_spice_bench.py` generates an additional model deck. Only `--run`, and only when ngspice is actually available, attempts the optional **full nonlinear K06 SPICE** transient analysis; that optional run has not occurred in this evidence release.

## Honest physical integration status

The **software bridge gap is partially resolved for the selected passive K06 R/C network**. The **physical device/ADC/DAC link and full-netlist feedback loop remain open**. To claim physical proof, a real manufactured and electrically qualified board, calibrated physical input/output instruments, a measured bidirectional IO channel, time-aligned raw physical traces, voltage/current/temperature conditions and negative-control intervention records are indispensable. No readings were fabricated, and R08's physical evidence header-only TSV has not been filled with synthetic output.

**Source preservation:** These four original model files are byte-identical copies from `VOID_OPERATES_INDEPENDENT_OF_DIGITAL_GATE_K_R08_20261029.zip`. The machine executable is the byte-identical recovered HX89 native x86-64 binary; everything else in the bridge code is new. None of the original sealed release archives or the prior 7,992-run SAT evidence were modified or duplicated.
