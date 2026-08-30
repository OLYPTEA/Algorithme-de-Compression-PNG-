class BitReader:
    def __init__(self, data: bytes):
        self.data = data
        self.byte_pos = 0
        self.bit_pos = 0   

    def read_bit(self) -> int:
        if self.byte_pos >= len(self.data):
            raise EOFError("Fin de flux atteinte")
        bit = (self.data[self.byte_pos] >> self.bit_pos) & 1
        self.bit_pos += 1
        if self.bit_pos == 8:
            self.bit_pos = 0
            self.byte_pos += 1
        return bit

    def read_bits(self, n: int) -> int:
        value = 0
        for i in range(n):
            value |= (self.read_bit() << i)
        return value
        

        