#include "bvh_spatial.h"
#include <vector>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <cstdint>
int main(){
  uint32_t s=0x913af72u;
  for(int n=1;n<=1001;++n){
    std::vector<float> p(n*3);
    for(int pass=0;pass<3;++pass){
      float mi[3]={INFINITY,INFINITY,INFINITY}, ma[3]={-INFINITY,-INFINITY,-INFINITY};
      for(int i=0;i<n*3;++i){s=s*1664525u+1013904223u;p[i]=float(int32_t(s))/4194304.f;
        int j=i%3;mi[j]=std::min(mi[j],p[i]);ma[j]=std::max(ma[j],p[i]);}
      BVHNodeTree tr;tr.partitionTree(p.data(),n);
      const auto &b=tr.nodeAABB;
      if(b.minX!=mi[0]||b.maxX!=ma[0]||b.minY!=mi[1]||b.maxY!=ma[1]||b.minZ!=mi[2]||b.maxZ!=ma[2])return 1;
      for(int j=0;j<n*3;j++) p[j]*=.5f;
      tr.refitAsynchronousTree(p.data());
      for(int j=0;j<3;j++){mi[j]*=.5f;ma[j]*=.5f;}
      const auto &c=tr.nodeAABB;
      if(c.minX!=mi[0]||c.maxX!=ma[0]||c.minY!=mi[1]||c.maxY!=ma[1]||c.minZ!=mi[2]||c.maxZ!=ma[2])return 2;
    }
  }
  BVHNodeTree empty;
  try{empty.partitionTree(nullptr,0);return 3;}catch(const std::invalid_argument&){}
  std::cout << "PASS BVH extended: 1001 sizes x 3 passes, 3003 builds and refits, negative null test\n";
}
