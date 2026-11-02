/* Adapt the exact archived AC/DC C11 nodal solver to a callable C ABI.
 * Rename only its CLI entry point at compile time; dc_node/ac_node and their
 * coefficient sets are compiled verbatim from the original archival source.
 */
#define main void_archived_acdc_cli
#include "../../../02_ANALOG_MATH/01_ACDC_LINEAR_NETWORK/analog_core.c"
#undef main

int void_acdc_observe(const double input[3], double dc[2],
                      double ac_real[2], double residuals[4]) {
    if (!input || !dc || !ac_real || !residuals) return -1;
    for (int i=0;i<3;i++) if (!isfinite(input[i]) || fabs(input[i])>1.0) return -2;
    for (int o=0;o<2;o++) {
        double kcldc=0.0,kclac=0.0;
        dc[o]=dc_node(o,input,&kcldc);
        double complex ac=ac_node(o,input,100000.0,READOUT_RESISTANCE,&kclac);
        ac_real[o]=creal(ac);
        residuals[o]=kcldc; residuals[2+o]=kclac;
        if(!isfinite(dc[o])||!isfinite(ac_real[o])||
           !isfinite(kcldc)||!isfinite(kclac)||kcldc>1e-12||kclac>1e-12)
            return -3;
    }
    return 0;
}
