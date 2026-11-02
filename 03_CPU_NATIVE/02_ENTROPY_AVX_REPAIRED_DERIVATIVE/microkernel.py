#!/usr/bin/env python3
"""Launch the built native binary with correct path and propagate status."""
from pathlib import Path
import os, subprocess, sys
if __name__ == "__main__":
    exe = Path(__file__).resolve().parent / "build_workspace_cache" / ("EntropyAVXEngine.exe" if os.name=="nt" else "EntropyAVXEngine")
    if not exe.is_file():
        print("Native executable missing: " + str(exe), file=sys.stderr)
        sys.exit(2)
    env = dict(os.environ, ISOLATED_AVX2_RUNTIME="TRUE")
    sys.exit(subprocess.run([str(exe)], env=env, check=False).returncode)
