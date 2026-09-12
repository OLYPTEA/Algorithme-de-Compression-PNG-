import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from codec.deflate import encoder_bloc_deflate
from codec.bitwriter import BitWriter
from codec.bitreader import BitReader

if __name__ == "__main__":
    bw = BitWriter()
    bw.write_bit(1)
    bw.write_bits("01")
    data = bw.get_bytes()

    br = BitReader(data)
    bfinal = br.read_bit()
    btype = br.read_bits(2)
    print("BFINAL:", bfinal, "BTYPE:", btype)