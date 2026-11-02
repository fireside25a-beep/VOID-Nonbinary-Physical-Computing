#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <sched.h>
#include <errno.h>
#include <string.h>
#include <x86intrin.h>
/* Non-destructive processor power/thermal timing *candidate* experiment.
 * Same fixed readout kernel after short AVX2 activity vs equivalent idle wait.
 * This records real TSC/monotonic timings, NOT die temperature or analog voltage.
 * Cache, CPU scheduler, branch predictors, DVFS and KVM are confounders.
 */
static volatile uint64_t output_sink;
static uint64_t ns(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC_RAW,&t);return (uint64_t)t.tv_sec*1000000000ULL+(uint64_t)t.tv_nsec;}
static uint64_t random_state=0xe9f27a1864d30bc5ULL;
static unsigned random_bit(void){random_state ^= random_state<<13;random_state ^= random_state>>7;random_state ^= random_state<<17;return (unsigned)(random_state&1);}
static void wait_idle(uint64_t duration){uint64_t start=ns();while(ns()-start<duration){struct timespec t={0,500000};nanosleep(&t,NULL);}}
__attribute__((target("avx2,fma"))) static void work_avx(uint64_t duration){
  uint64_t start=ns();__m256 x=_mm256_set1_ps(0.751f),y=_mm256_set1_ps(1.000001f),z=_mm256_set1_ps(0.001f);
  do {
    for(int j=0;j<2048;j++){
      x=_mm256_fmadd_ps(x,y,z);
      y=_mm256_add_ps(y,_mm256_set1_ps(0.00000001f));
    }
  }while(ns()-start<duration);
  float items[8];_mm256_storeu_ps(items,x);output_sink+=(uint64_t)(items[1]*1000.f);
}
static uint64_t same_probe(uint64_t *elapsed_ns,unsigned *aux){
  unsigned a,b;uint64_t t0=ns(),c0=__rdtscp(&a);
  uint64_t s=0xf0e1d2c3b4a59687ULL;
  for(unsigned i=0;i<20000;i++){s^=s<<9;s^=s>>11;s*=0x2545F4914F6CDD1DULL;__asm__ __volatile__("" : "+r"(s) :: "memory");}
  uint64_t c1=__rdtscp(&b),t1=ns();output_sink^=s;
  *elapsed_ns=t1-t0;*aux=(a==b)?a:999999;return c1-c0;
}
int main(int argc,char **argv){
  if(argc!=3){fputs("usage: power_response TRIALS OUTPUT_CSV (8..200)\n",stderr);return 2;}
  char *end=NULL;long n=strtol(argv[1],&end,10);if(!end||*end||n<8||n>200){fputs("invalid count\n",stderr);return 2;}
  cpu_set_t set;CPU_ZERO(&set);if(sched_getaffinity(0,sizeof(set),&set)){perror("affinity read");return 3;}
  int pinned=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&set)){pinned=i;break;}
  if(pinned<0){fputs("no allowed CPU\n",stderr);return 3;}
  CPU_ZERO(&set);CPU_SET(pinned,&set);if(sched_setaffinity(0,sizeof(set),&set)){perror("affinity pin");return 3;}
  FILE *f=fopen(argv[2],"w");if(!f){perror("open");return 3;}
  fprintf(f,"trial,order,after_busy_tsc,after_idle_tsc,after_busy_ns,after_idle_ns,busy_duration_ns,idle_duration_ns,aux_busy,aux_idle,pinned_cpu\n");
  const uint64_t duration=3000000ULL;
  for(long i=0;i<n;i++){
    unsigned a=0,b=0,o=random_bit();uint64_t x=0,y=0,xns=0,yns=0,ht=0,it=0;
    for(unsigned s=0;s<2;s++){
      unsigned busy=(s==0)?(o==0):(o!=0);
      uint64_t t=ns();
      if(busy){work_avx(duration);ht=ns()-t;x=same_probe(&xns,&a);}
      else {wait_idle(duration);it=ns()-t;y=same_probe(&yns,&b);}
    }
    fprintf(f,"%ld,%u,%llu,%llu,%llu,%llu,%llu,%llu,%u,%u,%d\n",i,o,
      (unsigned long long)x,(unsigned long long)y,(unsigned long long)xns,
      (unsigned long long)yns,(unsigned long long)ht,(unsigned long long)it,a,b,pinned);
  }
  if(fclose(f)){perror("close");return 3;}
  printf("EXECUTED real native busy/idle crossover trials=%ld pinned_cpu=%d checksum=%llu\n",n,pinned,(unsigned long long)output_sink);
  return 0;
}
