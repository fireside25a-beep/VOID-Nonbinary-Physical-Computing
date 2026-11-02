VOID / HX89 SOURCE AUDIT — macOS REPRODUCTION (READ-ONLY)
2026-11-02

1. Put the eight ORIGINAL, unchanged research ZIP files in one directory.
2. Unpack this small AUDIT ZIP to the same directory. It makes a directory named
   VOID_SOURCE_AUDIT_20261102 alongside the original research ZIPs.
3. Open Terminal and change to the extracted audit directory, e.g.
     cd "$HOME/Downloads/VOID_SOURCE_AUDIT_20261102"
   If originals are in another directory, configure VOID_ARCHIVE_DIR below.
4. With Python 3 installed, execute:
     python3 audit_inventory.py
     python3 categorize_inventory.py
     python3 nested_index.py
     python3 recursive_nested.py
5. To specify a different input location:
     VOID_ARCHIVE_DIR="$HOME/Research/Originals" python3 audit_inventory.py
     python3 categorize_inventory.py
     VOID_ARCHIVE_DIR="$HOME/Research/Originals" python3 nested_index.py
     VOID_ARCHIVE_DIR="$HOME/Research/Originals" python3 recursive_nested.py
   Outputs default to the audit script directory. For audit_inventory.py,
   nested_index.py and recursive_nested.py, VOID_AUDIT_OUTPUT changes that destination.

These scripts ONLY READ source ZIP archives and WRITE NEW audit metadata, replacing
metadata files in their designated audit output folder. They DO NOT unpack or
modify the research archives, run the HX89 binary, run compiled projects, or
synthesize measurements. They do not verify the scientific validity of a saved log.

IMPORTANT:
* Native executable 'hx89' in the bridge is Linux ELF x86-64, and will NOT run
  directly on an Apple Silicon MacBook. Mac compatibility requires an explicit
  port/rebuild or a compatible Linux/x86-64 execution environment.
* This package is the AUDIT REPORT, NOT a cleaned release and NOT a replacement
  for original user archives. No source files have been moved or renamed.
* Never flatten R06 historical source into the R08 active directory.
