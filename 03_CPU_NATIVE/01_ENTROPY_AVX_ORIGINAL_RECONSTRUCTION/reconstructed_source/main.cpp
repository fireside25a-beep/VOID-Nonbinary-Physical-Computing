#include "engine_core.h"
#include "snn_compiler.h"
#include "bvh_spatial.h"
#include "procedural.h"
#include "shader_pipeline.h"
#include <vector>
#include <chrono>
#include <thread>
#include <iostream>
#include <cmath>
int main() {
    const int gridRes = 16;
    const int totalVerts = gridRes * gridRes;
    OptimizedSoftwareCanvas engine(90, 38);
    HighPerformanceSNN compilerPool(16);
    HighEntropyTerrain environmentGenerator(4132);
    std::vector<float> rawMeshCoordinates(totalVerts * 3);
    std::vector<float> snnStabilizedCoords(totalVerts * 3);
    std::vector<int> indexMaps;
    environmentGenerator.generateProceduralGrid(rawMeshCoordinates.data(), indexMaps, gridRes, 0.0f);
    BVHNodeTree coreTree;
    coreTree.partitionTree(rawMeshCoordinates.data(), totalVerts);
    float dynamicTimeline = 0.0f;
    for (int frameLoop = 0; frameLoop < 60; ++frameLoop) {
        auto timeStart = std::chrono::high_resolution_clock::now();
        engine.clearFrames();
        environmentGenerator.generateProceduralGrid(rawMeshCoordinates.data(), indexMaps, gridRes, dynamicTimeline);
        coreTree.refitAsynchronousTree(rawMeshCoordinates.data());
        float cosA = std::cos(dynamicTimeline * 0.35f);
        float sinA = std::sin(dynamicTimeline * 0.35f);
        for (int i = 0; i < totalVerts; i += 8) {
            SIMDVertexPack inputPack;
            SIMDVertexPack outputPack;
            for (int k = 0; k < 8; ++k) {
                int baseIdx = (i + k < totalVerts) ? (i + k) * 3 : (totalVerts - 1) * 3;
                inputPack.x[k] = rawMeshCoordinates[baseIdx];
                inputPack.y[k] = rawMeshCoordinates[baseIdx + 1];
                inputPack.z[k] = rawMeshCoordinates[baseIdx + 2];
            }
            AVX2ShaderPipeline::executeVectorTransform(inputPack, outputPack, sinA, cosA);
            for (int k = 0; k < 8; ++k) {
                if (i + k >= totalVerts) break;
                int targetBase = (i + k) * 3;
                float spatialBatch[] = { outputPack.x[k], outputPack.y[k], outputPack.z[k] };
                int compiledSpikeTrain = 0;
                compilerPool.processSpikeTrain(spatialBatch, &compiledSpikeTrain, 1);
                snnStabilizedCoords[targetBase] = (static_cast<float>(compiledSpikeTrain) / 140.0f) * (outputPack.x[k] < 0 ? -1.0f : 1.0f);
                snnStabilizedCoords[targetBase + 1] = (static_cast<float>(compiledSpikeTrain) / 140.0f) * (outputPack.y[k] < 0 ? -1.0f : 1.0f);
                snnStabilizedCoords[targetBase + 2] = (static_cast<float>(compiledSpikeTrain) / 140.0f) + 2.4f;
            }
        }
        engine.rasterizeInterleavedGeometry(snnStabilizedCoords.data(), totalVerts, indexMaps, '#');
        engine.swapDisplayBuffers();
        auto timeEnd = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> executionDelta = timeEnd - timeStart;
        std::cout << "\n============= VECTORIZED AVX2 / SNN CORE ENGINE =============" << std::endl;
        std::cout << " SIMD Lane Core Latency : " << executionDelta.count() << " ms" << std::endl;
        std::cout << " Hardware Output Rate   : " << (1000.0f / executionDelta.count()) << " FPS" << std::endl;
        std::cout << " Active BVH Tree Leaf  : [" << coreTree.nodeAABB.minX << ", " << coreTree.nodeAABB.maxX << "]" << std::endl;
        std::cout << "============================================================" << std::endl;
        dynamicTimeline += 0.08f;
        std::this_thread::sleep_for(std::chrono::milliseconds(33));
    }
    return 0;
}
