# AC/DC passive analog neural-compute proof

## Status and scope

**Reproducible physical-equation simulation, NOT an experimental hardware measurement and NOT a full LLM.**

The C11 executable solves real Kirchhoff current-law (KCL) equations for a two-output,
three-input passive neural dot-product layer in two different substrates:

1. **DC resistive:** signal values are DC voltages; resistor conductances encode the
   non-negative magnitudes of fixed weights. No binary arithmetic in the modeled core.
2. **AC capacitive:** signal values are sinusoidal phasors at a shared frequency;
   capacitor admittances encode the non-negative magnitudes of fixed weights.
   Again, no binary arithmetic in the modeled core.

Negative weight coefficients use inverting source rails (the opposite voltage for
DC, or an extra 180-degree phase for AC). The rails are IDEAL BOUNDARY CONDITIONS.
Their practical drivers, energy consumption, programmability, and readout circuits
are NOT included in the passive-core energy model. A complete device cannot
remove all active circuitry just by using the passive networks demonstrated here.

This simulation runs on a conventional digital CPU; the CPU itself still switches
transistors as it numerically solves these physical equations. The simulation does
not turn that CPU into a native analog device.

## Fixed physical layer

Input voltages (or AC peak phasors): `x = [0.8, -0.4, 0.2] V`.

Matrix:

```
    +0.50  -0.25  +0.75
    -0.30  +0.60  +0.40
```

Expected unattenuated dot products: `W*x = [0.65, -0.40] V`.

For each row, sum of absolute weights plus shunt weight is exactly 2:

- Row 0: 0.50 + 0.25 + 0.75 + 0.50 shunt = 2
- Row 1: 0.30 + 0.60 + 0.40 + 0.70 shunt = 2

Thus the output of the *passive* circuit is `W*x/2 = [0.325, -0.200] V`.

### DC: resistor network

Every input uses a resistor with conductance `G_ji = |W_ji| / (1000 ohms)`.
Each output has an additional grounded shunt resistor `G_shunt = shunt_weight/1000`.

KCL at output node `j` is

```
 sum_i G_ji * (V_ji - V_out,j) - G_shunt,j*V_out,j = 0
 V_out,j = (sum_i G_ji V_ji) / (sum_i G_ji + G_shunt,j)
```

`V_ji = x_i` for a positive weight and `-x_i` for a negative weight.

At the exact stated voltages, ideal resistor power dissipation summed across both
output networks is **0.00040275 W = 0.40275 mW**. This is not chip/system power.

### AC: capacitor network

Every resistor branch is replaced with a passive capacitor
`C_ji = |W_ji| * 100 pF`; each grounded shunt becomes
`C_shunt = shunt_weight * 100 pF`.

`Y_ji = j 2*pi*f*C_ji` is the capacitor admittance.

KCL yields

```
 V_out,j = (sum_i j*2*pi*f*C_ji * V_ji)
           / (sum_i j*2*pi*f*C_ji + j*2*pi*f*C_shunt + G_readout)
```

For ideal infinite readout impedance (`G_readout = 0`) and nonzero AC frequency,
the frequency cancels and `V_out = W*x/2`. This is NOT a way to compute at DC
with capacitors: the AC network would be floating for steady DC operation.

For a finite 1 MΩ readout, the output is frequency- and phase-dependent.
The simulation computes actual complex phasors and validates nodal KCL.
At 100 kHz, row 0 output is approximately
`0.324979420438 + 0.002586104058j V`, magnitude `0.324989710056 V`.
At 50 Hz, row 0 magnitude falls to `0.020380163045 V`.

These are **idealized physical-model results**, not observed real circuit performance.
At high frequencies real devices have losses, parasitic capacitance/inductance,
source output impedance, finite measurement bandwidth, and noise.
At low frequencies leakage and readout can dominate.

## Reproduce

No root, no downloads, no Python package installation:

```
cc -std=c11 -O2 -Wall -Wextra -Werror -pedantic analog_core.c -lm -o analog_core
./analog_core --test
./analog_core > simulation_results.csv
python3 validate_spice_netlists.py
```

`--test` verifies 4096 fixed-seed inputs plus three boundary vectors for each of
2 outputs in both DC and AC, and separately checks AC frequency invariance in
the ideal case. The Python script independently parses the three actual SPICE
netlists and solves their complex or real nodal equations without reusing the
C implementation or hardcoding its matrix. It compares to the C output CSV.

Files:
- `analog_core.c`: physical KCL solver, deterministic inputs, circuit tests, CSV report.
- `analog_dc.cir`: transistor-free DC resistor core SPICE netlist.
- `analog_ac.cir`: transistor-free AC capacitor core SPICE netlist.
- `analog_ac_loaded.cir`: AC netlist with a 1 MΩ readout load.
- `validate_spice_netlists.py`: independent basic passive nodal checker.
- `simulation_results.csv`: computed circuit model results.
- `test_log.txt`: observed test output on this container.
- `SHA256SUMS`: file hashes (excluding itself).

The `.cir` files are usable with ngspice, e.g. `ngspice -b analog_dc.cir`.
**ngspice was not installed in this runtime and its own run has NOT been claimed.**
The independent Python checker is a restricted real-circuit solver and does not
pretend to be a complete SPICE implementation. It models only ideal R/C, grounded
ideal voltage sources, and linear readout loading.

The included `analog_core` binary is built for **Linux x86-64** using the local
compiler. Rebuild from `analog_core.c` for other OS/CPU combinations.

## What this proves, and what it does not

Proves in a mathematical/circuit-simulation sense:
- Linear neural dot products can be realized by physical passive networks without
  a clocked or binary arithmetic unit in the network itself.
- DC resistors and AC capacitors can yield the same scaled linear transform.
- Finite readout impedance changes the AC result substantially with frequency.

Does NOT prove:
- A working standalone analog LLM, tokenizer, dynamic KV cache, backpropagation,
  layer normalization, softmax, nonlinear activation, or physical analog memory.
- Transistor-free external input encoding, programmable negative weights,
  amplification between layers, stable readout, or generation of fresh tokens.
- Higher physical accuracy, throughput, lower total power, or exponential speedup.
- That 50/60 Hz electricity is an effective computation carrier for this circuit.
- Free computation: ideal capacitors store/return energy, but practical drivers,
  conductors and readers consume energy.

The next rigorous step would be a multi-layer nonlinear analog architecture and
end-to-end benchmark with conversion, memory, noise and control energy all measured.

## Peer-reviewed evidence (separate from this simulation)

- IBM analog speech chip (2023, Nature): 35 million PCM devices, 34 tiles, up to
  12.4 TOPS/W chip-sustained (not a full LLM):
  https://www.nature.com/articles/s41586-023-06337-5
- IBM 14 nm ALBERT transformer chip (2025, Nature Communications): 7.1 million
  unique analog weights represented in 28.3 million devices, 1.8 percentage points
  average accuracy below FP32 reference on measured evaluation tasks:
  https://www.nature.com/articles/s41467-025-63794-4
- Analog self-attention for language models (2025, Nature Computational Science):
  attention-performance estimates based on circuit simulations and architecture
  models, NOT complete silicon LLM measurements:
  https://www.nature.com/articles/s43588-025-00854-1
- Nonlinear analog frequency-domain acoustic/phononic neural networks (2025,
  Nature Electronics), 98.2% on a four-class experimental task:
  https://www.nature.com/articles/s41928-025-01436-9
- Official ngspice docs: https://ngspice.sourceforge.io/docs.html
