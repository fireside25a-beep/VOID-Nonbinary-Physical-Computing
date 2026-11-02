/* Independent native ABI smoke/negative tests against the REAL archived HX89 binary. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
int void_hx89_evaluate(const char *, int,int,int *,int *);
int void_sha256_matches(const char *,const char *);
int void_cpu_feedback(uint64_t,int,uint64_t *,uint64_t *);
#define REQUIRE(p,msg) do{if(!(p)){fprintf(stderr,"FAIL %s\n",msg);return 1;}checks++;}while(0)
int main(int argc,char**argv){
 if(argc!=2)return 2;
 int checks=0,s,b;
 for(int a=0;a<=1;a++)for(int c=0;c<=1;c++){
   int err=void_hx89_evaluate(argv[1],a,c,&s,&b);
   REQUIRE(err==0,"native executable actual 4 input combinations");
   REQUIRE(s==a+c && b==(a|c),"HX89 native oracle");
 }
 REQUIRE(void_hx89_evaluate(argv[1],-1,0,&s,&b)==-1,"reject negative ADC");
 REQUIRE(void_hx89_evaluate(argv[1],0,2,&s,&b)==-1,"reject ADC beyond 1");
 REQUIRE(void_hx89_evaluate("/absolutely/no/hx89",0,0,&s,&b)==-2,"missing native executable fail closed");
 REQUIRE(void_sha256_matches(argv[1],"0000000000000000000000000000000000000000000000000000000000000000")==0,"tamper hash rejection");
 uint64_t sum0=0,sum1=0,rep=0,ticks=0;
 REQUIRE(void_cpu_feedback(12345,0,&sum0,&ticks)==0 && ticks>0,"native AVX2 0");
 REQUIRE(void_cpu_feedback(12345,1,&sum1,&ticks)==0 && ticks>0,"native AVX2 1");
 REQUIRE(void_cpu_feedback(12345,0,&rep,&ticks)==0 && sum0==rep,"AVX2 deterministic checksum");
 REQUIRE(sum0!=sum1,"HX89-controlled AVX2 result changes");
 REQUIRE(void_cpu_feedback(12345,2,&rep,&ticks)==-1,"reject invalid control");
 printf("REAL_NATIVE_DRIVER_TESTS_PASS checks=%d outcomes=[%llu,%llu]\n",checks,(unsigned long long)sum0,(unsigned long long)sum1);
 return 0;
}
