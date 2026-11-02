#include "bvh_spatial.h"
#include <algorithm>
#include <future>
BVHNodeTree::BVHNodeTree() : leftBranch(nullptr), rightBranch(nullptr), isLeafNode(true) {}
BVHNodeTree::~BVHNodeTree() { delete leftBranch; delete rightBranch; }
void BVHNodeTree::partitionTree(const float* interleavedPositions, int totalVertices) {
    isLeafNode = true;
    elementIndices.clear();
    for (int i = 0; i < totalVertices; ++i) elementIndices.push_back(i);
    if (totalVertices > 4) {
        isLeafNode = false;
        leftBranch = new BVHNodeTree();
        rightBranch = new BVHNodeTree();
        int splitIndex = totalVertices / 2;
        leftBranch->partitionTree(interleavedPositions, splitIndex);
        rightBranch->partitionTree(interleavedPositions + splitIndex * 3, totalVertices - splitIndex);
    }
    refitAsynchronousTree(interleavedPositions);
}
void BVHNodeTree::refitAsynchronousTree(const float* interleavedPositions) {
    if (isLeafNode) {
        if (elementIndices.empty()) return;
        int firstIdx = elementIndices[0] * 3;
        nodeAABB.minX = interleavedPositions[firstIdx];
        nodeAABB.minY = interleavedPositions[firstIdx+1];
        nodeAABB.minZ = interleavedPositions[firstIdx+2];
        nodeAABB.maxX = nodeAABB.minX; nodeAABB.maxY = nodeAABB.minY; nodeAABB.maxZ = nodeAABB.minZ;
        for (int idx : elementIndices) {
            int base = idx * 3;
            nodeAABB.minX = std::min(nodeAABB.minX, interleavedPositions[base]);
            nodeAABB.minY = std::min(nodeAABB.minY, interleavedPositions[base+1]);
            nodeAABB.minZ = std::min(nodeAABB.minZ, interleavedPositions[base+2]);
            nodeAABB.maxX = std::max(nodeAABB.maxX, interleavedPositions[base]);
            nodeAABB.maxY = std::max(nodeAABB.maxY, interleavedPositions[base+1]);
            nodeAABB.maxZ = std::max(nodeAABB.maxZ, interleavedPositions[base+2]);
        }
    } else {
        auto branchL = std::async(std::launch::async, &BVHNodeTree::refitAsynchronousTree, leftBranch, interleavedPositions);
        auto branchR = std::async(std::launch::async, &BVHNodeTree::refitAsynchronousTree, rightBranch, interleavedPositions);
        branchL.wait(); branchR.wait();
        nodeAABB.minX = std::min(leftBranch->nodeAABB.minX, rightBranch->nodeAABB.minX);
        nodeAABB.minY = std::min(leftBranch->nodeAABB.minY, rightBranch->nodeAABB.minY);
        nodeAABB.minZ = std::min(leftBranch->nodeAABB.minZ, rightBranch->nodeAABB.minZ);
        nodeAABB.maxX = std::max(leftBranch->nodeAABB.maxX, rightBranch->nodeAABB.maxX);
        nodeAABB.maxY = std::max(leftBranch->nodeAABB.maxY, rightBranch->nodeAABB.maxY);
        nodeAABB.maxZ = std::max(leftBranch->nodeAABB.maxZ, rightBranch->nodeAABB.maxZ);
    }
}
