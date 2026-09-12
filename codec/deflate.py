from codec.bitreader import BitReader
from codec.bitwriter import BitWriter

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


def encoder_bloc_deflate(evenements: list, codes_lit_lon: dict, codes_dist: dict) -> bytes:
    bw = BitWriter()
    bw.write_bit(1)        
    bw.write_bits("01")    
    for event in evenements:
        if event[0] == "litteral":
            valeur = event[1]
            bw.write_bits(codes_lit_lon[valeur])
        elif event[0] == "longueur":
            _, code, bits, extra = event
            bw.write_bits(codes_lit_lon[code])
            if bits > 0:
                bw.write_bits(format(extra, f'0{bits}b'))
        elif event[0] == "distance":
            _, code, bits, extra = event
            bw.write_bits(codes_dist[code])
            if bits > 0:
                bw.write_bits(format(extra, f'0{bits}b'))
        elif event[0] == "fin_bloc":
            valeur = event[1]
            bw.write_bits(codes_lit_lon[valeur])

    return bw.get_bytes()





def code_vers_longueur(code: int) -> tuple:
    for min_val, nb_bits, c in LENGTH_TABLE:
        if c == code:
            return (min_val, nb_bits)
    raise ValueError(f"Code de longueur invalide : {code}")


def code_vers_distance(code: int) -> tuple:
    for min_val, nb_bits, c in DISTANCE_TABLE:
        if c == code:
            return (min_val, nb_bits)
    raise ValueError(f"Code de distance invalide : {code}")


def lire_symbole_huffman(br, racine) -> int:
    noeud_courant = racine
    while noeud_courant.symbol is None:
        bit = br.read_bit()
        if bit == 0:
            noeud_courant = noeud_courant.gauche
        else:
            noeud_courant = noeud_courant.droite
    return noeud_courant.symbol


def decoder_bloc_deflate(data: bytes, arbre_lit_lon, arbre_dist) -> list:
    br = BitReader(data)
    symboles_lz77 = []

    bfinal = br.read_bit()
    btype = br.read_bits(2)

    while True:
        symbole = lire_symbole_huffman(br, arbre_lit_lon)

        if symbole == 256:
            break
        elif symbole < 256:
            symboles_lz77.append(symbole)
        else:
            min_val_lon, nb_bits_lon = code_vers_longueur(symbole)
            extra_lon = br.read_bits(nb_bits_lon) if nb_bits_lon > 0 else 0
            longueur = min_val_lon + extra_lon

            code_dist = lire_symbole_huffman(br, arbre_dist)
            min_val_dist, nb_bits_dist = code_vers_distance(code_dist)
            extra_dist = br.read_bits(nb_bits_dist) if nb_bits_dist > 0 else 0
            distance = min_val_dist + extra_dist

            symboles_lz77.append((distance, longueur))

    return symboles_lz77


