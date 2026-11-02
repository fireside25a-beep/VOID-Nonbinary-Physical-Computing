# VOID R05: forensic claim audit and gaps, grounded in circuit source

### Verified by inspection and controlled static checks
- Five K05 voltage sources are electrically used; R04 corrected historical Vxm3 and repeating-decimal resistor branches. KCL equalities are nominal algebraic verification, not measured device outputs.
- K01 has an externally supplied 24 V rail, 3.3 kOhm limiting resistor, 100 Ohm sensing resistor, physical reverse-biased 7.5 V class diode model and AC coupling to two-node passive mesh. K02 is same source at zero bias; K03 is a 100 kOhm Johnson reference; K04 is a 50 Ohm terminated reference.
- The K01–K04 mesh has capacitors and resistors and **no inductor**; it is not a physically implemented resonant RLC mesh. There is no physically controlled two-parameter phase loop.
- K05 is a separate DC reference network. It is **not electrically connected to K01–K04**; this separation is intentional as a DC reference fixture, but an integrated SNN-like mixed noise/weighted-sum accelerator is NOT built.
- The 1 MOhm || 30 pF mesh output probes and 10 MOhm K05 output meters are nominal electrical loads in the design. Different real instruments require actual impedance verification.
- Neither an analog multilevel RBit cell, a physical feedback loop, a real acoustic/speaker interface, an accessible on-die analog mesh, nor a DAC/ADC PCIe BAR mapping is supplied by the active netlists or evidence archives.
- No evidence record TSV contains bench rows. The release contains physical circuit designs and historic DACB software tests, not calibrated measurements of the VOID hardware.

### Wrong or unsupported promotions to avoid
- Nominal mathematical y0/y1 equals a measured instrument output — false promotion.
- A diode DC .MODEL with BV/IBV proves a measured avalanche excess-noise spectrum — false promotion.
- A shared passive RC mesh mathematically acts as a demonstrated physical SNN or quantum stabilizer — false promotion.
- `RDRAND`/`RDSEED` produces real conditioned entropy, but those instructions do not identify a raw analog user-accessible K01/K05 mapping.
- Arbitrary unsigned addresses, `nop` cycles, or single-sample equality outcomes prove material operation — false promotion. Real custom hardware access is an engineering target; it needs an identified physical interface and cause/effect evidence.
- Lack of clock means flat settling time at arbitrary scale — unsupported; characterize built network scaling if claimed.

### Remaining high-value independent tests
1. K05 physical assembly, source polarity, branch tolerance and loaded y0/y1 with raw instrument files.
2. K01–K04 real reverse-bias I–V and noise transfer, passive-source/terminated controls, instrument self-noise and host-absent analog observations.
3. K01–K04 *measured* simultaneous node response and coupling versus changed physical component/source conditions. This is the cleanest evidence for analog multi-node computation already designed.
4. Only after those measurements, independently assess a finite observable predictive model at Gate K without turning prediction into the substrate.
5. Defer new physical multilevel elements, Finsler and holonomy campaigns until the respective physical variables are actually available and separately testable.
