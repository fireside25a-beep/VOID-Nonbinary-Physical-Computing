#include "engine_core.h"
#include <iostream>
#include <cmath>
#include <algorithm>
#include <stdexcept>

OptimizedSoftwareCanvas::OptimizedSoftwareCanvas(int w, int h) : screenWidth(w), screenHeight(h) {
    renderBuffer.resize(w * h, ' ');
    precisionDepthBuffer.resize(w * h, 10000.0f);
}

void OptimizedSoftwareCanvas::clearFrames() {
    std::fill(renderBuffer.begin(), renderBuffer.end(), ' ');
    std::fill(precisionDepthBuffer.begin(), precisionDepthBuffer.end(), 10000.0f);
}

void OptimizedSoftwareCanvas::renderLineStrip(int x0, int y0, int x1, int y1, float z0, float z1, char glyph) {
    int dX = std::abs(x1 - x0); int dY = std::abs(y1 - y0);
    int stepX = (x0 < x1) ? 1 : -1; int stepY = (y0 < y1) ? 1 : -1;
    int internalErr = dX - dY;
    int iterationSteps = std::max(dX, dY);
    int currentStep = 0;
    while (true) {
        if (x0 >= 0 && x0 < screenWidth && y0 >= 0 && y0 < screenHeight) {
            int offset = y0 * screenWidth + x0;
            float ratio = (iterationSteps == 0) ? 1.0f : static_cast<float>(currentStep) / iterationSteps;
            float deltaDepth = z0 + ratio * (z1 - z0);
            if (deltaDepth < precisionDepthBuffer[offset]) {
                precisionDepthBuffer[offset] = deltaDepth;
                renderBuffer[offset] = glyph;
            }
        }
        if (x0 == x1 && y0 == y1) break;
        int errorSlope = 2 * internalErr;
        if (errorSlope > -dY) { internalErr -= dY; x0 += stepX; }
        if (errorSlope < dX) { internalErr += dX; y0 += stepY; }
        currentStep++;
    }
}

void OptimizedSoftwareCanvas::rasterizeInterleavedGeometry(const float* coordBuffer, int totalVerts, const std::vector<int>& indexMaps, char glyph) {
    if (!coordBuffer || totalVerts<=0 || indexMaps.size()%3) throw std::invalid_argument("invalid raster geometry");
    for (int idx:indexMaps) if (idx<0 || idx>=totalVerts) throw std::out_of_range("triangle vertex index out of range");
    std::vector<std::pair<int, int>> projectedMap(totalVerts);
    std::vector<float> transformedDepths(totalVerts);
    for (int i = 0; i < totalVerts; ++i) {
        float zVal = coordBuffer[i * 3 + 2];
        if (zVal <= 0.1f) { projectedMap[i] = {-1, -1}; continue; }
        int sX = static_cast<int>(((coordBuffer[i * 3] * 1.5f) / (zVal * 2.3f) + 1.0f) * 0.5f * screenWidth);
        int sY = static_cast<int>((1.0f - (coordBuffer[i * 3 + 1] * 1.5f) / zVal) * 0.5f * screenHeight);
        projectedMap[i] = {sX, sY};
        transformedDepths[i] = zVal;
    }
    for (size_t i = 0; i < indexMaps.size(); i += 3) {
        int i0 = indexMaps[i]; int i1 = indexMaps[i+1]; int i2 = indexMaps[i+2];
        auto p0 = projectedMap[i0]; auto p1 = projectedMap[i1]; auto p2 = projectedMap[i2];
        if (p0.first == -1 || p1.first == -1 || p2.first == -1) continue;
        renderLineStrip(p0.first, p0.second, p1.first, p1.second, transformedDepths[i0], transformedDepths[i1], glyph);
        renderLineStrip(p1.first, p1.second, p2.first, p2.second, transformedDepths[i1], transformedDepths[i2], glyph);
        renderLineStrip(p2.first, p2.second, p0.first, p0.second, transformedDepths[i2], transformedDepths[i0], glyph);
    }
}

void OptimizedSoftwareCanvas::swapDisplayBuffers() const {
    std::cout << "\x1B[2J\x1B[H";
    std::string frameDump = "";
    frameDump.reserve(screenWidth * screenHeight + screenHeight);
    for (int y = 0; y < screenHeight; ++y) {
        frameDump.append(&renderBuffer[y * screenWidth], screenWidth);
        frameDump.push_back('\n');
    }
    std::cout << frameDump << std::flush;
}
