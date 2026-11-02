#ifndef BVH_SPATIAL_H
#define BVH_SPATIAL_H
#include <vector>
struct BoundingBoxAABB {
    float minX, minY, minZ;
    float maxX, maxY, maxZ;
};
class BVHNodeTree {
public:
    BoundingBoxAABB nodeAABB;
    BVHNodeTree* leftBranch;
    BVHNodeTree* rightBranch;
    std::vector<int> elementIndices;
    bool isLeafNode;
    BVHNodeTree();
    ~BVHNodeTree();
    // Owns child nodes; implicit copying would double-delete children.
    BVHNodeTree(const BVHNodeTree&) = delete;
    BVHNodeTree& operator=(const BVHNodeTree&) = delete;
    BVHNodeTree(BVHNodeTree&&) = delete;
    BVHNodeTree& operator=(BVHNodeTree&&) = delete;
    void partitionTree(const float* interleavedPositions, int totalVertices);
    void refitAsynchronousTree(const float* interleavedPositions);
};
#endif
