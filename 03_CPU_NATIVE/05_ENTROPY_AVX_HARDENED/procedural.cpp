#include "procedural.h"
#include <cmath>
HighEntropyTerrain::HighEntropyTerrain(unsigned int seed) : initialEntropySeed(seed) {}
float HighEntropyTerrain::evaluateEntropyNoise(float x, float z) const {
    float dotProduct = x * 12.9898f + z * 78.233f + static_cast<float>(initialEntropySeed);
    float fractionalPart = std::sin(dotProduct) * 43758.5453f;
    return (fractionalPart - std::floor(fractionalPart));
}
void HighEntropyTerrain::generateProceduralGrid(float* interleavedOutput, std::vector<int>& indicesOutput, int resolution, float phase) const {
    int vIdx = 0;
    for (int z = 0; z < resolution; ++z) {
        for (int x = 0; x < resolution; ++x) {
            float nX = (static_cast<float>(x) / (resolution - 1)) * 2.4f - 1.2f;
            float nZ = (static_cast<float>(z) / (resolution - 1)) * 2.4f - 1.2f;
            float noiseFactor = evaluateEntropyNoise(nX, nZ) * 0.15f;
            float nY = std::sin(nX * 4.0f + phase) * std::cos(nZ * 4.0f + phase) * 0.35f + noiseFactor;
            interleavedOutput[vIdx++] = nX;
            interleavedOutput[vIdx++] = nY;
            interleavedOutput[vIdx++] = nZ;
        }
    }
    indicesOutput.clear();
    for (int z = 0; z < resolution - 1; ++z) {
        for (int x = 0; x < resolution - 1; ++x) {
            int curr = z * resolution + x;
            int next = curr + resolution;
            indicesOutput.push_back(curr); indicesOutput.push_back(next); indicesOutput.push_back(curr + 1);
            indicesOutput.push_back(curr + 1); indicesOutput.push_back(next); indicesOutput.push_back(next + 1);
        }
    }
}
