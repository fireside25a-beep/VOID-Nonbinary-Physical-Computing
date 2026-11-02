/* Actual x86-64 AVX2 feedback operation. Selection originates in HX89 native result.
 * TSC is actual executed processor timestamp-counter instruction, not a voltage sample.
 * A genuinely unsupported CPU refuses execution; it does NOT synthesize AVX2 results.
 */
#include <stdint.h>
#if defined(__x86_64__) && (defined(__GNUC__) || defined(__clang__))
#include <x86intrin.h>
__attribute__((target("avx2"),noinline))
static uint64_t run_avx2(uint64_t ticket,int control) {
    __m256i v=_mm256_set_epi64x((long long)(ticket^UINT64_C(0x87ef0123456789ab)),
         (long long)ticket,(long long)(ticket+13),(long long)(ticket^UINT64_C(0xaf43a22bce901237)));
    const __m256i salt=_mm256_set1_epi64x((long long)(UINT64_C(0x9e3779b97f4a7c15)+(unsigned)control));
    for(int i=0;i<256;i++){
        v=_mm256_add_epi64(_mm256_xor_si256(v,salt),_mm256_set1_epi64x((long long)(i+control*271)));
        v=_mm256_xor_si256(v,_mm256_slli_epi64(v,13));
        v=_mm256_add_epi64(v,_mm256_srli_epi64(v,7));
    }
    uint64_t r[4];_mm256_storeu_si256((__m256i*)r,v);
    return r[0]^r[1]^r[2]^r[3];
}
int void_cpu_feedback(uint64_t ticket,int control,uint64_t *checksum,uint64_t *tsc_ticks){
    if(!checksum||!tsc_ticks||(control!=0&&control!=1))return -1;
    __builtin_cpu_init();if(!__builtin_cpu_supports("avx2"))return -2;
    unsigned aux=0;_mm_lfence();uint64_t t0=__rdtscp(&aux);_mm_lfence();
    uint64_t v=run_avx2(ticket,control);
    _mm_lfence();uint64_t t1=__rdtscp(&aux);_mm_lfence();
    if(t1<t0)return -3;
    *checksum=v;*tsc_ticks=t1-t0;return 0;
}
#else
int void_cpu_feedback(uint64_t ticket,int control,uint64_t *checksum,uint64_t *tsc_ticks){
    (void)ticket;(void)control;(void)checksum;(void)tsc_ticks;
    return -2;  /* CPU-specific driver refuses absent AVX2 hardware. */
}
#endif
