import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from codec.bitreader import BitReader
from codec.bitwriter import BitWriter

if __name__ == "__main__":
    bw = BitWriter()
    bw.write_bits("1011")
    data = bw.get_bytes()

    br = BitReader(data)
    bits_lus = [br.read_bit() for _ in range(4)]
    print(bits_lus)
    assert bits_lus == [1, 0, 1, 1], f"KO : {bits_lus}"
    print("OK : BitReader round-trip validé")

    # Test avec read_bits directement
    br2 = BitReader(data)
    valeur = br2.read_bits(4)
    print(bin(valeur))
    assert valeur == 0b1101, f"KO : {bin(valeur)}"  # 1011 en LSB-first -> valeur 0b1101
    print("OK : read_bits validé")