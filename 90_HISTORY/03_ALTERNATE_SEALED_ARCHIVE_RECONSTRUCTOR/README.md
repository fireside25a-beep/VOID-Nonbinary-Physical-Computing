# Alternate historical reconstruction convention

This retained Python source expects a `VOID_SPLIT_ARCHIVE_V1` JSON manifest of byte-concatenated pieces of a single ZIP. It is not the reader for the current **independent** `VOID_RELEASE_PART_*.zip` files. The active release script is at `00_CONTROL/reconstruct_void_parts.py` and accepts `--parts-dir`, `--verify-only`, and `--output`. Preserve both formats separately; never substitute the historical one for the active release.
