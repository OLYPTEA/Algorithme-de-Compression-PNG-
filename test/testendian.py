import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.bigendian import encode_uint32_be, decode_uint32_be



if __name__ == "__main__":
    valeur = 1000
    encoded = encode_uint32_be(valeur)
    print(list(encoded))          # attendu : [0, 0, 3, 232]
    print(encoded.hex())           # attendu : '000003e8'

    decoded = decode_uint32_be(encoded)
    assert decoded == valeur, f"KO : {decoded} != {valeur}"
    print("OK : round-trip big-endian validé")

    valeur2 = 4_000_000_000
    encoded2 = encode_uint32_be(valeur2)
    decoded2 = decode_uint32_be(encoded2)
    assert decoded2 == valeur2
    print("OK : round-trip sur grande valeur validé")