/* Strict ingestion of independently collected physical K06 measurements.
 * Compilation uses OpenSSL for SHA-256. This parser never synthesizes telemetry,
 * emulates a device, emits DAC instructions, or accepts missing calibration.
 * Hashes prove file identity, NOT hardware authenticity by themselves.
 */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <math.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>

static const char hdr[]="sample_index,time_ns,instrument_serial,calibration_id,charge_a_v,charge_b_v,charge_c_v,probe_a_v,probe_b_v,write_a_v,write_b_v";
static int digest(const char*path,char out[65]){
    FILE*f=fopen(path,"rb");if(!f)return -1;
    EVP_MD_CTX*ctx=EVP_MD_CTX_new();if(!ctx){fclose(f);return -1;}
    int good=EVP_DigestInit_ex(ctx,EVP_sha256(),NULL)==1;
    unsigned char buf[32768],hash[32];size_t n;unsigned size=0;
    while(good&&(n=fread(buf,1,sizeof buf,f))>0)good=EVP_DigestUpdate(ctx,buf,n)==1;
    if(ferror(f))good=0;
    if(good)good=EVP_DigestFinal_ex(ctx,hash,&size)==1&&size==32;
    EVP_MD_CTX_free(ctx);fclose(f);
    if(!good)return -1;
    for(size_t i=0;i<32;i++)snprintf(out+2*i,3,"%02x",hash[i]);
    out[64]='\0';return 0;
}
static int token_id(const char*s){
    size_t n=strlen(s);if(n<2||n>96)return 0;
    for(size_t i=0;i<n;i++)if(!isalnum((unsigned char)s[i])&&s[i]!='-'&&s[i]!='_'&&s[i]!='.')return 0;
    return 1;
}
static int parseu64(const char*s,uint64_t*v){
    if(!*s||*s=='-'||isspace((unsigned char)*s))return -1;
    char*end=NULL;errno=0;unsigned long long x=strtoull(s,&end,10);
    if(errno||end==s||*end)return -1;
    *v=(uint64_t)x;return 0;
}
static int parsedouble(const char*s,double*v,double bound){
    if(!*s||isspace((unsigned char)*s))return -1;
    char*end=NULL;errno=0;double x=strtod(s,&end);
    if(errno||end==s||*end||!isfinite(x)||fabs(x)>bound)return -1;
    *v=x;return 0;
}
int main(int argc,char**argv){
    if(argc!=3){fprintf(stderr,"usage: void_bench_ingest MEASURED_FILE.csv RECEIPT_FILE.txt\n");return 2;}
    if(!strcmp(argv[1],argv[2])){fputs("REFUSE input/output alias\n",stderr);return 2;}
    FILE*f=fopen(argv[1],"rb");if(!f){perror("REFUSE no acquired bench input");return 3;}
    char*line=NULL;size_t cap=0;ssize_t length=getline(&line,&cap,f);
    if(length<0){fputs("REFUSE missing header\n",stderr);free(line);fclose(f);return 3;}
    while(length>0&&(line[length-1]=='\n'||line[length-1]=='\r'))line[--length]='\0';
    if(strcmp(line,hdr)){fputs("REFUSE exact acquisition schema mismatch\n",stderr);free(line);fclose(f);return 3;}
    uint64_t prev_idx=0,prev_time=0,count=0;char first_serial[97]={0},first_cal[97]={0};
    double minimum[7],maximum[7];for(int i=0;i<7;i++){minimum[i]=INFINITY;maximum[i]=-INFINITY;}
    int good=1;
    while((length=getline(&line,&cap,f))>=0){
        if(length>4096){good=0;break;}
        while(length>0&&(line[length-1]=='\n'||line[length-1]=='\r'))line[--length]='\0';
        if(!length){good=0;break;}
        char*parts[11]={0};size_t fields=0;char*save=NULL;
        for(char*t=strtok_r(line,",",&save);t;t=strtok_r(NULL,",",&save)){
            if(fields>=11){fields=12;break;}
            parts[fields++]=t;
        }
        if(fields!=11){good=0;break;}
        uint64_t idx,time;double volts[7];
        if(parseu64(parts[0],&idx)||parseu64(parts[1],&time)||!token_id(parts[2])||!token_id(parts[3])){good=0;break;}
        if((count&&idx!=prev_idx+1)||(!count&&idx!=0)||(count&&time<=prev_time)||time==0){good=0;break;}
        if(!count){strcpy(first_serial,parts[2]);strcpy(first_cal,parts[3]);}
        if(strcmp(first_serial,parts[2])||strcmp(first_cal,parts[3])){good=0;break;}
        for(int i=0;i<7;i++){
            /* charge ±5V, probes ±12V, protected WRITE pads nominal 0..1.8V */
            double bound=(i<3?5.0:(i<5?12.0:1.8));
            if(parsedouble(parts[4+i],&volts[i],bound)){good=0;break;}
            if(i>=5 && volts[i]<-0.05){good=0;break;}
            if(volts[i]<minimum[i])minimum[i]=volts[i];
            if(volts[i]>maximum[i])maximum[i]=volts[i];
        }
        if(!good)break;
        prev_idx=idx;prev_time=time;count++;
        if(count>20000000){good=0;break;}
    }
    if(ferror(f))good=0;
    free(line);fclose(f);
    if(!good||count<2){fprintf(stderr,"REFUSE invalid or insufficient physical acquisition rows (validated=%llu)\n",(unsigned long long)count);return 4;}
    char sha[65];if(digest(argv[1],sha)){fputs("REFUSE cannot hash physical acquisition\n",stderr);return 5;}
    FILE*out=fopen(argv[2],"wx");if(!out){perror("REFUSE append-only evidence receipt already exists or cannot open");return 6;}
    fprintf(out,"SCHEMA=VOID_PHYSICAL_BENCH_INGEST_V1\nINPUT_SHA256=%s\n",sha);
    fprintf(out,"RECORDS=%llu\nDEVICE_SERIAL=%s\nCALIBRATION_ID=%s\nFIRST_INDEX=0\nLAST_INDEX=%llu\nLAST_TIME_NS=%llu\n",(unsigned long long)count,first_serial,first_cal,(unsigned long long)prev_idx,(unsigned long long)prev_time);
    const char*names[]={"CHARGE_A","CHARGE_B","CHARGE_C","PROBE_A","PROBE_B","WRITE_A","WRITE_B"};
    for(int i=0;i<7;i++)fprintf(out,"MIN_%s=%.17g\nMAX_%s=%.17g\n",names[i],minimum[i],names[i],maximum[i]);
    fputs("CLAIM=VALIDATED_FILE_SCHEMA_AND_HASH_NOT_HARDWARE_AUTHENTICITY\n",out);
    if(fclose(out)){fputs("FAIL receipt write\n",stderr);return 6;}
    printf("BENCH_FILE_ACCEPTED %llu data rows SHA256 %s (hardware authenticity not established by file hash)\n",(unsigned long long)count,sha);
    return 0;
}
