# EntropyAVXEngine: source-and-runtime audit

## Provenance / scope
This package reconstructs the **15 supplied files** from their contents pasted in the chat (not a filesystem archive submitted by the user). It does NOT claim to be a byte-identical copy of any unpublished original project or Google AI Mode's private browser component. Comment-only differences may exist compared with user originals. The separate `bootstrap_rebuild.py` is an **independent experiment authored during this audit**, NOT a discovered original file.

## What was actually executed
- The pasted `CMakeLists.txt` and 11 C++ header/source entries were rebuilt with GNU C++ on x86_64 AVX2 and linked successfully.
- Native `EntropyAVXEngine` executed all 60 frames in ~2.40s wall time, wrote ANSI clear-screen plus 90x38 printable glyph frames, with 8 distinct frame SHA-256 hashes.
- Median self-reported processing time across 60 frames was approximately 6.292ms (not end-to-end FPS; a 33ms sleep happens afterwards).
- AddressSanitizer+UndefinedBehaviorSanitizer instrumented executable ran 60 frames with zero bytes of stderr output. This does not establish absence of all bugs.
- An independent 8-vertex BVH bounds test fails: expected max X=7, actual max X=3 (the right subtree is refitted against the wrong base pointer).

## Spawn/autobuild trace of supplied code
- `build_engine.sh` **does** create `build_workspace_cache`, from which CMake generates its usual cache, object directory and compiled executable.
- The script reports `Compilation Complete!`, then invokes project-root `microkernel.py`, which looks for an executable in the project root instead of `build_workspace_cache`. Consequently, it prints `Execution signature missing`. The shell still returns exit status zero; this is a false-positive success.
- No `HYPER_SOURCE_FILES` dictionary or any routines that write the C++ source files were found in the supplied 15 files. The screenshot's source-regenerator is a different missing artifact.
- `microkernel.py` is a launcher, not a Python microkernel compute loop; it doesn't create source files.

## Experimental self-spawning proof, separate from original
`bootstrap_rebuild.py` embeds all 15 reconstructed source files as Python strings. It creates an empty destination, writes all source files, can compile them with CMake, and launches the binary from its real build path. In the verification run it emitted 15 source files with no SHA-256 content mismatches, built successfully, and ran all 60 native frames. It explicitly refuses to overwrite a nonempty destination.

Usage:

    python3 bootstrap_rebuild.py /path/to/empty/project --build --run

Requires Python 3, CMake, C++17 compiler, and x86_64 CPU with AVX2 for the source as supplied. The generated project uses `-march=native`, `-ffast-math`, `-mavx2`, which are not portable and do not guarantee deterministic floating-point behavior across targets.

## Additional defects / caveats in supplied source
- The BVH repointer error proven above.
- `main.cpp` passes a three-coordinate buffer to SNN with `batchSize=1`, so only X goes through the spike input; it reuses the one spike result for X/Y/Z output coordinates.
- `std::async(std::launch::async)` recurses into every internal BVH node on every frame and can oversubscribe threads.
- Displayed engine frame processing rate is calculated before a 33ms sleep; not observed end-to-end FPS.
- Text rasterizer's `rasterizeInterleavedGeometry` assumes `indexMaps.size()` divisible by 3 and indices valid; no bounds check.
- Text render output is not the separate colored browser animation in the supplied screenshots.
- The earlier user-pasted `microkernel.py` and `procedural.h` differ from these versions; version identity cannot be inferred from snippets.

## Reproducing the independent BVH failure

    c++ -std=c++17 -Ireconstructed_source tests/bvh_repro.cpp reconstructed_source/bvh_spatial.cpp -pthread -o bvh_repro
    ./bvh_repro

Expected exit status: nonzero and `expected bounds [0,7]; built [0,3] => FAIL`.

## Real vs absent
- VERIFIED: C++ compilation, 60 native text frames, sanitizer-instrumented run, actual source bootstrap proof, and BVH error.
- ABSENT: Google AI Mode's generated UI JavaScript/HTML, a telemetry bridge to native code, original screenshot bootstrap dictionary, and proof Google executed the compiled C++ in-browser.

The Google AI Mode interface can be genuinely interactive because Google Search generative UI can emit HTML, CSS, and JavaScript for execution in the browser (see Google's Generative UI research article, Nov 18 2025). That mechanism is distinct from running the native C++ binary shown in this package.
