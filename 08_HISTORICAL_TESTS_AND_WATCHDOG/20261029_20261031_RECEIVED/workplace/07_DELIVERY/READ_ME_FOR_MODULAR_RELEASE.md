# Full modular VOID/HX89 workplace delivery

All nine transport ZIP modules extract into a single `workplace/` path. They are not nine separate projects. They preserve every source/log and historical release, including failed or aborted runs; no tree trimming is performed.

1. Place all nine ZIPs plus the restore/audit kit in one directory.
2. Extract the kit at that location.
3. Run `python3 RESTORE_VERIFY.py --verify-only`.
4. Run `python3 RESTORE_VERIFY.py --dest VOID_HX89_REBUILT` in an empty destination.
5. Read `VOID_HX89_REBUILT/workplace/WORKPLACE_START_HERE.md`.
6. Read `06_RELEASE_CONTROL/FINAL_CURRENT_SNAPSHOT_RELEASE_NOTES.md` for exact current test status.

Part 01 and Part 02 contain the literal original byte-split research master and the restoration script reconstructs its 301,454,742-byte master file exactly, rather than omitting it or replacing it with a placeholder.
