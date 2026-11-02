@echo off
echo ==========================================================
echo       UNIVERSAL GRAPHICS ENGINE AUTOMATED BUILD SYSTEM
echo ==========================================================
mkdir build_workspace_cache 2>nul
cd build_workspace_cache
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
if %ERRORLEVEL% EQU 0 (
    echo [🎉] Compilation Complete! Running engine orchestrator...
    cd ..
    python microkernel.py
) else (
    echo [-] Build Failure. Check toolchain dependencies.
)
pause
