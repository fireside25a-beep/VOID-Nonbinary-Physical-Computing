import os
import sys
if __name__ == "__main__":
    binary_target = "./EntropyAVXEngine" if os.name != "nt" else "EntropyAVXEngine.exe"
    if os.path.exists(binary_target):
        os.environ["ISOLATED_AVX2_RUNTIME"] = "TRUE"
        os.system(binary_target)
    else:
        print("[-] Execution signature missing. Run the compiler build chain scripts first.")
