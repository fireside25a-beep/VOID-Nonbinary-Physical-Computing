#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sched.h>
#include <string.h>
#include <errno.h>
#include <x86intrin.h>

/* Real CPU cache coherence experiment. No fabricated analog signal or model.
 * Measurements: TSC ticks for load after in-core warm versus CLFLUSH eviction.
 * Negative control: second warm load vs first warm load.
 * Environment dependent: virtualization and scheduling may confound timing.
 */
static volatile unsigned char sink;
static uint64_t state=0x92a7e545fac39403ULL;
static uint64_t rand64(void){state ^=state<<13;state^=state>>7;state^=state<<17;return state;}
static __attribute__((noinline)) uint64_t load_time(volatile unsigned char *p,unsigned *core){
  unsigned a=0,b=0;_mm_lfence();
  uint64_t t0=__rdtscp(&a);_mm_lfence();
  sink ^= *p;
  _mm_lfence();uint64_t t1=__rdtscp(&b);_mm_lfence();
  if(a!=b){*core=999999;return 0;}
  *core=a;return t1-t0;
}
static uint64_t warm(volatile unsigned char *p,unsigned *c){sink^=*p;_mm_lfence();return load_time(p,c);}
static uint64_t cold(volatile unsigned char *p,unsigned *c){_mm_clflush((const void *)p);_mm_mfence();return load_time(p,c);}
int main(int argc,char **argv){
  if(argc!=3){fprintf(stderr,"usage: cache_causality TRIALS OUTPUT_CSV (200..100000)\n");return 2;}
  char *e=NULL;long n=strtol(argv[1],&e,10);
  if(!e||*e||n<200||n>100000){fputs("invalid trials\n",stderr);return 2;}
  cpu_set_t s; CPU_ZERO(&s);if(sched_getaffinity(0,sizeof(s),&s)!=0){perror("getaffinity");return 3;}
  int pinned=-1;for(int i=0;i<CPU_SETSIZE;i++)if(CPU_ISSET(i,&s)){pinned=i;break;}
  if(pinned<0){fputs("no permitted CPU\n",stderr);return 3;}
  CPU_ZERO(&s);CPU_SET(pinned,&s);if(sched_setaffinity(0,sizeof(s),&s)!=0){perror("setaffinity");return 3;}
  void *mem=NULL;if(posix_memalign(&mem,64,4096)){fputs("memalign fail\n",stderr);return 3;}
  memset(mem,0x5a,4096);volatile unsigned char *p=(volatile unsigned char *)mem;
  FILE *f=fopen(argv[2],"w");if(!f){perror("fopen");free(mem);return 3;}
  fprintf(f,"trial,order,cached_tsc,evicted_tsc,warm_control_tsc,aux_cached,aux_evicted,aux_control,cpu_pinned\n");
  for(long i=0;i<n;i++){
    unsigned ac=0,ae=0,an=0;uint64_t w=0,c=0,k=0;
    unsigned order=(unsigned)(rand64()&1);
    if(order==0){w=warm(p,&ac);c=cold(p,&ae);}else{c=cold(p,&ae);w=warm(p,&ac);}
    k=warm(p,&an);
    fprintf(f,"%ld,%u,%llu,%llu,%llu,%u,%u,%u,%d\n",i,order,
       (unsigned long long)w,(unsigned long long)c,(unsigned long long)k,ac,ae,an,pinned);
  }
  if(fclose(f)!=0){perror("fclose");free(mem);return 3;}
  free(mem);printf("PASS wrote %ld measured paired trials pinned_cpu=%d sink=%u\n",n,pinned,sink);return 0;
}
