#ifndef SHADER_PIPELINE_H
#define SHADER_PIPELINE_H
#include "engine_core.h"
#include <immintrin.h>
class AVX2ShaderPipeline {
public:
    static void executeVectorTransform(const SIMDVertexPack& input, SIMDVertexPack& output, float sinA, float cosA);
};
#endif
