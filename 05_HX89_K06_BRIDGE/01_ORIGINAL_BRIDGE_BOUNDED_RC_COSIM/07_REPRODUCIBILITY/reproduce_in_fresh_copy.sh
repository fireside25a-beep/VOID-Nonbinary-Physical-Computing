#!/bin/sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
COPY="$(mktemp -d "${TMPDIR:-/tmp}/void-hx89-bridge-repro.XXXXXXXX")"
printf 'Preserved release: %s\n' "$ROOT"
printf 'New isolated rerun location: %s\n' "$COPY"
cp -a "$ROOT/." "$COPY/"
cd "$COPY"
python3 01_BRIDGE_CODE/independent_tests.py > 05_TESTS_AND_AUDITS/rerun_unit_tests.log 2>&1
python3 01_BRIDGE_CODE/native_bridge.py > 05_TESTS_AND_AUDITS/rerun_bridge.log 2>&1
python3 01_BRIDGE_CODE/readback_verify.py > 05_TESTS_AND_AUDITS/rerun_readback.log 2>&1
printf 'COMPLETE — rerun outputs: %s\n' "$COPY"
