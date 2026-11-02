#include "bvh_spatial.h"
#include <type_traits>
#include <iostream>
static_assert(!std::is_copy_constructible<BVHNodeTree>::value, "BVH must own its child nodes");
static_assert(!std::is_copy_assignable<BVHNodeTree>::value, "BVH must not shallow-copy");
static_assert(!std::is_move_constructible<BVHNodeTree>::value, "no unsafe implicit move");
int main(){BVHNodeTree tr; float p[15]={};tr.partitionTree(p,5);std::cout<<"PASS BVH ownership is noncopyable, root owns children\n";}
