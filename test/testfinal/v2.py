import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from compression.lz77 import lz77, lz77_decode, lz77_2
from codec.jsp import lz77_vers_symboles_deflate, separer_symboles
from collections import Counter
from compression.Huffman import huffman, huffman_encode, huffman_decode, extract_code
from codec.deflate import encoder_bloc_deflate, code_vers_distance, code_vers_longueur, lire_symbole_huffman, decoder_bloc_deflate 

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




if __name__ == "__main__":
    # Round-trip complet : lz77 -> deflate encode -> deflate decode -> lz77_decode
    symboles_lz77_origine = [65, 66, (2, 4)]
    evenements = lz77_vers_symboles_deflate(symboles_lz77_origine)
    lit_lon, dist = separer_symboles(evenements)
 
    freq_lit_lon = Counter(lit_lon)
    freq_dist = Counter(dist)
    arbre_lit_lon = huffman(dict(freq_lit_lon))
    arbre_dist = huffman(dict(freq_dist))
    codes_lit_lon = extract_code(arbre_lit_lon)
    codes_dist = extract_code(arbre_dist)
 
    encoded = encoder_bloc_deflate(evenements, codes_lit_lon, codes_dist)
    print("Flux encodé :", list(encoded))
 
    symboles_decodes = decoder_bloc_deflate(encoded, arbre_lit_lon, arbre_dist)
    print("Symboles LZ77 décodés :", symboles_decodes)
 
    assert symboles_decodes == symboles_lz77_origine, (
        f"KO : {symboles_decodes} != {symboles_lz77_origine}"
    )
    print("OK : décodage DEFLATE -> symboles LZ77 identiques à l'origine")
 
    data_finale = lz77_decode(symboles_decodes)
    print("Données finales :", data_finale)
    assert data_finale == b"ABABAB", f"KO : {data_finale}"
    print("✅ Round-trip complet LZ77 + Huffman + DEFLATE validé")