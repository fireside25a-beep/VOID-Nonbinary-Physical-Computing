#!/usr/bin/env python3
"""Real CPU -> HX89 -> next CPU intervention cycle; strict evidence provenance.

Executed native instructions are not claimed to expose raw analog CPU gate voltages.
The HX89 SEARCH output (not an independently computed shadow) chooses the actual
next native program's mode order and computational work factor. This is a real,
bounded, bidirectional host execution/control chain, not a material VOID proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import batch_bridge as base
sys.path.insert(0, str(base.CONN.parent))
import connector

SEARCH = re.compile(r'^SEARCH step=(\d+) head=(\d+) q=(\d+) fitness=(\d+) target=(\d+)$', re.M)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def decode_real_native(stdout: str, rotate: int, work: int) -> tuple[dict, list[dict]]:
    records = [json.loads(x) for x in stdout.splitlines() if x.strip()]
    if len(records) != 5 or records[0].get('type') != 'header':
        raise RuntimeError('Native single-round trace missing or wrong length')
    header, trials = records[0], records[1:]
    if header.get('rounds') != 1 or header.get('controller_rotate') != rotate or header.get('work') != work:
        raise RuntimeError('Native process did not execute requested HX89-derived command')
    if not header.get('affinity_succeeded'):
        raise RuntimeError('Native CPU affinity not established')
    base.analyze(trials, header)
    # Check the *observed* ordered mode sequence. Merely checking the set of
    # labels would accept rearranged/stale traces and break causal provenance.
    modes = ['scalar', 'avx2', 'avx512' if header['avx512f'] else 'avx2_fallback', 'large_cache']
    expected_order = [modes[(position + rotate) % 4] for position in range(4)]
    observed_order = [trial['mode'] for trial in trials]
    if observed_order != expected_order:
        raise RuntimeError('Native ordered CPU interventions differ from executed command')
    if [trial['position'] for trial in trials] != list(range(4)):
        raise RuntimeError('Native trial positions are not contiguous and ordered')
    return header, trials


def decode_real_hx89(stdout: str, target: int) -> dict:
    matches = SEARCH.findall(stdout)
    if not matches:
        raise RuntimeError('Missing/ambiguous HX89 executed SEARCH output')
    # HX89 may execute multiple real SEARCH transitions before its halt.
    # Selecting the last actual transition is essential; the earlier single-step
    # assumption caused the preserved run_12 failure.
    executed = [tuple(map(int, item)) for item in matches]
    if any(step != i + 1 or head != 0 or got_target != target or not 0 <= q < 25 or not 0 <= fitness <= 25
           for i, (step, head, q, fitness, got_target) in enumerate(executed)):
        raise RuntimeError('HX89 actual search state/target mismatch')
    if len(executed) > 100:
        raise RuntimeError('Unexpected unbounded HX89 trajectory')
    step, head, q, fitness, echoed_target = executed[-1]
    return {'step': step, 'head': head, 'q': q, 'fitness': fitness, 'target': echoed_target}


def next_command(hx: dict, base_work: int) -> tuple[int, int]:
    """Actions are derived from observed HX89 execution, not a predicted state."""
    if set(hx) != {'step', 'head', 'q', 'fitness', 'target'}:
        raise RuntimeError('HX89 feedback record is incomplete')
    if not 0 <= hx['q'] < 25 or not 0 <= hx['fitness'] <= 25:
        raise RuntimeError('Invalid executed HX89 control fields')
    return (hx['q'] * 3 + hx['fitness']) % 4, base_work + (hx['q'] + hx['fitness']) % 3


def run(rounds: int, base_work: int, out_dir: Path) -> dict:
    if not 4 <= rounds <= 64 or not 1 <= base_work <= 20:
        raise RuntimeError('Finite native experiment bounds violated')
    out_dir.mkdir(parents=True, exist_ok=True)
    history = base.check_master()
    contract = connector.k06_contract()
    native = connector.native_trace()
    feedback = []
    rotate, work = 0, base_work
    observed_change = 0
    for r in range(rounds):
        requested = {'rotate': rotate, 'work': work}
        p = subprocess.run([str(base.EXEC), '--rounds', '1', '--work', str(work),
                            '--rotate', str(rotate), '--pin'], capture_output=True,
                            text=True, timeout=25, check=False)
        prefix = out_dir / f'round_{r:03d}'
        (prefix.with_suffix('.native.jsonl')).write_text(p.stdout)
        (prefix.with_suffix('.native.stderr.txt')).write_text(p.stderr)
        if p.returncode:
            raise RuntimeError(f'Native CPU executable failed at round {r}: {p.returncode} {p.stderr[-200:]}')
        header, trials = decode_real_native(p.stdout, rotate, work)
        # The actual measured CPU event controls HX89. The HX89 executed SEARCH
        # state then controls the *next* CPU experiment (not a speculative q).
        measured = sum(x['post_ticks'] + x['stimulus_ticks'] for x in trials)
        target = measured % 25
        response = connector.hx_execute(connector.Q2PROGRAM, ('--target-q', str(target)))
        (prefix.with_suffix('.hx89.stdout.txt')).write_text(response['stdout'])
        actual = decode_real_hx89(response['stdout'], target)
        next_rotate, next_work = next_command(actual, base_work)
        if (next_rotate, next_work) != (rotate, work):
            observed_change += 1
        feedback.append({
            'cycle': r, 'requested_cpu_control': requested,
            'observed_cpu_modes_in_order': [x['mode'] for x in trials],
            'native_observed_tsc_ticks_total': measured,
            'native_trial_sha256': digest(prefix.with_suffix('.native.jsonl')),
            'hx89_program_sha256': response['program_sha256'],
            'hx89_semantic_hash': response['semantic_hash'],
            'hx89_execution': actual,
            'hx89_stdout_sha256': digest(prefix.with_suffix('.hx89.stdout.txt')),
            'next_cpu_control_from_executed_hx89': {'rotate': next_rotate, 'work': next_work},
            'processor_id': header['cpu'],
        })
        rotate, work = next_rotate, next_work
    if observed_change == 0:
        raise RuntimeError('HX89 did not change the native CPU command in any cycle')
    # Cross-cycle causal command consistency must be true throughout the actual log.
    for prev, succ in zip(feedback, feedback[1:]):
        if prev['next_cpu_control_from_executed_hx89'] != succ['requested_cpu_control']:
            raise RuntimeError('Feedback chain broken at cycle ' + str(succ['cycle']))
    result = {
        'schema': 'VOID_HX89_NATIVE_BIDIRECTIONAL_FEEDBACK_V1',
        'result': 'EXECUTED_NATIVE_CPU_HX89_CPU_FEEDBACK',
        'physical_nonbinary_material_computation_verified': False,
        'evidence_class': 'HARDWARE_INSTRUCTION_AND_EXECUTED_HX89_DIGITAL_CONTROL',
        'physical_interpretation': 'No direct observation of subthreshold leakage, analog gate charge, or K06 hardware. Not a native nonbinary material operator.',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'cycles': rounds, 'cpu_native_trials': rounds * 4,
        'command_changed_cycles': observed_change,
        'hx89_native_ir': native['native_ir'],
        'hx89_native_result': native['native_result'],
        'history': history, 'k06_contract': contract,
        'source_sha256': digest(Path(__file__)),
        'native_binary_sha256': digest(base.EXEC),
        'hx89_binary_sha256': digest(connector.HX89),
        'feedback': feedback,
    }
    (out_dir / 'BIDIRECTIONAL_EXECUTION.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rounds', type=int, default=8)
    p.add_argument('--base-work', type=int, default=3)
    p.add_argument('--out', type=Path, default=ROOT / '04_TESTS_AND_LOGS/20261029_BIDIRECTIONAL')
    a = p.parse_args()
    result = run(a.rounds, a.base_work, a.out)
    print(json.dumps({'result': result['result'], 'cycles': result['cycles'],
                      'native_trials': result['cpu_native_trials'],
                      'changed_cpu_commands': result['command_changed_cycles'],
                      'evidence': str(a.out / 'BIDIRECTIONAL_EXECUTION.json'),
                      'physical_nonbinary_material_computation_verified': False}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(json.dumps({'result': 'FAIL', 'reason': str(ex)}), file=sys.stderr)
        sys.exit(5)
