#include "bvh_spatial.h"
#include <algorithm>
#include <stdexcept>

BVHNodeTree::BVHNodeTree() : leftBranch(nullptr), rightBranch(nullptr), isLeafNode(true) {
    nodeAABB = {0,0,0,0,0,0};
}
BVHNodeTree::~BVHNodeTree() { delete leftBranch; delete rightBranch; }

// All leaves keep global vertex offsets into the SAME input array. No shifted
// pointers are retained between frames. Tree ownership remains with the root.
static void build_range(BVHNodeTree& node, int start, int count) {
    node.isLeafNode = count <= 4;
    node.elementIndices.clear();
    if (node.isLeafNode) {
        for (int i=0;i<count;++i) node.elementIndices.push_back(start+i);
    } else {
        const int left_count = count/2;
        node.leftBranch = new BVHNodeTree();
        node.rightBranch = new BVHNodeTree();
        build_range(*node.leftBranch,start,left_count);
        build_range(*node.rightBranch,start+left_count,count-left_count);
    }
}
void BVHNodeTree::partitionTree(const float* points, int n) {
    if (!points || n<=0) throw std::invalid_argument("BVH requires nonempty coordinates");
    delete leftBranch; delete rightBranch;
    leftBranch=nullptr; rightBranch=nullptr;
    build_range(*this,0,n);
    refitAsynchronousTree(points);
}
void BVHNodeTree::refitAsynchronousTree(const float* points) {
    if (!points) throw std::invalid_argument("null positions");
    if (isLeafNode) {
        if (elementIndices.empty()) throw std::logic_error("empty BVH leaf");
        const int first=3*elementIndices.front();
        nodeAABB = {points[first],points[first+1],points[first+2],
                    points[first],points[first+1],points[first+2]};
        for (int idx:elementIndices) {
            const int b=3*idx;
            nodeAABB.minX=std::min(nodeAABB.minX,points[b]);
            nodeAABB.minY=std::min(nodeAABB.minY,points[b+1]);
            nodeAABB.minZ=std::min(nodeAABB.minZ,points[b+2]);
            nodeAABB.maxX=std::max(nodeAABB.maxX,points[b]);
            nodeAABB.maxY=std::max(nodeAABB.maxY,points[b+1]);
            nodeAABB.maxZ=std::max(nodeAABB.maxZ,points[b+2]);
        }
    } else {
        if (!leftBranch || !rightBranch) throw std::logic_error("BVH broken tree");
        // Bounded sequential traversal avoids recursively spawning a thread per node.
        leftBranch->refitAsynchronousTree(points);
        rightBranch->refitAsynchronousTree(points);
        const auto& a=leftBranch->nodeAABB;
        const auto& b=rightBranch->nodeAABB;
        nodeAABB = {std::min(a.minX,b.minX),std::min(a.minY,b.minY),std::min(a.minZ,b.minZ),
                    std::max(a.maxX,b.maxX),std::max(a.maxY,b.maxY),std::max(a.maxZ,b.maxZ)};
    }
}
