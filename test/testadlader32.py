import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.adlader32 import adler32


if __name__ == "__main__":
    resultat = adler32(b"Wikipedia")
    print(hex(resultat))
    assert resultat == 0x11E60398, f"KO : {hex(resultat)}"
    print("OK : Adler-32 conforme à la référence")