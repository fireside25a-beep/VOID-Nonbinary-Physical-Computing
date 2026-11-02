# Immutable uploaded inputs — reconstructable byte-for-byte

All eight original ZIP archives are retained either as a whole ZIP (<48 MB) or as a simple sequence of raw byte fragments of <=45 MB each. No compressed archive was normalized, altered, or renamed internally.

Why: GitHub warns for files >=50 MB and rejects ordinary Git pushes of files >=100 MB. Large historical ZIPs are split without data loss for GitHub storage.

Use `python3 reconstruct_original_inputs.py --out ../VOID_RECONSTRUCTED_UPLOADS` from inside the `VOID/` directory to rebuild original byte-identical ZIP archives in a folder outside your Git repository. Every fragment and rebuilt ZIP is hashed and verified.

This is provenance, not proof of software correctness or permission to republish every historically included asset.
