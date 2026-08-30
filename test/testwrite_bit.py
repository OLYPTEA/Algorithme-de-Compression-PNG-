import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from codec.bitwriter import BitWriter


if __name__ == "__main__":
    bw = BitWriter()
    bw.write_bits("1011")
    resultat = bw.get_bytes()
    print(bin(resultat[0]))
    assert resultat[0] == 0b00001101, f"KO : {bin(resultat[0])}"
    print("OK : BitWriter LSB-first validé")