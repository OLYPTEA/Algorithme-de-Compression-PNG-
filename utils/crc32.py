POLY = 0xEDB88320

def build_crc_table() -> list[int]:
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            if c & 1:
                c = POLY ^ (c>> 1)
            else:
                c >>= 1
        table.append(c)
    return table

CRC_TABLE = build_crc_table()

def crc32(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for byte in data:
        index = (crc ^ byte) & 0xFF
        crc = CRC_TABLE[index] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF