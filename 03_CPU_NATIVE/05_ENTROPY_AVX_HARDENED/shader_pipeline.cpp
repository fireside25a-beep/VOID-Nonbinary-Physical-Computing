#include "shader_pipeline.h"
void AVX2ShaderPipeline::executeVectorTransform(const SIMDVertexPack& input, SIMDVertexPack& output, float sinA, float cosA) {
#if defined(__AVX2__) || defined(__x86_64__)
    __m256 cosVector = _mm256_set1_ps(cosA);
    __m256 sinVector = _mm256_set1_ps(sinA);
    __m256 zOffset = _mm256_set1_ps(3.2f);
    __m256 xIn = _mm256_load_ps(input.x);
    __m256 yIn = _mm256_load_ps(input.y);
    __m256 zIn = _mm256_load_ps(input.z);
    __m256 xRot = _mm256_sub_ps(_mm256_mul_ps(xIn, cosVector), _mm256_mul_ps(zIn, sinVector));
    __m256 zRot = _mm256_add_ps(_mm256_add_ps(_mm256_mul_ps(xIn, sinVector), _mm256_mul_ps(zIn, cosVector)), zOffset);
    _mm256_store_ps(output.x, xRot);
    _mm256_store_ps(output.y, yIn);
    _mm256_store_ps(output.z, zRot);
#else
    for (int i = 0; i < 8; ++i) {
        output.x[i] = input.x[i] * cosA - input.z[i] * sinA;
        output.y[i] = input.y[i];
        output.z[i] = input.x[i] * sinA + input.z[i] * cosA + 3.2f;
    }
#endif
}
