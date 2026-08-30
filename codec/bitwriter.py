class BitWriter:
    def __init__(self):
        self.buffer = bytearray()
        self.bit_courant = 0
        self.nb_bits = 0

    def write_bit(self, bit: int):
        if bit not in (0, 1):
            raise ValueError("Le bit doit être 0 ou 1")
        self.bit_courant |= (bit << self.nb_bits)
        self.nb_bits += 1
        if self.nb_bits == 8:
            self.buffer.append(self.bit_courant)
            self.bit_courant = 0
            self.nb_bits = 0

    def write_bits(self, bits: str):
        for bit in bits:
            self.write_bit(int(bit))

    def get_bytes(self) -> bytes:
        if self.nb_bits > 0:
            self.buffer.append(self.bit_courant)
        return bytes(self.buffer)