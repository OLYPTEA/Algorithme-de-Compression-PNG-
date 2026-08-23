def encode_uint32_be(valeur: int) -> bytes:
    b3 = (valeur >> 24) & 0xFF
    b2 = (valeur >> 16) & 0xFF
    b1 = (valeur >> 8) & 0xFF
    b0 = valeur & 0xFF
    return bytes([b3, b2, b1, b0])
   


def decode_uint32_be(data: bytes) -> int:
    b3, b2, b1, b0 = data[0], data[1], data[2], data[3]
    return (b3 << 24) | (b2 << 16) | (b1 << 8) | b0