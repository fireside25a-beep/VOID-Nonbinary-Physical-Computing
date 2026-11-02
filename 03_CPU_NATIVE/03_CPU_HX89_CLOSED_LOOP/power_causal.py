"""Full-machine CPU power/thermal timing candidate. Not a die-temperature claim."""
import csv,hashlib,statistics,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'power_response.c';EXEC=HERE/'power_response'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def compile_native():
    r=subprocess.run(['gcc','-std=c11','-O2','-Wall','-Wextra','-Werror','-o',str(EXEC),str(SOURCE)],capture_output=True,text=True,timeout=35)
    if r.returncode:raise RuntimeError('Native power candidate compile failed: '+r.stderr[-500:])
    return sha(SOURCE),sha(EXEC)
def inspect(path,count):
    with Path(path).open(newline='') as f: rows=list(csv.DictReader(f))
    if len(rows)!=count:raise ValueError('Missing candidate power readings')
    vals=[];orders=[0,0];cpu=None;drifts=[]
    for i,r in enumerate(rows):
        a={k:int(v) for k,v in r.items()}
        if a['trial']!=i or a['order'] not in (0,1):raise ValueError('Invalid trial order')
        if min(a[k] for k in ('after_busy_tsc','after_idle_tsc','after_busy_ns','after_idle_ns','busy_duration_ns','idle_duration_ns'))<=0:raise ValueError('Invalid real timing')
        if a['aux_busy']!=a['aux_idle'] or a['aux_busy']==999999:raise ValueError('Processor migration during timing')
        if cpu is None:cpu=a['pinned_cpu']
        if cpu!=a['pinned_cpu']:raise ValueError('Pinned CPU inconsistency')
        orders[a['order']]+=1
        vals.append(a['after_busy_tsc']-a['after_idle_tsc'])
        drifts.append(a['busy_duration_ns']-a['idle_duration_ns'])
    if min(orders)<count//5:raise ValueError('No randomized crossover comparison')
    d=statistics.median(vals)
    return {'probe_kind':'REAL_X86_AVX2_BUSY_VS_IDLE_WITH_IDENTICAL_NEXT_READOUT',
            'trace_sha256':sha(path),'trials':count,'orders':orders,'pinned_cpu':cpu,
            'busy_minus_idle_median_tsc':d,'busy_slower_fraction':sum(x>0 for x in vals)/count,
            'stimulus_duration_imbalance_median_ns':statistics.median(drifts),
            'timing_result_not_independent_thermometer':True,
            'thermal_or_power_causal_analog_physics_verified':False}
def run_probe(prefix,count=16):
    if not 8<=count<=200:raise ValueError('Invalid physical candidate trial count')
    path=Path(prefix).with_suffix('.power.csv')
    if path.exists():raise FileExistsError('Refusing to overwrite physical candidate evidence')
    if not EXEC.is_file():compile_native()
    p=subprocess.run([str(EXEC),str(count),str(path)],capture_output=True,text=True,timeout=60)
    prefix=Path(prefix)
    prefix.with_suffix('.power.stdout.txt').write_text(p.stdout)
    prefix.with_suffix('.power.stderr.txt').write_text(p.stderr)
    if p.returncode:raise RuntimeError(f'Native power response candidate failed {p.returncode}: {p.stderr[-300:]}')
    d=inspect(path,count)
    d.update({'source_sha256':sha(SOURCE),'native_executable_sha256':sha(EXEC),'stdout_sha256':sha(prefix.with_suffix('.power.stdout.txt')),'stderr_sha256':sha(prefix.with_suffix('.power.stderr.txt'))})
    return d
