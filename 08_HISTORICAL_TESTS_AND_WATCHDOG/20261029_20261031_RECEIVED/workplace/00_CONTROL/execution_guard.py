#!/usr/bin/env python3
"""Process-level exclusive guard for VOID/HX89 native verification.

One whole-machine or standalone watchdog at a time. Nested watchdogs inherit
only an already locked descriptor; no independent lock that would deadlock.
This guards shared *build outputs* and native measurements, not the physics.
"""
from contextlib import contextmanager
from pathlib import Path
import fcntl
import os

LOCK_PATH = Path(__file__).resolve().parent / '.native_execution_exclusive.lock'

@contextmanager
def exclusive(inherited_fd=None):
    if inherited_fd is not None:
        fd = int(inherited_fd)
        if fd < 3 or os.fstat(fd).st_ino != LOCK_PATH.stat().st_ino:
            raise RuntimeError('Refusing invalid inherited native-run guard')
        yield fd
        return
    with LOCK_PATH.open('a+b') as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('A VOID native verification run owns the shared build lock; refusing concurrent execution') from exc
        try:
            yield f.fileno()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
