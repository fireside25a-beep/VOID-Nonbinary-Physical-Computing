# VOID R03 — Reopened physical substrate and external interface decision

Date: 2026-10-29. Status: EVIDENCE REOPENED, not a prohibition on hardware discovery. This document supersedes the previous categorical wording. No prior netlist, source archive, or physical measurement record has been overwritten.

## The correction

Calling x86 a **strictly digital object** is wrong in the physical sense. Real processors include physical analog and mixed-signal phenomena, such as thermal-noise-derived entropy, clock generation, power management and sensing. Intel's published DRNG design describes a self-timed on-chip entropy source using silicon thermal noise, conditioning hardware and software-visible RDRAND/RDSEED outputs. Accordingly, a physical phenomenon **can occur inside an x86 die** without being numerically simulated by host software.

This does not, by itself, identify a user-programmable raw analog matrix on a particular die. A physical entropy source and a user-configurable analog computation fabric are two separate claims to establish by accessible routing, physical stimulus, readout and energy evidence. Both remain legitimate research questions; neither should be declared impossible or already established by fiat.

## Three previously overgeneralized statements — corrected

### 1. On-die material elements

**Corrected:** There are unquestionably physical semiconductor junctions, resistive paths, parasitic capacitances and thermal dynamics inside processors. The external VOID `K01` design specifies `R_CURRENT_LIMIT ... 3.3k`, `R_KELVIN ... 100`, a selected BZX55C7V5 family diode, and a passive coupling mesh in SPICE. These specific parts are actual *proposed external components in that netlist*. No inspected raw die layout, bonding diagram, analog-pin map or manufacturer characterization identifies that exact discrete Vishay diode and 3.3 kOhm resistor as on-die elements in the execution host. That correspondence is **NOT YET EVIDENCED**, not ruled out as a physical principle.

A documented on-die entropy junction or a subsequently discovered die-interface shall be assessed on its actual electrical transfer function, not rejected because it is inside x86.

### 2. Physical MMIO access

**Corrected:** MMIO is a genuine physical device interface and is not inherently a simulation. Device BARs and mapped hardware resources can be accessed where the hardware, system mapping, privileges and device driver are established. The strings `0x40000000` and `0x40000008` appearing in a proposed example are **not currently associated with an enumerated ADC/DAC device** in the inspected evidence. They may be valid on some explicitly mapped platform, but cannot be declared active registers on this host solely from the example.

The older ISA probe source also contains `0x40000000` as a CPUID **flag bitmask**; that occurrence is not an MMIO address and cannot be used as corroboration. No blind raw-address write will be introduced into the VOID release. A verified manufacturer or measured bus mapping would immediately reopen the route, without changing the physical-computing objective.

### 3. Physical settling and instruction delays

**Corrected:** Instructions and fences have real hardware timing effects. A `nop` sequence can occupy finite execution time, and documented processor/barrier behavior can matter for ordering. Nevertheless, a *compiler fence* only constrains compiler rearrangement and a small number of NOPs do not establish a circuit-specific RC settling measurement. To claim the physical response has settled, compare against a measured transient or a previously characterized component/fixture response with its uncertainty; hardware triggers and independent timing references are valid methods. This is an evidence requirement, **not** a general ban on timing experiments using processors.

## Existing evidence: positive and unresolved

**ESTABLISHED FROM FILES:** two previously logged `RDRAND`/`RDSEED` ISA probes executed in a hypervisor-advertised context and produced reported words; the on-chip entropy hardware exists as a documented Intel design class. The five external VOID K01–K05 netlists and `VOID_K_MESH_V1.lib` are real physical-circuit descriptions, preserved byte-for-byte from R02. R03 measurement TSVs exist and are header-only; none is a raw physically acquired trace.

**NOT ESTABLISHED BY THE INSPECTED FILES:** a fabricated or externally assembled K01–K05 fixture; observed analog voltages/current/noise; a die photograph or on-chip interconnect proof for the exact custom R/C/Zener network; a verified BAR that drives these nets; or a physical settling trace established by fence/NOP timing alone. These are open evidence questions, not assertions that such arrangements cannot exist.

## VOID's physical execution objective

Physical mechanisms are allowed and sought wherever they are: external analog mesh, embedded mixed-signal hardware, or verified on-chip material blocks. A discovered accessible material operator should be specified by physical inputs, energy source, observable outputs, and controllable causal transition. The digital host can supervise and capture, but an ISA word or software-algebra output is not silently promoted to the requested analog transformation. Do not conflate source entropy with an arbitrary programmable material computation.

The **host-disconnect test** applies literally to the externally powered K01–K05 case; in an on-chip arrangement where the source shares power with the CPU, independently measure activity under reduced, paused or isolated digital workloads instead. Do not claim impossible galvanic separation within a shared silicon power domain. Power and latency are empirical quantities, not assertions of constant-time/zero-host-load.

## Action for real contrary proof

If earlier builds contain die-level routing diagrams, measured node response, a BAR/resource map, verified physical register wiring, or time-correlated analog captures, register their **actual filenames and hashes** in `VOID_EXISTING_BUILD_EVIDENCE_REVIEW_R03.md`; check them against the physical source. A demonstrated on-chip computation should change the status to PHYSICALLY_MEASURED for that exact hardware operation, not leave this decision frozen.

Evidence labels: DOCUMENTED_PHYSICAL_SUBSYSTEM; VERIFIED_ISA_EXECUTION; NETLIST_SPECIFIED; MAPPED_INTERFACE_VERIFIED; PHYSICALLY_MEASURED; NOT_YET_EVIDENCED. No blanket blocked-by-architecture claim is retained.

References: Intel DRNG guide (https://www.intel.com/content/www/us/en/developer/articles/guide/intel-digital-random-number-generator-drng-software-implementation-guide.html); Linux kernel PCI resource mapping (https://kernel.org/doc/html/latest/PCI/pci.html); inspected original VOID and BCSE evidence files recorded in `VOID_EXISTING_BUILD_EVIDENCE_REVIEW_R03.md`.
