#ifndef PROCEDURAL_H
#define PROCEDURAL_H
#include <vector>
class HighEntropyTerrain {
private:
    unsigned int initialEntropySeed;
public:
    HighEntropyTerrain(unsigned int seed);
    float evaluateEntropyNoise(float x, float z) const;
    void generateProceduralGrid(float* interleavedOutput, std::vector<int>& indicesOutput, int resolution, float phase) const;
};
#endif
