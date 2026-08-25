def lz77(data : bytes, pos : int, win_size :int = 32768, max_length : int = 258):
    meilleur_distance = 0
    meilleur_longueur = 0
    debut_fenetre = max(0, pos - win_size)

    for candidat in range(debut_fenetre, pos):
        longueur  = 0
        while pos + longueur < len(data) and longueur < max_length and data[candidat + longueur] == data[pos + longueur]:
            longueur +=1
        if longueur > meilleur_longueur and longueur <= max_length:
            meilleur_longueur = longueur
            meilleur_distance = pos - candidat
    if meilleur_longueur >= 3:
        return (meilleur_distance, meilleur_longueur)
    return (0, 0)

def lz77_2(data : bytes):
    pos = 0
    symbols = []
    while pos < len(data):
        distance, longueur = lz77(data, pos)
        if longueur >= 3:
            symbols.append((distance, longueur))
            pos += longueur
        else:
            symbols.append(data[pos])
            pos += 1
    return symbols

def lz77_decode(symbols : list):
    result = bytearray()
    for symbol in symbols:
        if isinstance(symbol, tuple):
            distance, longueur = symbol
            for _ in range(longueur):
                pos_source = len(result) - distance
                valeur = result[pos_source]
                result.append(valeur)
        else:
            result.append(symbol)
    return bytes(result)