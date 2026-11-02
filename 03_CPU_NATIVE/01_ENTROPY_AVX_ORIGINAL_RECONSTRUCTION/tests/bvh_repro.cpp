#include "bvh_spatial.h"
#include <iostream>
#include <cmath>
int main() {
    float coords[8 * 3] = {};
    for(int i=0; i<8; ++i) coords[3*i] = float(i);
    BVHNodeTree tree;
    tree.partitionTree(coords,8);
    const bool okay = std::abs(tree.nodeAABB.minX - 0.0f)<0.00001f && std::abs(tree.nodeAABB.maxX - 7.0f)<0.00001f;
    std::cout << "expected bounds [0,7]; built ["<<tree.nodeAABB.minX<<","<<tree.nodeAABB.maxX<<"] => "<<(okay?"PASS":"FAIL")<<"\n";
    tree.refitAsynchronousTree(coords);
    const bool refit_okay = std::abs(tree.nodeAABB.maxX - 7.0f)<0.00001f;
    std::cout << "after refit: ["<<tree.nodeAABB.minX<<","<<tree.nodeAABB.maxX<<"] => "<<(refit_okay?"PASS":"FAIL")<<"\n";
    return (okay&&refit_okay) ? 0 : 1;
}
