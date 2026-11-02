# First-run failure and executed repair

Original call: `python3 -u workplace/00_CONTROL/run_whole_machine.py --cycles 32`.

Original Python traceback terminated before an acceptance manifest:

```text
  File ".../run_whole_machine.py", line 79, in main
    orig={p.name:digest(p) for _,p in wd.PARTS}
AttributeError: 'str' object has no attribute 'name'
```

Cause: `wd.PARTS` consists of `(Path, expected_sha256)` tuples, not `(label, Path)` tuples.

Repair in working copy: change both source-integrity enumerations to `for p,_ in wd.PARTS`.

Independent rerun of full acceptance completed with 9/9 stages and 64 CPU→HX89→CPU cycles. The first failure is not rewritten as PASS. See JSON acceptance, append-only journal and per-stage logs. Original uploaded sources remain untouched.
