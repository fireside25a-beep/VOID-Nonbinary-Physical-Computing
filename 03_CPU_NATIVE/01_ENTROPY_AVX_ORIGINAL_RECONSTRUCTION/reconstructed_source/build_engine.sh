#!/usr/bin/env bash
set -euo pipefail
echo "=========================================================="
echo "      UNIVERSAL GRAPHICS ENGINE AUTOMATED BUILD SYSTEM    "
echo "=========================================================="
mkdir -p build_workspace_cache
cd build_workspace_cache
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
if [ $? -eq 0 ]; then
    echo "[🎉] Compilation Complete! Running engine orchestrator..."
    cd ..
    python3 microkernel.py
else
    echo "[-] Build Failure. Check toolchain dependencies."
fi
