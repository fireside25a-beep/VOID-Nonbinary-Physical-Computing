/* Circuit-state observation through the ACTUAL repaired EntropyAVX BVH and
 * procedural geometry code, not an alternative or generated bounding box.
 * The 4x4 geometry is derived from observed K06 charge nodes and the prior
 * native CPU-state digest. The BVH's computed extrema enter the next gate.
 */
#include "../../../03_CPU_NATIVE/05_ENTROPY_AVX_HARDENED/bvh_spatial.h"
#include "../../../03_CPU_NATIVE/05_ENTROPY_AVX_HARDENED/procedural.h"
#include <vector>
#include <cmath>
#include <cstdint>
#include <exception>
#include <limits>
extern "C" int void_entropy_bvh_observe(double charge_a,double charge_b,
                                         uint64_t cpu_digest,double bounds[6]) {
    if(!bounds||!std::isfinite(charge_a)||!std::isfinite(charge_b)||
       charge_a < -2 || charge_a > 2 || charge_b < -2 || charge_b > 2) return -1;
    try {
        const uint32_t seed=static_cast<uint32_t>(cpu_digest ^ (cpu_digest>>32));
        HighEntropyTerrain terrain(seed);
        std::vector<float> xyz(4*4*3);
        std::vector<int> triangles;
        const float phase=static_cast<float>(charge_a * 1.5 + charge_b * 0.75);
        terrain.generateProceduralGrid(xyz.data(),triangles,4,phase);
        if(triangles.size()!=54)return -2;
        /* Map source-derived analog values to terrain elevation. The adapter
         * does not mutate the archived geometry generator implementation. */
        for (int i=0;i<16;i++)
            xyz[3*i+1]+=static_cast<float>((i%4) * charge_a / 10.0 + (i/4) * charge_b / 10.0);
        BVHNodeTree actual_tree;
        actual_tree.partitionTree(xyz.data(),16);
        auto box=actual_tree.nodeAABB;
        const double ext[6]={box.minX,box.minY,box.minZ,box.maxX,box.maxY,box.maxZ};
        for(int j=0;j<6;j++){
            if(!std::isfinite(ext[j]))return -3;
            bounds[j]=ext[j];
        }
        if(bounds[0]>bounds[3] || bounds[1]>bounds[4] || bounds[2]>bounds[5])return -4;
        return 0;
    }catch(const std::exception&){return -5;}
}
