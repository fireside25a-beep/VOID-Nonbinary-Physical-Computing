#ifndef SNN_COMPILER_H
#define SNN_COMPILER_H
#include <vector>
class alignas(64) HighPerformanceSNN {
public:
    std::vector<int> membranePotentials;
    std::vector<int> thresholds;
    std::vector<int> resetPotentials;
    int poolSize;
    HighPerformanceSNN(int totalNeurons);
    void processSpikeTrain(const float* inputBuffer, int* outputSpikeCounts, int batchSize);
};
#endif
