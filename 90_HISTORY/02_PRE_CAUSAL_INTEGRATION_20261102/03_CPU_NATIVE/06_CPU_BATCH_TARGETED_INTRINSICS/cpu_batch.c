/* Native CPU intervention experiment. SIMD lanes run simultaneously within hardware
 * vector operations. The physical observables here are instruction/timing effects;
 * no raw thermodynamic voltage, on-die entropy state or nonbinary memory is claimed.
 * Source provided as real experimental engineering, not a simulated measurement.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <time.h>
#include <sched.h>
#include <x86intrin.h>
#include <cpuid.h>
#include <errno.h>

#define SMALL_WORDS (32768u)    /* 256 KiB, intended to exercise local cache */
#define LARGE_WORDS (1048576u)  /* 8 MiB, deliberately beyond usual private caches */
#define PROBE_WORDS (8192u)
#define PROBE_STEPS (8192u)
static volatile uint64_t observable_sink;
/* Compile instruction sites with target-specific ISA; runtime CPUID checks remain. */
__attribute__((target("rdrnd"),noinline))
static int void_try_rdrand64(unsigned long long *v){return _rdrand64_step(v);}
__attribute__((target("rdseed"),noinline))
static int void_try_rdseed64(unsigned long long *v){return _rdseed64_step(v);}

static inline uint64_t ticks(unsigned *aux) { _mm_lfence(); uint64_t x=__rdtscp(aux); _mm_lfence(); return x; }
static uint64_t mix(uint64_t *s) {uint64_t x=*s; x^=x>>12; x^=x<<25; x^=x>>27;*s=x;return x*UINT64_C(2685821657736338717);}
static uint64_t scalar(uint64_t *p, size_t n,int times) {
 uint64_t acc=UINT64_C(0x14650fb0739d0383);
 for(int t=0;t<times;t++)for(size_t i=0;i<n;i+=4){acc=(acc ^ p[i])+((acc<<7)|(acc>>57));p[i]=acc;}
 observable_sink=acc;return acc;
}
__attribute__((target("avx2"),noinline))
static uint64_t simd2(uint64_t *p, size_t n,int times){
 __m256i v=_mm256_set1_epi64x(0x123456789ABCDEFLL), salt=_mm256_set1_epi64x(0x009E3779B97F4A7CLL);
 for(int t=0;t<times;t++)for(size_t i=0;i<n;i+=4){
  __m256i x=_mm256_load_si256((const __m256i*)(p+i));
  v=_mm256_add_epi64(_mm256_xor_si256(v,x),salt);
  v=_mm256_xor_si256(v,_mm256_slli_epi64(v,13));
  _mm256_store_si256((__m256i*)(p+i),v);
 }
 uint64_t out[4];_mm256_storeu_si256((__m256i*)out,v);
 uint64_t sum=out[0]^out[1]^out[2]^out[3];observable_sink=sum;return sum;
}
__attribute__((target("avx512f"),noinline))
static uint64_t simd5(uint64_t *p,size_t n,int times){
 __m512i v=_mm512_set1_epi64(0x123456789ABCDEFLL), salt=_mm512_set1_epi64(0x009E3779B97F4A7CLL);
 for(int t=0;t<times;t++)for(size_t i=0;i<n;i+=8){
  __m512i x=_mm512_load_si512((const void*)(p+i));
  v=_mm512_add_epi64(_mm512_xor_si512(v,x),salt);
  v=_mm512_xor_si512(v,_mm512_slli_epi64(v,13));
  _mm512_store_si512((void*)(p+i),v);
 }
 uint64_t out[8];_mm512_storeu_si512((void*)out,v);
 uint64_t sum=0;for(int i=0;i<8;i++)sum^=out[i];observable_sink=sum;return sum;
}
/* Serial dependent indexed load. The physical TSC reading is a counter, not a raw voltage. */
static uint64_t probe(const uint32_t *link, unsigned *auxstart,unsigned *auxend,uint32_t *last){
 uint32_t i=*last;uint64_t t0=ticks(auxstart);
 for(unsigned k=0;k<PROBE_STEPS;k++)i=link[i];
 uint64_t t1=ticks(auxend);*last=i;observable_sink+=i;return t1-t0;
}
static void init_links(uint32_t *a){
 /* One complete permutation as a ring; strictly dependent successive cache accesses. */
 uint32_t *tmp=malloc(PROBE_WORDS*sizeof(uint32_t));if(!tmp){perror("malloc");exit(3);}
 for(uint32_t i=0;i<PROBE_WORDS;i++)tmp[i]=i;
 uint64_t rng=UINT64_C(0x7505c175a3e11e23);
 for(uint32_t i=PROBE_WORDS-1;i>0;i--){uint32_t j=(uint32_t)(mix(&rng)%(i+1));uint32_t z=tmp[j];tmp[j]=tmp[i];tmp[i]=z;}
 for(uint32_t i=0;i<PROBE_WORDS;i++)a[tmp[i]]=tmp[(i+1)%PROBE_WORDS];
 free(tmp);
}
int main(int argc,char**argv){
 int rounds=8,work=12, pin=0, rotate=0;
 for(int a=1;a<argc;a++){
  if(!strcmp(argv[a],"--rounds")&&a+1<argc)rounds=atoi(argv[++a]);
  else if(!strcmp(argv[a],"--work")&&a+1<argc)work=atoi(argv[++a]);
  else if(!strcmp(argv[a],"--pin"))pin=1;
  else if(!strcmp(argv[a],"--rotate")&&a+1<argc)rotate=atoi(argv[++a]);
  else {fprintf(stderr,"usage: cpu_batch [--rounds 1..128] [--work 1..200] [--rotate 0..3] [--pin]\n");return 2;}
 }
 if(rounds<1||rounds>128||work<1||work>200||rotate<0||rotate>3){fprintf(stderr,"bounded argument violation\n");return 2;}
 __builtin_cpu_init();const int avx2=!!__builtin_cpu_supports("avx2"),avx512=!!__builtin_cpu_supports("avx512f");
 if(!avx2){fprintf(stderr,"AVX2 not available: refusing to replace with fake SIMD\n");return 4;}
 unsigned cp_a,cp_b,cp_c,cp_d;
 if(!__get_cpuid(0x80000001u,&cp_a,&cp_b,&cp_c,&cp_d) || !(cp_d&(1u<<27))){fprintf(stderr,"RDTSCP not present: refusing unsupported timing\n");return 4;}
 cpu_set_t mask;int affinity_ok=0,requested_cpu=-1;
 if(pin){
  CPU_ZERO(&mask);if(!sched_getaffinity(0,sizeof(mask),&mask)){
   for(int c=0;c<CPU_SETSIZE;c++)if(CPU_ISSET(c,&mask)){requested_cpu=c;break;}
   if(requested_cpu>=0){CPU_ZERO(&mask);CPU_SET(requested_cpu,&mask);affinity_ok=(sched_setaffinity(0,sizeof(mask),&mask)==0);}
  }
 }
 uint64_t *small=NULL,*large=NULL;uint32_t*links=NULL;
 if(posix_memalign((void**)&small,64,SMALL_WORDS*8)||posix_memalign((void**)&large,64,LARGE_WORDS*8)||posix_memalign((void**)&links,64,PROBE_WORDS*4)){
  fprintf(stderr,"aligned allocation failed\n");return 3;
 }
 uint64_t rng=UINT64_C(0x87b9dc3814c27d05);for(size_t i=0;i<SMALL_WORDS;i++)small[i]=mix(&rng);
 for(size_t i=0;i<LARGE_WORDS;i++)large[i]=mix(&rng);
 init_links(links);
 uint32_t state=0;unsigned a0=0,a1=0;
 /* Explicit warmup: unrecorded, but real native instructions execute. */
 (void)probe(links,&a0,&a1,&state);
 unsigned a,b,c,d;__cpuid(1,a,b,c,d);int hypervisor=!!(c&(1u<<31));
 printf("{\"schema\":\"VOID_CPU_BATCH_V1\",\"type\":\"header\",\"avx2\":true,\"avx512f\":%s,\"hypervisor\":%s,\"rounds\":%d,\"work\":%d,\"controller_rotate\":%d,\"pin_requested\":%s,\"affinity_succeeded\":%s,\"cpu\":%d,\"classification\":\"NATIVE_INSTRUCTION_TIMING_NOT_RAW_ANALOG\"}\n",avx512?"true":"false",hypervisor?"true":"false",rounds,work,rotate,pin?"true":"false",affinity_ok?"true":"false",requested_cpu);
 fflush(stdout);
 /* Deterministic, counterbalanced 8-block Latin schedule; actual observations never synthesized. */
 for(int r=0;r<rounds;r++){
  int modes[4];for(int j=0;j<4;j++){int k=(j+r%4)%4;modes[j]=((r/4)%2)?(3-k):k;}
  for(int q=0;q<4;q++){
   int m=modes[(q+rotate)%4];uint64_t outcome=0;unsigned beforeaux=0,afteraux=0;
   uint64_t pre=probe(links,&a0,&a1,&state);
   uint64_t stim0=ticks(&beforeaux);
   if(m==0)outcome=scalar(small,SMALL_WORDS,work);
   else if(m==1)outcome=simd2(small,SMALL_WORDS,work);
   else if(m==2){if(avx512)outcome=simd5(small,SMALL_WORDS,work);else outcome=simd2(small,SMALL_WORDS,work);}
   else outcome=scalar(large,LARGE_WORDS,work);
   uint64_t stim1=ticks(&afteraux);
   uint64_t post=probe(links,&a0,&a1,&state);
   /* Independent entropy hardware events, not raw thermal noise, explicitly identified. */
   unsigned long long randword=0,seedword=0;int rdro=0,rdse=0;
   if(__builtin_cpu_supports("rdrnd"))rdro=void_try_rdrand64(&randword);
   if(__builtin_cpu_supports("rdseed"))rdse=void_try_rdseed64(&seedword);
   printf("{\"type\":\"trial\",\"round\":%d,\"position\":%d,\"mode\":\"%s\",\"pre_ticks\":%" PRIu64 ",\"stimulus_ticks\":%" PRIu64 ",\"post_ticks\":%" PRIu64 ",\"processor_id_pre\":%u,\"processor_id_post\":%u,\"processor_id_stim_start\":%u,\"processor_id_stim_end\":%u,\"native_checksum\":\"%016" PRIx64 "\",\"rdrand_success\":%s,\"rdseed_success\":%s,\"rdrand_word\":\"%016llx\",\"rdseed_word\":\"%016llx\"}\n",r,q,m==0?"scalar":m==1?"avx2":m==2?(avx512?"avx512":"avx2_fallback"):"large_cache",pre,stim1-stim0,post,a0,a1,beforeaux,afteraux,outcome,rdro?"true":"false",rdse?"true":"false",randword,seedword);
  }
 }
 free(small);free(large);free(links);
 return 0;
}
