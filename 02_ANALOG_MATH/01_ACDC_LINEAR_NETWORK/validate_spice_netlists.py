#!/usr/bin/env python3
"""Independent nodal checker for the supplied passive R/C + ideal source SPICE netlists.

No third-party modules. This reads the actual .cir files rather than duplicating
weights or expected results. It is not a general SPICE simulator.
"""
import cmath
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent

def val(s):
    s = s.lower()
    for suffix, scale in [('meg', 1e6), ('k', 1e3), ('m', 1e-3), ('u', 1e-6), ('n', 1e-9), ('p', 1e-12)]:
        if s.endswith(suffix):
            return float(s[:-len(suffix)]) * scale
    return float(s)

def parse(filename, mode):
    sources = {'0': 0j}
    elements = []
    for line in (HERE / filename).read_text(encoding='utf-8').splitlines()[1:]:
        line = line.strip()
        if not line or line.startswith(('*', '.')):
            continue
        parts = line.split()
        name, n1, n2 = parts[:3]
        if name[0].lower() == 'v':
            if n2 != '0':
                raise ValueError('Only grounded ideal source supported: ' + line)
            if parts[3].upper() != mode:
                raise ValueError('Wrong source mode: ' + line)
            if mode == 'DC':
                sources[n1] = complex(val(parts[4]), 0)
            else:
                mag = val(parts[4]); angle = math.radians(float(parts[5]))
                sources[n1] = cmath.rect(mag, angle)
        elif name[0].lower() in ('r', 'c'):
            elements.append((name[0].lower(), n1, n2, val(parts[3])))
        else:
            raise ValueError('Unexpected element ' + line)
    return sources, elements

def solve(file, mode, frequency):
    sources, components = parse(file, mode)
    unknowns = sorted({node for _, a, b, _ in components for node in (a,b) if node not in sources})
    dim = len(unknowns)
    A = [[0j for _ in range(dim)] for __ in range(dim)]
    b = [0j for _ in range(dim)]
    indices = {node: i for i, node in enumerate(unknowns)}
    for kind, n1, n2, value in components:
        adm = (1/value) if kind == 'r' else (1j*2*math.pi*frequency*value if mode == 'AC' else 0j)
        for p, q in ((n1, n2), (n2, n1)):
            if p not in indices:
                continue
            i = indices[p]
            A[i][i] += adm
            if q in indices:
                A[i][indices[q]] -= adm
            else:
                b[i] += adm * sources[q]
    # Complex Gaussian elimination with row pivoting.
    for i in range(dim):
        pivot = max(range(i, dim), key=lambda k: abs(A[k][i]))
        if abs(A[pivot][i]) < 1e-30:
            raise ValueError('Floating or disconnected node')
        A[i], A[pivot] = A[pivot], A[i]
        b[i], b[pivot] = b[pivot], b[i]
        for j in range(i+1, dim):
            ratio = A[j][i]/A[i][i]
            for k in range(i,dim):
                A[j][k] -= ratio * A[i][k]
            b[j] -= ratio * b[i]
    x = [0j] * dim
    for i in range(dim-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j]*x[j] for j in range(i+1,dim)))/A[i][i]
    return {n: x[indices[n]] for n in unknowns}

def main():
    rows = list(csv.DictReader((HERE / 'simulation_results.csv').open(encoding='utf-8')))
    cases = [
        ('analog_dc.cir', 'DC', 0.0, 'DC'),
        ('analog_ac.cir', 'AC', 100000.0, 'AC_ideal'),
        ('analog_ac_loaded.cir', 'AC', 100000.0, 'AC_1Mohm_readout'),
    ]
    for netlist, mode, hz, result_mode in cases:
        results = solve(netlist, mode, hz)
        for output in (0,1):
            expected = next(r for r in rows if r['mode']==result_mode
                            and float(r['frequency_hz'])==hz and int(r['output'])==output)
            actual = results['y'+str(output)]
            reported = complex(float(expected['real_v']), float(expected['imag_v']))
            error = abs(actual-reported)
            if error > 1e-10:
                raise AssertionError((netlist, output, actual, reported, error))
            print(f'PASS netlist={netlist} y{output}={actual.real:.12f}{actual.imag:+.12f}j |delta|={error:.3g} V')
    print('PASS: independent circuit-netlist solution agrees with C11 solver')

if __name__=='__main__':
    main()
