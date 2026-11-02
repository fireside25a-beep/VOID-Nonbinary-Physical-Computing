#ifndef VOID_ANALOG_API_H
#define VOID_ANALOG_API_H
#ifdef __cplusplus
extern "C" {
#endif
/* Actual 3-input, 2-output passive nodal solver; scalar units volts and amperes. */
int void_acdc_sample(double x0, double x1, double x2, double *y0, double *y1, double *kcl_residual);
#ifdef __cplusplus
}
#endif
#endif
