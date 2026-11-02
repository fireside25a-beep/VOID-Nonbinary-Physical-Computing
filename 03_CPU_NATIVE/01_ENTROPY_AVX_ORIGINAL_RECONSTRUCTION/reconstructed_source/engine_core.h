#ifndef ENGINE_CORE_H
#define ENGINE_CORE_H

#include <vector>
#include <string>

struct alignas(32) SIMDVertexPack {
    float x[8];
    float y[8];
    float z[8];
};

class OptimizedSoftwareCanvas {
private:
    int screenWidth;
    int screenHeight;
    std::vector<char> renderBuffer;
    std::vector<float> precisionDepthBuffer;

public:
    OptimizedSoftwareCanvas(int w, int h);
    void clearFrames();
    void renderLineStrip(int x0, int y0, int x1, int y1, float z0, float z1, char glyph);
    void rasterizeInterleavedGeometry(const float* coordBuffer, int totalVerts, const std::vector<int>& indexMaps, char glyph);
    void swapDisplayBuffers() const;
};
#endif
