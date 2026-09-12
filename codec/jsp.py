def longueur_vers_code(longueur: int) -> tuple[int, int, int]:
    """Retourne (code, nb_bits_supplementaires, valeur_bits_supplementaires)"""
    for i in range(len(LENGTH_TABLE) - 1, -1, -1):
        min_val, nb_bits, code = LENGTH_TABLE[i]
        if longueur >= min_val:
            valeur_extra = longueur - min_val
            return (code, nb_bits, valeur_extra)
    raise ValueError(f"Longueur invalide : {longueur}")

def distance_vers_code(distance: int) -> tuple[int, int, int]:
    """Retourne (code, nb_bits_supplementaires, valeur_bits_supplementaires)"""
    for i in range(len(DISTANCE_TABLE) - 1, -1, -1):
        min_val, nb_bits, code = DISTANCE_TABLE[i]
        if distance >= min_val:
            valeur_extra = distance - min_val
            return (code, nb_bits, valeur_extra)
    raise ValueError(f"Distance invalide : {distance}")


DISTANCE_TABLE = [
    (1, 0, 0), (2, 0, 1), (3, 0, 2), (4, 0, 3),
    (5, 1, 4), (7, 1, 5),
    (9, 2, 6), (13, 2, 7),
    (17, 3, 8), (25, 3, 9),
    (33, 4, 10), (49, 4, 11),
    (65, 5, 12), (97, 5, 13),
    (129, 6, 14), (193, 6, 15),
    (257, 7, 16), (385, 7, 17),
    (513, 8, 18), (769, 8, 19),
    (1025, 9, 20), (1537, 9, 21),
    (2049, 10, 22), (3073, 10, 23),
    (4097, 11, 24), (6145, 11, 25),
    (8193, 12, 26), (12289, 12, 27),
    (16385, 13, 28), (24577, 13, 29),
]


LENGTH_TABLE = [
    (3, 0, 257), (4, 0, 258), (5, 0, 259), (6, 0, 260),
    (7, 0, 261), (8, 0, 262), (9, 0, 263), (10, 0, 264),
    (11, 1, 265), (13, 1, 266), (15, 1, 267), (17, 1, 268),
    (19, 2, 269), (23, 2, 270), (27, 2, 271), (31, 2, 272),
    (35, 3, 273), (43, 3, 274), (51, 3, 275), (59, 3, 276),
    (67, 4, 277), (83, 4, 278), (99, 4, 279), (115, 4, 280),
    (131, 5, 281), (163, 5, 282), (195, 5, 283), (227, 5, 284),
    (258, 0, 285),
]


def lz77_vers_symboles_deflate(symboles_lz77: list) -> list:
    evenements = []
    for symbole in symboles_lz77:
        if isinstance(symbole, tuple):
            distance, longueur = symbole
            code_lon, bits_lon, extra_lon = longueur_vers_code(longueur)
            code_dist, bits_dist, extra_dist = distance_vers_code(distance)

            evenements.append(("longueur", code_lon, bits_lon, extra_lon))
            evenements.append(("distance", code_dist, bits_dist, extra_dist))
        else:
            evenements.append(("litteral", symbole))

    evenements.append(("fin_bloc", 256))
    return evenements

def separer_symboles(evenements: list) -> tuple[list, list]:
    symboles_lit_lon = []
    symboles_dist = []

    for event in evenements:
        if event[0] == "litteral":
            symboles_lit_lon.append(event[1])
        elif event[0] == "longueur":
            symboles_lit_lon.append(event[1])   # event[1] = le code (257-285)
        elif event[0] == "distance":
            symboles_dist.append(event[1])       # event[1] = le code (0-29)
        elif event[0] == "fin_bloc":
            symboles_lit_lon.append(event[1])    # 256

    return symboles_lit_lon, symboles_dist