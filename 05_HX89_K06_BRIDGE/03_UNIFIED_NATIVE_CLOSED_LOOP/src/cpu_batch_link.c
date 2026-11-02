/* Reuse EXACT native batch source: cache pointer chase, scalar, AVX2, RDTSCP
 * and instruction-targeted RDRAND/RDSEED remain in the archived harness.
 * Only the CLI main is excluded; deterministic native buffers are managed here.
 * RDRAND/RDSEED values never enter reproducibility hashes. */
#define VOID_BATCH_LIBRARY 1
#include "../../../03_CPU_NATIVE/06_CPU_BATCH_TARGETED_INTRINSICS/cpu_batch.c"

static uint64_t *batch_small;
static uint32_t *batch_links;
static uint32_t batch_position;
int void_batch_init(void){
    __builtin_cpu_init();
    if(!__builtin_cpu_supports("avx2"))return -2;
    unsigned a,b,c,d;
    if(!__get_cpuid(0x80000001u,&a,&b,&c,&d) || !(d&(1u<<27)))return -2;
    if(batch_small || batch_links)return -1;
    if(posix_memalign((void**)&batch_small,64,SMALL_WORDS*sizeof(uint64_t)) ||
       posix_memalign((void**)&batch_links,64,PROBE_WORDS*sizeof(uint32_t))){
        free(batch_small);free(batch_links);batch_small=NULL;batch_links=NULL;return -3;
    }
    uint64_t rng=UINT64_C(0x87b9dc3814c27d05);
    for(size_t i=0;i<SMALL_WORDS;i++)batch_small[i]=mix(&rng);
    init_links(batch_links);batch_position=0;return 0;
}
void void_batch_close(void){
    free(batch_small);free(batch_links);batch_small=NULL;batch_links=NULL;batch_position=0;
}
int void_batch_step(int selection,uint64_t previous_digest,int epoch,
                    uint64_t *work_digest,uint64_t *work_ticks,uint64_t *cache_ticks,
                    int *rdrand_status,int *rdseed_status){
    if(!batch_small||!batch_links||!work_digest||!work_ticks||!cache_ticks||!rdrand_status||!rdseed_status||
       epoch<0||(selection!=0&&selection!=1))return -1;
    /* Materialize previous CPU state as a real dependency in native memory.
     * This word is subsequently consumed by scalar or vector instructions. */
    batch_small[((size_t)epoch*4u)%SMALL_WORDS]^=previous_digest;
    unsigned beforeaux=0,afteraux=0;
    uint64_t before=ticks(&beforeaux);
    uint64_t value;
    if(selection==0)value=scalar(batch_small,SMALL_WORDS,1);
    else if(__builtin_cpu_supports("avx512f") && epoch%4==3)
        value=simd5(batch_small,SMALL_WORDS,1);
    else value=simd2(batch_small,SMALL_WORDS,1);
    uint64_t after=ticks(&afteraux);
    unsigned p0=0,p1=0;
    uint64_t latency=probe(batch_links,&p0,&p1,&batch_position);
    if(after<before)return -4;
    /* ISA entropy is recorded as provenance only: never injected into the
     * deterministic control state, trajectory or work digest. */
    unsigned long long random_sample=0,seed_sample=0;
    *rdrand_status=__builtin_cpu_supports("rdrnd") ? void_try_rdrand64(&random_sample) : 0;
    *rdseed_status=__builtin_cpu_supports("rdseed") ? void_try_rdseed64(&seed_sample) : 0;
    observable_sink ^= (uint64_t)random_sample ^ (uint64_t)seed_sample;
    *work_digest=value;*work_ticks=after-before;*cache_ticks=latency;
    return 0;
}
