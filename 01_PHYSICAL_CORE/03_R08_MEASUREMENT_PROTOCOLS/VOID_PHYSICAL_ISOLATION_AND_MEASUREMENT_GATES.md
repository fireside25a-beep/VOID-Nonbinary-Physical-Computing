# Gate K — actual physical isolation and witness acceptance

## A. Hardware preparation before energizing

Use the existing K01–K04 shared two-node mesh and K05 DC witness. Confirm component identity, orientation, contact resistances, protection ratings, 24 V current-limited external rail and isolation of instrument grounds. The source's diode has a nominal datasheet 7.0–7.9 V reverse voltage at 5 mA, not a certified excess-noise spectrum. Verify voltmeters and oscilloscope input impedance and bandwidth, environmental interference, and a fault-safe physical power switch. An independent skilled bench operator performs first energization.

## B. First measurable physical operator: K05

K05 uses six independent external DC source terminals and physical resistor conductances. The source values, polarities, instruments and their energy supplies must be REAL and logged. The external voltmeter loading is now explicitly included as two 10 MOhm input loads, which are instrument equivalents, not extra resistors to install in parallel. Nominal unloaded mathematical reference: y0=+0.325000000 V, y1=-0.200000000 V. Nominal loaded target for ideal, exactly specified resistor values and true 10 MOhm meters: y0=+0.324983750812 V, y1=-0.199990000500 V. They are expected analytical references only. Compare actual voltages against independently measured source/resistor/voltmeter tolerances, not an invented universal accuracy guarantee.

Disconnection requirement: power physical source references and voltmeters independently; unplug host computing devices; demonstrate y0 and y1 persist physically when the external voltage references remain powered. No claim of digital-free BUILD or fabricating hardware follows from this design file alone.

## C. K01–K04 physical noise response

First capture source-off and terminated receiver traces, then unbiased resistor reference, then powered diode. Equalize receiver settings; measure actual source impedances (50 ohm and 100 kohm control sources are intentionally not matched) and calibrate the transfer through the identical capacitor/resistor mesh. Exchange readout channels and cables to distinguish source-correlated behavior from receiver artifacts. Raw original instrument files, calibration records, board photographs and energy measurements become authoritative.

The K01 diode's Spice `.MODEL` is a static DC approximation and is NOT a validated avalanche excess-noise generator. The `.cir` file may be used for connectivity review, never to produce fake experimental waveforms.

## D. Physical versus controller energy

Keep distinct records for physical substrate input bias energy, physical source-reference power, analog pre-amplification, sampling/ADC/converter, control, and external acquisition instruments. Total end-to-end energy is the sum of the *actual consumed* energy within the claimed system boundary. Do not report "energy saved" by subtracting readout energy, or assume an unpowered resistor supplies net usable free work.

## E. Gate criteria

K hardware status can change from DESIGN to MEASURED_PHYSICAL only when real hardware identity, calibrated current/voltage readbacks, raw traces and independent source controls are all available. Finite Koopman observables can be assessed externally only after this acquisition, with train/held-out runs separated and prespecified rank/accuracy thresholds. Finsler and holonomy remain LOCKED; no cross-category promotion.
