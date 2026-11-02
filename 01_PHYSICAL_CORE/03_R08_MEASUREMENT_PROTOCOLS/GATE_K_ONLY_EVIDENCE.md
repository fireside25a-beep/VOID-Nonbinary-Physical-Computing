# Exact evidence gates — K only

NO PHYSICAL PASS MAY BE CLAIMED FROM ANY NETLIST, analytic result, script, simulation or stored historical evidence. Physical fabrication and measurements require access to an actual circuit and calibrated equipment. This environment has no connected external sensor/DAQ/analog component interface.

Sequence on a physically fabricated board:
1. Verify assembly against this revision's connectivity and actual component identities unpowered. Check polarity, rail isolation, DC-block leakage, current-limit and direct-port safety.
2. Calibrate the sensor chain and log full analog transfer function and gain, sample-clock accuracy, temperature and input-referred noise. Record external instrument energy separately.
3. Under operator-controlled isolated low-voltage current-limited conditions, measure actual junction I-V and shunt drop; stop on unexpected heating, bias, shorts, or unsafe load. Do not impose an unverified step that exceeds component limits.
4. Measure K04 termination (finite thermal noise), K02 diode with connected zero-volt rail (not equivalent to disconnected), K03 unpowered resistor, K01 powered junction, in preregistered independently recorded runs at fixed steady bias/temperature. Use matched receiver gain/bandwidth, record source impedance, and repeat with receiver/channel interchange to check artifacts.
5. Preserve original raw physical traces, device ID, maker/lot, rail volt/current, shunt readback, board photo, instrument chain and bandwidth, clock, cable routing, environmental temperature and raw file SHA-256. Do not record simulated or synthetic waveforms as measurements.
6. K finite-model question, only after authentic traces: evaluate conditional means and conditional variances against mean/AR/instrument baselines on strictly separated acquisition runs. Analyze DMD/TLS-DMD and, where observation and process noise interact, subspace DMD as independent external methods. Define rank and performance threshold before held-out evaluation. Failure rejects the SPECIFIED finite model and operating regime, not universal Koopman mathematics.

Gate F directional tests: LOCKED. Gate H geometric phase tests: LOCKED. No p-adic, Finsler or Berry protection interpretation can be imported into a K outcome. No circuit can be called physically computational or quantum merely because it has noise and multiple observed nodes.
