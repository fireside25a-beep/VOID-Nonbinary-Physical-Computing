# VOID R03 existing build evidence review — source-focused

Date: 2026-10-29. Purpose: correct overbroad denial of physical on-chip computation without fabricating support for specific custom connections. Inspected read-only before document updates.

## Positive primary record

- `/mnt/data/BCSE_PHYSICAL_COMPUTATION_MASTER_20261029/08_EVIDENCE/ISA_PROBE_RUN_01.log`: reports CPUID hypervisor indicator YES, RDRAND/RDSEED words; scope statement ISA only.
- `/mnt/data/BCSE_PHYSICAL_COMPUTATION_MASTER_20261029/08_EVIDENCE/ISA_PROBE_RUN_02.log`: second set of ISA outputs; still digital interface, not a raw analog trace.
- `/mnt/data/BCSE_PHYSICAL_COMPUTATION_MASTER_20261029/02_HARDWARE_GATE/isa_probe_x86_64.s`: includes CPUID and ISA instructions. The constant `0x40000000` here is a CPUID flag mask, NOT an address-mapped ADC register.
- Intel's published DRNG design specifies asynchronous on-chip entropy generation from thermal noise (a native physical process) and subsequent digital conditioning. This positively refutes the wording 'strictly digital processor' when applied to its full physical implementation.

## Specific VOID circuit references

- `02_PHYSICAL_CIRCUITS/VOID_K01_BIASED_BREAKDOWN_WITH_MESH.cir`: explicitly selects a physically buildable external 24V supply, 3.3k current-limit resistor, 100-ohm Kelvin resistor, nominal BZX55C7V5 7.5V diode model, capacitor coupling, readout ports. Not a measured on-die interconnect.
- `02_PHYSICAL_CIRCUITS/VOID_K02_DIODE_ZERO_VOLT_WITH_MESH.cir` and `VOID_K03_PASSIVE_JOHNSON_WITH_MESH.cir`: source controls, not physical acquisitions.
- `02_PHYSICAL_CIRCUITS/VOID_K05_DC_ADMITTANCE_WITNESS.cir`: resistive analog DC witness and explicit 10MOhm meter-loading references, with calculated y0 and y1, not actual logged voltages.
- The active R03 `VOID_RAW_PHYSICAL_EVIDENCE_REGISTER.tsv`, `VOID_K05_PHYSICAL_ACQUISITIONS.tsv`, `VOID_GATE_K_PHYSICAL_TRANSIENTS.tsv` are each **one header line with no measurements**.
- The prior sealed R02 ZIP passed CRC; all six 02_PHYSICAL_CIRCUITS source members and five 01_PRESERVED_INPUTS ZIP members matched the active worktree byte-for-byte during this audit.

## Pending evidence to resolve the user's stronger claims

1. **On-die custom substrate:** directly attributed die circuit/terminal/control mapping and a measured physical operator implementing the selected admittance function.
2. **Addresses:** real processor/board/device identity, mapped resource evidence for `0x40000000` and `0x40000008`, safe readback or documented DAC/ADC connection. Same numerical constant as CPUID bitmask is not corroborating evidence.
3. **Settling:** independently timed analog response under controlled input schedule, including fixture/instrument delay. Instruction execution is a real hardware event but does not by itself certify analog settling.

No final negative conclusion about future semiconductor architectures, undisclosed dies, or user-held external physical evidence is drawn. The result is an exact assessment of materials actually inspected in this container and relevant Library search.

## Continuity controls

The user-requested computer-independent physical evolution remains the primary goal. No new C, assembly, software qubits, synthetic noise, or fake physical traces have been created. Existing circuit sources and preserved ZIPs remain immutable. The original categorical host-interface text has been replaced in place by an evidence-reopened decision. Future measured hardware evidence should supersede any provisional unknown immediately after source validation.
