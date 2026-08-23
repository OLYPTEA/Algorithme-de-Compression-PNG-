from utils.crc32 import crc32
from utils.bigendian import encode_uint32_be
from utils.bigendian import encode_uint32_be, decode_uint32_be

PNG_SIGNATURE = bytes([137, 80, 78, 71, 13, 10, 26, 10])


def write_chunks(path: str, chunks: list[tuple[str, bytes]]) -> None:
    with open(path, "wb") as f:
        f.write(PNG_SIGNATURE)
        for chunk_type, data in chunks:
            type_bytes = chunk_type.encode("ascii")
            length = len(data)
            length_bytes = encode_uint32_be(length)
            f.write(length_bytes)
            f.write(type_bytes)
            f.write(data)
            crc_input = type_bytes + data
            crc_value = crc32(crc_input)
            crc_bytes = encode_uint32_be(crc_value)
            f.write(crc_bytes)

def read_chunks(path: str) -> list[tuple[str, bytes]]:
    with open(path, "rb") as f:
        data = f.read()

    if data[:8] != PNG_SIGNATURE:
        raise ValueError("Signature PNG invalide")

    chunks = []
    offset = 8

    while offset < len(data):
        length_bytes = data[offset:offset + 4]
        length = decode_uint32_be(length_bytes)
        offset += 4

        type_bytes = data[offset:offset + 4]
        chunk_type = type_bytes.decode("ascii")
        offset += 4

        chunk_data = data[offset:offset + length]
        offset += length

        crc_bytes = data[offset:offset + 4]
        crc_value = decode_uint32_be(crc_bytes)
        offset += 4

        crc_input = type_bytes + chunk_data
        calculated_crc = crc32(crc_input)

        if crc_value != calculated_crc:
            raise ValueError(f"CRC invalide pour le chunk {chunk_type}")

        chunks.append((chunk_type, chunk_data))

    return chunks


          