# VOID R06 authoritative physical wiring — one unencoded material machine

The ONLY active integrated circuit is `02_PHYSICAL_CIRCUITS/VOID_K06_INTEGRATED_PHYSICAL_CONTINUUM.cir`.

Original K01 physical breakdown junction (24V, 3.3k limiting resistor) -> original 2-node RC mesh. Original K05 5-input/2-output resistor network -> two capacitor-resistor couplings -> SAME mesh. Existing actual inductor/series capacitor/resistor and two coupled capacitor charge-state nodes remain. Anti-parallel real diode pair with 47k series resistance creates a nonlinear physical path between charge states. There is no numerical state-evolution processor, digital register, noise generator, or program controlling a physical material update.

The ONE new primitive input module `VOID_PRIMITIVE_MATERIAL_INTERFACE.lib` contains eight mechanically variable contact resistances and two physical potentiometer wipers. Contacts join through two common FIELD_A/B analog electrodes and four coupling resistors into shared mesh/charge nodes. Two external analog boundary voltage sources also join the mesh through 470k resistors. No physical alphabet, per-key encoded ROM, software qubit or binary conversion is embedded in the circuit.

The SAME CHARGE_A/B physical nodes produce X/Y analog visual-display electrode voltages. Two additionally powered BJT/LED output stages convert charge-state voltages to light intensity by actual semiconductor conduction. These are electrical and optical output primitives, not a digital display program, text renderer or a complete assembled board.

Retired duplicate alphabet-specific modules and superseded R06 documentation are stored intact in `01_PRESERVED_INPUTS/R06_SUPERSEDED_UNSEALED_HUMAN_IO/`; they are not active includes. Complete physical component connections, pin-by-pin interface mapping, nominal source-only models, independent source returns, and current monitoring are covered in the regenerated R06 component and port TSVs. K01–K05 historical source controls and M00–M115 original roadmap remain unchanged.

Hardware realization requires actual components and instrument capture, not a numerical result substituted for the physical operation. Never claim measured voltage, light output, SNN operation, physical RBits or physical noise just because this source topology contains their candidate component classes.
