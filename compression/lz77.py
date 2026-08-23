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