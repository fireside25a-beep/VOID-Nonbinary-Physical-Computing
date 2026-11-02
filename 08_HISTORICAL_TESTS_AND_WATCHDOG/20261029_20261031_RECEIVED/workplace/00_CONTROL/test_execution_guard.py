#!/usr/bin/env python3
"""Real kernel flock subprocess integration tests for native verifier exclusivity."""
import os
import subprocess
import sys
from pathlib import Path
import execution_guard

SELF = Path(__file__).resolve().parent
PYTHON=sys.executable

with execution_guard.exclusive() as fd:
    reject=subprocess.run([PYTHON,'-c',
        'import sys;sys.path.insert(0,sys.argv[1]);import execution_guard;\n'
        'try:\n with execution_guard.exclusive():pass\n'
        'except RuntimeError:sys.exit(23)\n'
        'sys.exit(0)',str(SELF)],capture_output=True,text=True,timeout=5)
    assert reject.returncode == 23, ('concurrent execution not refused', reject.returncode, reject.stderr)
    print('PASS real concurrent verifier blocked')
    inherit=subprocess.run([PYTHON,'-c',
        'import sys;sys.path.insert(0,sys.argv[1]);import execution_guard;\n'
        'with execution_guard.exclusive(inherited_fd=int(sys.argv[2])): print("NESTED PASS")',
        str(SELF),str(fd)],pass_fds=(fd,),capture_output=True,text=True,timeout=5)
    assert inherit.returncode == 0 and 'NESTED PASS' in inherit.stdout, (inherit.returncode,inherit.stderr)
    print('PASS nested watchdog receives live owner lock')
with execution_guard.exclusive():
    print('PASS lock released cleanly for next full-machine invocation')
