/* VOID native CPU-work driver: HX89-selected successor *software work cycle*.
 * Compiled x86-64 instructions, real AVX2, persistent state, RDTSCP readings.
 * No hardware MMIO, CPU clock control, physical analog input, or fake entropy.
 */
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <x86intrin.h>
#include <cpuid.h>

#define WORDS 64
static _Alignas(32) uint64_t state[WORDS];
static volatile uint64_t observed_checksum;
static int initialized;

__attribute__((target("avx2"),noinline))
static void vector_cycle(uint64_t step) {
    const __m256i salt=_mm256_set1_epi64x((long long)(UINT64_C(0x9E3779B97F4A7C15)^step));
    for (int repeat=0;repeat<32;repeat++) {
        for (int i=0;i<WORDS;i+=4) {
            __m256i x=_mm256_load_si256((const __m256i*)&state[i]);
            x=_mm256_add_epi64(_mm256_xor_si256(x,salt),_mm256_set1_epi64x((long long)(repeat+1)));
            x=_mm256_xor_si256(x,_mm256_slli_epi64(x,13));
            _mm256_store_si256((__m256i*)&state[i],x);
        }
    }
}
__attribute__((noinline))
static void scalar_cycle(uint64_t step) {
    for (int repeat=0;repeat<32;repeat++)
        for (int i=0;i<WORDS;i++) {
            uint64_t x=state[i]^step;
            x^=x>>12;x^=x<<25;x^=x>>27;
            state[i]=x*UINT64_C(2685821657736338717)+(uint64_t)repeat;
        }
}
int void_cpu_cycle_init(void) {
    __builtin_cpu_init();
    if (!__builtin_cpu_supports("avx2"))return -1;
    unsigned a,b,c,d;
    if (!__get_cpuid(0x80000001u,&a,&b,&c,&d) || !(d&(1u<<27)))return -2; /* RDTSCP */
    for (int i=0;i<WORDS;i++)state[i]=UINT64_C(0xA0761D6478BD642F)^((uint64_t)i*UINT64_C(0xE7037ED1A0B428DB));
    observed_checksum=0;initialized=1;return 0;
}
int void_cpu_cycle_execute(int selection, int epoch, int64_t *digest, int64_t *ticks, int *migration) {
    if (!initialized||!digest||!ticks||!migration||epoch<0||(selection!=0&&selection!=1))return -3;
    unsigned before_cpu=0,after_cpu=0;
    _mm_lfence();uint64_t before=__rdtscp(&before_cpu);_mm_lfence();
    if (selection)vector_cycle((uint64_t)epoch);
    else scalar_cycle((uint64_t)epoch);
    _mm_lfence();uint64_t after=__rdtscp(&after_cpu);_mm_lfence();
    uint64_t h=UINT64_C(1469598103934665603);
    for (int i=0;i<WORDS;i++){h^=state[i];h*=UINT64_C(1099511628211);}
    h^=(uint64_t)selection;h^=((uint64_t)(unsigned)epoch<<32);
    observed_checksum=h;
    *digest=(int64_t)h;*ticks=(int64_t)(after-before);*migration=(before_cpu!=after_cpu);
    return 0;
}
