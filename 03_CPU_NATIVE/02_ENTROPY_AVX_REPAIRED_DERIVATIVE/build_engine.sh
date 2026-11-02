#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
cmake -S . -B build_workspace_cache -DCMAKE_BUILD_TYPE=Release
cmake --build build_workspace_cache --config Release
exec python3 microkernel.py
