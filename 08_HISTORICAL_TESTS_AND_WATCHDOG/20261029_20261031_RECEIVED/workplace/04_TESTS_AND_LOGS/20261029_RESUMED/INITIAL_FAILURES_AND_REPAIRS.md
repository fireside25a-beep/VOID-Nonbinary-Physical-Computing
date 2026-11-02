# Failed first attempts and real repairs — preserved evidence

The following failures occurred in this session before successful reruns. They are not
recast as PASS events. The errors appeared during actual tool execution.

1. First GCC `-Werror` build of new `cpu_batch.c` failed on
   `error: this 'for' clause does not guard... [-Werror=misleading-indentation]`
   at the line containing the large-array initialization and `init_links(links)`.
   Repair: separated `init_links(links)` onto its own statement/line. A full
   `-Wall -Wextra -Werror` rebuild succeeded and real native trials executed.

2. First invocation of `batch_bridge.py` failed with
   `{"status": "FAIL", "reason": "No module named 'connector'"}`.
   Root cause: new experimental path calculated workspace as `HERE.parents[2]`,
   which was `/mnt/data` rather than `workplace`.
   Repair: use `HERE.parents[1]` to locate preserved connector/physical contracts.
   The 8, 32 and 64-round runs subsequently executed HX89 feedback successfully.

3. The original EntropyAVX source's BVH bound defect was reproduced in the
   earlier preserved session and documented as bounds `[0,3]` rather than `[0,7]`.
   The isolated derivative repair passed extended BVH builds/refits and was
   recompiled/retested during the bounded watchdog run.

Important: negative tests in `test_bridge.py` deliberately mutate **in-memory copies**
of real observed trial records to verify refusal behavior. They are not fabricated
physical measurements and never enter the evidence ledger as hardware observations.

The append-only watchdog event journal records actual later task status and logs.
Prior failed commands were not recorded in its event journal because it did not
exist at the time; this note retains their diagnostic content without inventing
missing stdout or timestamps.
