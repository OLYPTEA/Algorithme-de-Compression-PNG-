from utils.bigendian import encode_uint32_be
from utils.adlader32 import adler32

def zlib_wrap(deflate_data: bytes, donnees_originales: bytes) -> bytes:
    CMF = 0x78
    FLG = 0
    while (CMF * 256 + FLG) % 31 != 0:
        FLG += 1

    checksum = adler32(donnees_originales)
    checksum_bytes = encode_uint32_be(checksum)  # tu as déjà cette fonction !

    return bytes([CMF, FLG]) + deflate_data + checksum_bytes