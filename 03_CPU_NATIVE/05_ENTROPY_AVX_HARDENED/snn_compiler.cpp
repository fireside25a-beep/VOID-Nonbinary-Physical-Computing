#include "snn_compiler.h"
#include <algorithm>
HighPerformanceSNN::HighPerformanceSNN(int totalNeurons) : poolSize(totalNeurons) {
    membranePotentials.resize(totalNeurons, -70000);
    thresholds.resize(totalNeurons, -55000);
    resetPotentials.resize(totalNeurons, -75000);
}
void HighPerformanceSNN::processSpikeTrain(const float* inputBuffer, int* outputSpikeCounts, int batchSize) {
    for (int b = 0; b < batchSize; ++b) {
        int currentInput = static_cast<int>(inputBuffer[b] * 16000.0f);
        int accumulationSpikes = 0;
        for (int step = 0; step < 8; ++step) {
            for (int i = 0; i < poolSize; ++i) {
                membranePotentials[i] += (-(membranePotentials[i] - (-70000)) + currentInput) >> 2;
                if (membranePotentials[i] >= thresholds[i]) {
                    membranePotentials[i] = resetPotentials[i];
                    accumulationSpikes++;
                }
            }
        }
        outputSpikeCounts[b] = accumulationSpikes;
    }
}
