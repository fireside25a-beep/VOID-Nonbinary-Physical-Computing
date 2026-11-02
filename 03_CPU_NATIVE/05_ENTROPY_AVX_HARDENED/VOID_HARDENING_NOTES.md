# VOID EntropyAVX hardened derivative — 2026-11-02

Derived from `03_CPU_NATIVE/02_ENTROPY_AVX_REPAIRED_DERIVATIVE`, which remains unmodified.
Only code changes: `bvh_spatial.h` explicitly deletes copying/moving of the raw-pointer child-owner tree, and `CMakeLists.txt` removes CPU-dependent `-march=native` and `-ffast-math`, instead requiring x86 and baseline AVX2. `test_bvh_ownership.cpp` exercises compile-time ownership contracts. No claim of novel CPU instructions or analog hardware. Runtime BVH and engine tests required before approval.
