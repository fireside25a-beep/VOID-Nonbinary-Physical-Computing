/* Native machine contract: selected modes mutate the CPU-work array, not just labels. */
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>
int void_cpu_cycle_init(void);
int void_cpu_cycle_execute(int,int,int64_t*,int64_t*,int*);
#define CHECK(c,m) do{if(!(c)){fprintf(stderr,"FAIL: %s\n",m);return 1;}checks++;}while(0)
int main(void){
  int checks=0,migrate=0;int64_t digest=0,ticks=0,baseline=0,scalar=0,vector=0;
  CHECK(void_cpu_cycle_execute(0,0,&digest,&ticks,&migrate)==-3,"refuse uninitialized");
  CHECK(void_cpu_cycle_init()==0,"real CPU supports AVX2/RDTSCP");
  CHECK(void_cpu_cycle_execute(-1,0,&digest,&ticks,&migrate)==-3,"reject invalid selector");
  CHECK(void_cpu_cycle_execute(2,0,&digest,&ticks,&migrate)==-3,"reject selector 2");
  CHECK(void_cpu_cycle_execute(0,-1,&digest,&ticks,&migrate)==-3,"reject negative epoch");
  CHECK(void_cpu_cycle_execute(0,0,0,&ticks,&migrate)==-3,"reject NULL digest");
  CHECK(void_cpu_cycle_execute(0,0,&digest,0,&migrate)==-3,"reject NULL ticks");
  CHECK(void_cpu_cycle_execute(0,0,&digest,&ticks,0)==-3,"reject NULL migration");
  CHECK(void_cpu_cycle_execute(0,0,&scalar,&ticks,&migrate)==0 && ticks>0,"real scalar CPU work");
  CHECK(void_cpu_cycle_init()==0,"reseed deterministic real state");
  CHECK(void_cpu_cycle_execute(1,0,&vector,&ticks,&migrate)==0 && ticks>0,"real AVX2 CPU work");
  CHECK(scalar!=vector,"different CPU work state, no selector in hash");
  CHECK(void_cpu_cycle_init()==0,"reseed deterministic rerun");
  CHECK(void_cpu_cycle_execute(0,0,&baseline,&ticks,&migrate)==0 && baseline==scalar,"same native scalar state digest");
  CHECK(void_cpu_cycle_init()==0,"reseed deterministic AVX2 rerun");
  CHECK(void_cpu_cycle_execute(1,0,&baseline,&ticks,&migrate)==0 && baseline==vector,"same native vector state digest");
  printf("PASS native_cpu_state_contract checks=%d scalar=%" PRId64 " vector=%" PRId64 "\n",checks,scalar,vector);
  return 0;
}
