def adler32(data: bytes) -> int:
    MOD = 65521
    A = 1
    B = 0
    for octet in data:
        A = (A + octet) % MOD
        B = (B + A) % MOD
    return (B << 16) | A