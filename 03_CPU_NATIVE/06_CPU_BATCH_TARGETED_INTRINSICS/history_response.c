#define _GNU_SOURCE
#include <errno.h>
#include <inttypes.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <x86intrin.h>

/* Real three-intensity randomized-order processor-history experiment.
 * No temperature, power, charge or analog junction readback is asserted.
 * The identical CPU timing probe is performed before and after each
 * intervention. An order-balanced six-permutation block reduces time trends.
 */
static volatile uint64_t observed_sink;
static uint64_t timestamp_ns(void) {
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC_RAW,&t)) { perror("clock_gettime"); exit(3); }
    return (uint64_t)t.tv_sec*1000000000ULL+(uint64_t)t.tv_nsec;
}
static uint64_t rng_state;
static uint64_t next_random(void) {
    rng_state ^= rng_state>>12;
    rng_state ^= rng_state<<25;
    rng_state ^= rng_state>>27;
    return rng_state*UINT64_C(2685821657736338717);
}
static void idle_until(uint64_t deadline) {
    while (timestamp_ns()<deadline) {
        struct timespec t={.tv_sec=0,.tv_nsec=100000};
        if (nanosleep(&t,NULL) && errno!=EINTR) {perror("nanosleep");exit(3);}
    }
}
__attribute__((target("avx2,fma"))) static void cpu_stress_until(uint64_t deadline) {
    __m256 x=_mm256_set1_ps(0.76f), y=_mm256_set1_ps(1.000001f);
    __m256 z=_mm256_set1_ps(0.000001f);
    while (timestamp_ns()<deadline) {
        for (int j=0;j<2048;j++) {
            x=_mm256_fmadd_ps(x,y,z);
            y=_mm256_add_ps(y,z);
        }
    }
    float lanes[8]; _mm256_storeu_ps(lanes,x);
    if (lanes[0]>0.f) observed_sink+=(uint64_t)lanes[0];
}
static uint64_t identical_probe(uint64_t *duration_ns,unsigned *aux_start,unsigned *aux_end) {
    unsigned a,b;
    uint64_t start_ns=timestamp_ns();
    _mm_lfence();
    uint64_t start=__rdtscp(&a);
    uint64_t v=UINT64_C(0xfedcba9876543210);
    for (unsigned j=0;j<16000;j++) {
        v^=v<<7;v^=v>>9;v*=UINT64_C(0x2545f4914f6cdd1d);
        __asm__ __volatile__("" : "+r"(v) :: "memory");
    }
    uint64_t end=__rdtscp(&b);
    _mm_lfence();
    *duration_ns=timestamp_ns()-start_ns;
    *aux_start=a;*aux_end=b;
    observed_sink^=v;
    return end-start;
}
int main(int argc,char **argv) {
    if(argc!=4) {fputs("usage: history_response BLOCKS SEED OUTPUT_CSV (1..24; seed nonzero)\n",stderr);return 2;}
    char *tail=NULL;
    errno=0;long blocks=strtol(argv[1],&tail,10);
    if(errno||!tail||*tail||blocks<1||blocks>24) {fputs("invalid blocks\n",stderr);return 2;}
    errno=0;tail=NULL;
    uint64_t seed=strtoull(argv[2],&tail,0);
    if(errno||!tail||*tail||!seed) {fputs("invalid seed\n",stderr);return 2;}
    rng_state=seed;
    if(!__builtin_cpu_supports("avx2") || !__builtin_cpu_supports("fma")) {
        fputs("Real CPU lacks AVX2/FMA for this experiment\n",stderr);return 4;
    }
    cpu_set_t allowed;CPU_ZERO(&allowed);
    if (sched_getaffinity(0,sizeof(allowed),&allowed)) {perror("sched_getaffinity");return 3;}
    int cpu=-1;
    for (int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&allowed)){cpu=i;break;}
    if(cpu<0){fputs("no allowed CPU\n",stderr);return 3;}
    CPU_ZERO(&allowed);CPU_SET(cpu,&allowed);
    if(sched_setaffinity(0,sizeof(allowed),&allowed)){perror("sched_setaffinity");return 3;}
    FILE *f=fopen(argv[3],"wx");
    if(!f){perror("fopen exclusive");return 3;}
    fprintf(f,"trial,block,position,intensity,previous_intensity,pre_tsc,post_tsc,pre_ns,post_ns,stimulus_ns,active_ns,aux_pre_start,aux_pre_end,aux_post_start,aux_post_end,pinned_cpu,seed\n");
    const unsigned perms[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
    const uint64_t window_ns=5000000ULL;
    long trial=0;
    int prev=-1;
    for(long block=0;block<blocks;block++){
        unsigned order[6]={0,1,2,3,4,5};
        for (int i=5;i>0;i--){unsigned j=(unsigned)(next_random()%(unsigned)(i+1));unsigned t=order[i];order[i]=order[j];order[j]=t;}
        for(int p=0;p<6;p++)for(int k=0;k<3;k++){
            int intensity=(int)perms[order[p]][k];
            uint64_t pre_ns,post_ns;
            unsigned a,b,c,d;
            uint64_t pre=identical_probe(&pre_ns,&a,&b);
            uint64_t start=timestamp_ns(),active=0;
            if(intensity==0) idle_until(start+window_ns);
            else if(intensity==1){
                uint64_t until=start+window_ns/5;
                cpu_stress_until(until);
                active=timestamp_ns()-start;
                idle_until(start+window_ns);
            }else{
                cpu_stress_until(start+window_ns);
                active=timestamp_ns()-start;
            }
            uint64_t duration=timestamp_ns()-start;
            uint64_t post=identical_probe(&post_ns,&c,&d);
            if(a!=b||c!=d||a!=c||a!=(unsigned)cpu){
                /* RDTSCP AUX may not equal linux CPU ID for every kernel;
                 * migration check uses AUX consistency, affinity separately.
                 */
                if(a!=b||c!=d||a!=c){fputs("processor changed during readout\n",stderr);fclose(f);return 5;}
            }
            fprintf(f,"%ld,%ld,%d,%d,%d,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%u,%u,%u,%u,%d,%" PRIu64 "\n",
                    trial,block,p*3+k,intensity,prev,pre,post,pre_ns,post_ns,duration,active,
                    a,b,c,d,cpu,seed);
            prev=intensity;
            trial++;
        }
    }
    if(fclose(f)){perror("fclose");return 3;}
    printf("HISTORY_REAL_EXECUTION trials=%ld blocks=%ld pinned_cpu=%d seed=%" PRIu64 " sink=%" PRIu64 "\n",trial,blocks,cpu,seed,observed_sink);
    return 0;
}
