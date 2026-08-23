# filtres

def filtre0(L : bytes) -> bytes:             #identité
    return L

def filtre1(L : bytes, bpp : int) -> bytes:  #Difference avec le voisin de gauche
    out = bytearray(len(L))
    for i in range(len(L)):
        x = L[i]
        a = L[i - bpp] if i >= bpp else 0
        out[i] = (x - a) % 256
    return bytes(out)

def filtre2(L : bytes, M : bytes) -> bytes:  #Difference avec le voisin du haut
    out = bytearray(len(L))
    for i in range(len(L)):
        x = L[i]
        b = M[i] if M is not None else 0
        out[i] = (x - b) % 256
    return bytes(out)


def filtre3(L :bytes, M: bytes, bpp : int) -> bytes:  #Difference avec le voisin de gauche et du haut
    out = bytearray(len(L))
    for i in range(len(L)):
        x = L[i]
        a = L[i - bpp] if i >= bpp else 0
        b = M[i] if M is not None else 0
        out[i] = (x - (a+b)//2) % 256
    return bytes(out)

def filtre4(L: bytes, M: bytes, bpp : int) -> bytes: #Difference avec le voisin de gauche et du haut et du haut gauche
    out = bytearray(len(L))
    for i in range(len(L)):
        x = L[i]
        a = L[i - bpp] if i >= bpp else 0
        b = M[i] if M is not None else 0
        c = M[i - bpp] if (M is not None and i >= bpp) else 0
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            out[i] = (x - a) % 256
        elif pb <= pc:
            out[i] = (x - b) % 256
        else:
            out[i] = (x - c) % 256
    return bytes(out)