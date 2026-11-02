/* Native, fail-closed HX89 process driver. No shell, no emulator, no fabricated traces.
 * C ABI consumed by Fortran; HX89's own executable performs native work.
 * Byte SHA-256 binds runtime to the archived HX89 executable.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <signal.h>
#include <poll.h>
#include <openssl/evp.h>

#define MAX_TRACE 32768
static const char *HX89_DIGEST = "50f0bae4d7ae0536b191cd5710b43a82e5350d4be84aff9d3f30649c8f3bd451";

int void_sha256_matches(const char *filename, const char *expected) {
    FILE *in = fopen(filename, "rb");
    if (!in || !expected || strlen(expected)!=64) { if(in)fclose(in); return 0; }
    EVP_MD_CTX *ctx=EVP_MD_CTX_new(); unsigned char chunk[65536], digest[EVP_MAX_MD_SIZE];
    unsigned n=0; size_t k; char got[65]; int ok=ctx && EVP_DigestInit_ex(ctx,EVP_sha256(),NULL)==1;
    while(ok && (k=fread(chunk,1,sizeof chunk,in))>0) ok=EVP_DigestUpdate(ctx,chunk,k)==1;
    if(ferror(in))ok=0;
    if(ok)ok=EVP_DigestFinal_ex(ctx,digest,&n)==1 && n==32;
    fclose(in); EVP_MD_CTX_free(ctx);
    if(!ok)return 0;
    for(unsigned i=0;i<32;i++)snprintf(got+2*i,3,"%02x",digest[i]);
    got[64]=0; return strcmp(got,expected)==0;
}

static int write_all(int fd,const void *buf,size_t n) {
    const char *p=buf;
    while(n){ssize_t k=write(fd,p,n);if(k<0 && errno==EINTR)continue;if(k<=0)return 0;p+=k;n-=(size_t)k;}
    return 1;
}

/* Return 0 only on complete, consistent native trace.
 * -1 arguments; -2 binary hash; -3 I/O; -4 child; -5 shape; -6 native oracle mismatch.
 */
int void_hx89_evaluate(const char *executable, int a, int b, int *sum, int *bit) {
    if(!executable || !sum || !bit || (a!=0&&a!=1)||(b!=0&&b!=1))return -1;
    if(!void_sha256_matches(executable,HX89_DIGEST))return -2;
    char program[1024];
    int m=snprintf(program,sizeof program,
         "HX87P1\n"
         "# NEW bridge Polyform; no HX89 engine source is included\n"
         "# material ADC inputs charge_A=%d charge_B=%d\n"
         "CELL 0 0 0 0 0 33 3 0 0\n"
         "CELL 1 0 0 0 0 34 %d 0 0\n"
         "CELL 2 0 0 0 0 35 %d 0 0\n"
         "CELL 3 0 0 0 0 35 0 0 0\n"
         "CELL 4 0 0 0 0 23 1 1 0\n"
         "CELL 5 0 0 0 0 1 49 0 0\n"
         "CELL 6 0 0 0 0 0 0 0 0\n"
         "CELL 4 1 0 0 0 1 48 0 0\n"
         "CELL 4 2 0 0 0 0 0 0 0\n", a,b,a,b);
    if(m<=0 || (size_t)m>=sizeof program)return -1;
    char tempfile[]="/tmp/void-hx89-XXXXXXXX";
    int fd=mkstemp(tempfile);
    if(fd<0)return -3;
    int ok=write_all(fd,program,(size_t)m) && close(fd)==0;
    if(!ok){close(fd);unlink(tempfile);return -3;}
    int pfd[2];if(pipe(pfd)){unlink(tempfile);return -3;}
    pid_t pid=fork();
    if(pid<0){close(pfd[0]);close(pfd[1]);unlink(tempfile);return -3;}
    if(pid==0){
       close(pfd[0]);
       if(dup2(pfd[1],STDOUT_FILENO)<0 || dup2(pfd[1],STDERR_FILENO)<0)_exit(126);
       close(pfd[1]);
       execl(executable,executable,"--native",tempfile,"1","1000",(char*)NULL);
       _exit(127);
    }
    close(pfd[1]);char output[MAX_TRACE+1];size_t used=0;int over=0;ssize_t got;
    while(1){
        struct pollfd watch={.fd=pfd[0],.events=POLLIN|POLLHUP};
        int ready=poll(&watch,1,5000);
        if(ready<0 && errno==EINTR)continue;
        if(ready<=0){over=1;break;}
        got=read(pfd[0],output+used,MAX_TRACE-used);
        if(got<0 && errno==EINTR)continue;
        if(got<=0)break;
        used+=(size_t)got;
        if(used==MAX_TRACE){over=1;break;}
    }
    if(over)kill(pid,SIGKILL);
    close(pfd[0]);int status=0;
    if(waitpid(pid,&status,0)!=pid){unlink(tempfile);return -4;}
    unlink(tempfile);
    if(over || got<0 || !WIFEXITED(status) || WEXITSTATUS(status)!=0)return -4;
    output[used]=0;
    if(!strstr(output,"HEXWORLD_ENTER") || !strstr(output,"HX89 seed="))return -5;
    char *res=strstr(output,"NATIVE_ACCEL epoch=1 ir=3 bytes=18 result=");
    char *halt=strstr(output,"HX89 halt steps=");
    if(!res || !halt || strstr(res+1,"NATIVE_ACCEL epoch=")!=NULL)return -5;
    if(strstr(halt+1,"HX89 halt")!=NULL)return -5;
    int linecount=0;for(size_t z=0;z<used;z++)if(output[z]=='\n')linecount++;
    if(linecount!=4 || used<180 || used>320)return -5;
    int native=-1, hbit=-1, steps=-1;
    if(sscanf(res,"NATIVE_ACCEL epoch=1 ir=3 bytes=18 result=%d",&native)!=1)return -5;
    /* Expected native trace starts with 0/1 just before HX89 halt. */
    if(halt==output || (halt[-1]!='0'&&halt[-1]!='1'))return -5;
    hbit=halt[-1]-'0';
    if(sscanf(halt,"HX89 halt steps=%d",&steps)!=1 || steps!=4)return -5;
    if(native!=a+b || hbit!=(native>0))return -6;
    *sum=native; *bit=hbit;return 0;
}
