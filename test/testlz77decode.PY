import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compression.lz77 import lz77_decode, lz77_2


if __name__ == "__main__":
    # Cas 1 : exemple "Hello" qu'on vient de dérouler à la main
    symboles1 = [72, 101, 108, 108, 111, (5, 5), 33]
    resultat1 = lz77_decode(symboles1)
    assert resultat1 == b"HelloHello!", f"KO cas 1 : {resultat1}"
    print("OK cas 1 :", resultat1)

    # Cas 2 : chevauchement (distance < longueur)
    symboles2 = [65, (1, 5)]
    resultat2 = lz77_decode(symboles2)
    assert resultat2 == b"AAAAAA", f"KO cas 2 : {resultat2}"
    print("OK cas 2 (chevauchement) :", resultat2)

    # Cas 3 : round-trip complet, encode puis decode
    data = b"ABABAB"
    encoded = lz77_2(data)
    decoded = lz77_decode(encoded)
    assert decoded == data, f"KO round-trip : {decoded} != {data}"
    print("OK round-trip :", decoded)