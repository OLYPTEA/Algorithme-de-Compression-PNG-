import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.crc32 import build_crc_table, crc32

if __name__ == "__main__":
    table = build_crc_table()
    print(table[0])    # doit être 0
    print(table[1])    # doit être 0x77073096
    print(len(table))  # doit être 256

    resultat = crc32(b"123456789")
    print(hex(resultat))
    assert resultat == 0xCBF43926, f"KO : obtenu {hex(resultat)}, attendu 0xcbf43926"
    print("OK : CRC32 conforme à la référence standard")