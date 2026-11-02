# Native CPU batch build-target derivative — 2026-11-02

Exact source origin is `03_CPU_NATIVE/03_CPU_HX89_CLOSED_LOOP`. Only `cpu_batch.c` changes, adding GCC/Clang target-attribute functions for RDRAND/RDSEED intrinsics, leaving run-time CPU support checks in place. Compile with `cc -std=c11 -O2 -Wall -Wextra -Werror cpu_batch.c -o cpu_batch` on Linux x86-64. This remains a digital CPU timing experiment and does not verify substrate-based multilevel computing. On non-x86/Apple Silicon the experiment cannot run natively.
