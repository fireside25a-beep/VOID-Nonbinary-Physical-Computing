# Release tools

`BUILD_TEN_FOLDER_RELEASE.py` creates the ten logical ZIP folders from an immutable snapshot of a single `workplace/` tree. It rejects unclassified paths, original master omission, unsafe source modes and ZIP modules >=200,000,000 bytes. Run outside the actual source tree to avoid recursive inclusion.

`RESTORE_AND_AUDIT.py` independently verifies module SHA-256/CRC, extracts into a new destination only, reconstructs the 301 MB historical source master from its two original parts, and hashes every file and checks every directory. It preserves executable mode bits.

Official release processes only freeze the tree **after** all repeat tests have finished. Never run packaging against an actively writing test tree.
