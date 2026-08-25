import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compression.lz77 import lz77_2

if __name__ == "__main__":
    data = b"ABABAB"
    resultat = lz77_2(data)
    print(resultat)
    # attendu : [65, 66, (2, 4)]
    assert resultat == [65, 66, (2, 4)], f"KO : {resultat}"
    print("OK : lz77_2 fonctionne")