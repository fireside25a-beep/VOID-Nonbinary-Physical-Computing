/* Downstream instrument: source-derived VOID K06 trajectory -> actual repaired
 * EntropyAVX SIMD transform, owning BVH, and raster canvas. Deterministic input.
 * Never invent geometry or read analog voltages from the CPU timing counters.
 */
#include "engine_core.h"
#include "bvh_spatial.h"
#include "shader_pipeline.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

struct Sample { double time, a, b, c; };
static std::vector<std::string> split(const std::string& line) {
    std::vector<std::string> parts;
    std::istringstream in(line);
    for (std::string part; std::getline(in,part,','); ) parts.push_back(part);
    return parts;
}
static double parse(const std::string& s) {
    std::size_t n=0;
    double d=std::stod(s,&n);
    if(n!=s.size() || !std::isfinite(d)) throw std::invalid_argument("nonfinite or malformed trace value");
    return d;
}
int main(int argc,char** argv) {
    try {
        if(argc!=2) throw std::invalid_argument("usage: void_trajectory_renderer K06_trajectory.csv");
        __builtin_cpu_init();
        if(!__builtin_cpu_supports("avx2")) throw std::runtime_error("AVX2 required for EntropyAVX renderer");
        std::ifstream f(argv[1]);
        if(!f) throw std::runtime_error("missing trajectory file");
        std::string line;
        if(!std::getline(f,line) || line!="step,substep,time_s,drive_a_v,drive_b_v,charge_a_v,charge_b_v,charge_c_v,probe_a_v,probe_b_v,energy_j")
            throw std::runtime_error("unexpected source trajectory schema");
        std::vector<Sample> samples;
        while(std::getline(f,line)) {
            if(line.empty()) continue;
            const auto cols=split(line);
            if(cols.size()!=11 || samples.size()>=200000)throw std::runtime_error("malformed or oversized trace");
            Sample s={parse(cols[2]),parse(cols[5]),parse(cols[6]),parse(cols[7])};
            if(!samples.empty() && s.time<=samples.back().time)throw std::runtime_error("non-monotonic time stamps");
            samples.push_back(s);
        }
        if(samples.size()<2)throw std::runtime_error("trace must contain multiple time points");
        const double span=samples.back().time-samples.front().time;
        if(!(span>0))throw std::runtime_error("zero time span");
        const std::size_t n=samples.size();
        std::vector<float> coords(3*n*3);
        std::array<double,3> mn={std::numeric_limits<double>::infinity(),std::numeric_limits<double>::infinity(),std::numeric_limits<double>::infinity()};
        std::array<double,3> mx={-mn[0],-mn[1],-mn[2]};
        for(const auto &s:samples){
            std::array<double,3> vals={s.a,s.b,s.c};
            for(int k=0;k<3;++k){mn[k]=std::min(mn[k],vals[k]);mx[k]=std::max(mx[k],vals[k]);}
        }
        double vscale=0.002;
        for(int k=0;k<3;++k)vscale=std::max(vscale,std::max(std::abs(mn[k]),std::abs(mx[k])));
        /* Eight real voltage/time samples go through EntropyAVX's actual AVX2 shader. */
        for(std::size_t i=0;i<3*n;i+=8) {
            SIMDVertexPack pack{},rendered{};
            for(int j=0;j<8;++j){
                std::size_t p=std::min(i+std::size_t(j),3*n-1);
                std::size_t t=p/3;int c=int(p%3);
                double val=(c==0?samples[t].a:c==1?samples[t].b:samples[t].c);
                pack.x[j]=float(2.0*(samples[t].time-samples.front().time)/span-1.0);
                pack.y[j]=float(val/vscale);
                pack.z[j]=2.0f+float(c)*0.03f;
            }
            AVX2ShaderPipeline::executeVectorTransform(pack,rendered,0.0f,1.0f);
            for(int j=0;j<8 && i+std::size_t(j)<3*n;++j) {
                const auto p=i+std::size_t(j);
                coords[p*3]=rendered.x[j];coords[p*3+1]=rendered.y[j];coords[p*3+2]=rendered.z[j];
            }
        }
        BVHNodeTree tree;
        tree.partitionTree(coords.data(),int(3*n));
        if(tree.nodeAABB.minX>tree.nodeAABB.maxX || tree.nodeAABB.minY>tree.nodeAABB.maxY)
            throw std::runtime_error("BVH geometry invalid");
        OptimizedSoftwareCanvas canvas(100,33);
        canvas.clearFrames();
        for(int c=0;c<3;++c) for(std::size_t i=1;i<n;++i) {
            const float* p=&coords[(3*(i-1)+std::size_t(c))*3];
            const float* q=&coords[(3*i+std::size_t(c))*3];
            auto x0=int(std::lround((p[0]+1.0f)*49.0f)), x1=int(std::lround((q[0]+1.0f)*49.0f));
            auto y0=int(std::lround((1.0f-p[1])*16.0f)), y1=int(std::lround((1.0f-q[1])*16.0f));
            canvas.renderLineStrip(x0,y0,x1,y1,p[2],q[2],"ABC"[c]);
        }
        std::cout<<"VOID_K06_REAL_TRACE_SAMPLES="<<n<<" AVX2=executed BVH=source_derived\n";
        std::cout<<std::setprecision(14)<<"CHARGE_A_RANGE="<<mn[0]<<","<<mx[0]
                 <<" CHARGE_B_RANGE="<<mn[1]<<","<<mx[1]
                 <<" CHARGE_C_RANGE="<<mn[2]<<","<<mx[2]<<"\n";
        std::cout<<"AABB_X="<<tree.nodeAABB.minX<<","<<tree.nodeAABB.maxX<<"\n";
        canvas.swapDisplayBuffers();
        return EXIT_SUCCESS;
    } catch(const std::exception& e) {
        std::cerr<<"VOID_TRACE_RENDER_FAIL: "<<e.what()<<"\n";
        return EXIT_FAILURE;
    }
}
