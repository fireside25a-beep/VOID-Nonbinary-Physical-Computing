/*
 * Passive AC/DC neural dot-product proof
 * C11, no dependencies other than libm. Physical model: Kirchhoff nodal balance.
 * Only the computational network is passive/transistor-free. Sources and measurement
 * are IDEAL boundary conditions, not demonstrated transistor-free hardware.
 *
 * cc -std=c11 -O2 -Wall -Wextra -Werror -pedantic analog_core.c -lm -o analog_core
 * ./analog_core
 */
#include <complex.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define IN 3
#define OUT 2
#define TESTS 4096
#define BASE_RESISTANCE 1000.0 /* R_i = R_base / |w_i| */
#define BASE_CAPACITANCE 1.0e-10 /* C_i = C_base * |w_i| */
#define READOUT_RESISTANCE 1.0e6
#define PI 3.141592653589793238462643383279502884

static const double weights[OUT][IN] = {
    { 0.5, -0.25, 0.75 },
    {-0.3,  0.6,  0.4 }
};
static const double shunt_weight[OUT] = {0.5, 0.7};
static const double example_input[IN] = {0.8, -0.4, 0.2};

static uint64_t rng_state = UINT64_C(0x9e3779b97f4a7c15);
static uint64_t next_u64(void) {
    uint64_t x = rng_state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    rng_state = x;
    return x * UINT64_C(2685821657736338717);
}
static double next_input(void) {
    /* exactly representable binary fractions in [-1,1] */
    return ((double)(next_u64() % 2049u) - 1024.0) / 1024.0;
}
static double dot(const int out, const double x[IN]) {
    double v = 0.0;
    for (int i = 0; i < IN; ++i) v += weights[out][i] * x[i];
    return v;
}
static double injected_source(const int out, const int i, const double x[IN]) {
    /* A negative weight is encoded on the inverted input voltage rail. */
    return (weights[out][i] < 0.0) ? -x[i] : x[i];
}
static double dc_node(const int out, const double x[IN], double *residual_amps) {
    double numerator = 0.0, total_g = shunt_weight[out] / BASE_RESISTANCE;
    for (int i = 0; i < IN; ++i) {
        const double g = fabs(weights[out][i]) / BASE_RESISTANCE;
        numerator += g * injected_source(out, i, x);
        total_g += g;
    }
    const double v = numerator / total_g;
    double kcl = -shunt_weight[out] * v / BASE_RESISTANCE;
    for (int i = 0; i < IN; ++i) {
        const double g = fabs(weights[out][i]) / BASE_RESISTANCE;
        kcl += g * (injected_source(out, i, x) - v);
    }
    *residual_amps = fabs(kcl);
    return v;
}
static double complex ac_node(const int out, const double x[IN], double hz,
                              double readout_ohms, double *residual_amps) {
    const double omega = 2.0 * PI * hz;
    double complex numerator = 0.0;
    double complex total_y = I * omega * BASE_CAPACITANCE * shunt_weight[out];
    if (readout_ohms > 0.0) total_y += 1.0 / readout_ohms;
    for (int i = 0; i < IN; ++i) {
        const double complex y = I * omega * BASE_CAPACITANCE * fabs(weights[out][i]);
        numerator += y * injected_source(out, i, x);
        total_y += y;
    }
    const double complex v = numerator / total_y;
    double complex kcl = -v * (I * omega * BASE_CAPACITANCE * shunt_weight[out]
                                    + ((readout_ohms > 0.0) ? 1.0 / readout_ohms : 0.0));
    for (int i = 0; i < IN; ++i) {
        const double complex y = I * omega * BASE_CAPACITANCE * fabs(weights[out][i]);
        kcl += y * (injected_source(out, i, x) - v);
    }
    *residual_amps = cabs(kcl);
    return v;
}
static void require_close(const char *name, double actual, double expected, double limit) {
    if (!isfinite(actual) || fabs(actual - expected) > limit) {
        fprintf(stderr, "FAIL %s: got %.17g, expected %.17g, limit %.3g\n",
                name, actual, expected, limit);
        exit(EXIT_FAILURE);
    }
}
static void run_tests(void) {
    double x[IN];
    for (int n = -3; n < TESTS; ++n) {
        if (n == -3) for (int i = 0; i < IN; ++i) x[i] = example_input[i];
        if (n == -2) for (int i = 0; i < IN; ++i) x[i] = 0.0;
        if (n == -1) for (int i = 0; i < IN; ++i) x[i] = 1.0;
        if (n >= 0) for (int i = 0; i < IN; ++i) x[i] = next_input();
        for (int o = 0; o < OUT; ++o) {
            double residual_dc, residual_ac;
            const double expected = dot(o, x) / 2.0;
            const double vdc = dc_node(o, x, &residual_dc);
            const double complex vac = ac_node(o, x, 100000.0, 0.0, &residual_ac);
            require_close("dc/reference", vdc, expected, 1e-13);
            require_close("ac/reference real", creal(vac), expected, 1e-13);
            require_close("ac/reference imaginary", cimag(vac), 0.0, 1e-13);
            require_close("dc/KCL", residual_dc, 0.0, 1e-15);
            require_close("ac/KCL", residual_ac, 0.0, 1e-15);
        }
    }
    /* Frequency invariance is expected only for the IDEAL capacitive network. */
    const double frequencies[] = {50.0, 1000.0, 100000.0, 1000000.0};
    for (size_t i = 0; i < sizeof(frequencies)/sizeof(frequencies[0]); ++i) {
        for (int o = 0; o < OUT; ++o) {
            double residual;
            const double complex v = ac_node(o, example_input, frequencies[i], 0.0, &residual);
            require_close("ac/ideal frequency", creal(v), dot(o, example_input)/2.0, 1e-13);
            require_close("ac/ideal imaginary", cimag(v), 0.0, 1e-13);
        }
    }
    puts("PASS: 4099 deterministic input vectors x 2 outputs x DC/AC");
    puts("PASS: passive nodal-KCL residual bounds");
    puts("PASS: ideal capacitive frequency invariance at 50/1000/100000/1000000 Hz");
}
static void output_report(void) {
    puts("mode,frequency_hz,output,reference_dot_v,real_v,imag_v,magnitude_v,phase_degrees,kcl_residual_a");
    for (int o = 0; o < OUT; ++o) {
        double residual;
        const double v = dc_node(o, example_input, &residual);
        printf("DC,0,%d,%.12g,%.12g,0,%.12g,0,%.3g\n", o, dot(o, example_input), v, fabs(v), residual);
    }
    const double frequencies[] = {50.0, 100.0, 1000.0, 100000.0, 1000000.0};
    for (int loading = 0; loading < 2; ++loading) {
        for (size_t f = 0; f < sizeof(frequencies)/sizeof(frequencies[0]); ++f) {
            for (int o = 0; o < OUT; ++o) {
                double residual;
                const double complex v = ac_node(o, example_input, frequencies[f],
                              loading ? READOUT_RESISTANCE : 0.0, &residual);
                printf("%s,%.12g,%d,%.12g,%.12g,%.12g,%.12g,%.12g,%.3g\n",
                     loading ? "AC_1Mohm_readout" : "AC_ideal", frequencies[f], o,
                     dot(o, example_input), creal(v), cimag(v), cabs(v),
                     atan2(cimag(v), creal(v)) * 180.0 / PI, residual);
            }
        }
    }
}
int main(int argc, char **argv) {
    if (argc > 1 && argv[1][0] == '-' && argv[1][1] == '-' && argv[1][2] == 't') {
        run_tests();
    } else if (argc == 1) {
        output_report();
    } else {
        fprintf(stderr, "usage: %s [--test]\n", argv[0]);
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
