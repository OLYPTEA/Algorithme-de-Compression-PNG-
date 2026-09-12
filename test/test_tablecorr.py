import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from compression.Huffman import huffman, extract_code, huffman_decode, huffman_encode

from compression.lz77 import lz77, lz77_2, lz77_decode
from collections import Counter

from codec.jsp import longueur_vers_code, distance_vers_code, lz77_vers_symboles_deflate, separer_symboles


if __name__ == "__main__":
    # Vérifions distance=12 : quelle plage la contient ?
    # Table : (9, 2, 6) couvre 9-12, puis (13, 2, 7) couvre 13-16
    # 12 >= 9 mais 12 < 13, donc c'est la ligne (9, 2, 6) qui correspond
    resultat = distance_vers_code(12)
    print(resultat)  # attendu : (6, 2, 3)   <- code 6, 2 bits supplémentaires, valeur 12-9=3
    assert resultat == (6, 2, 3), f"KO : {resultat}"
    print("OK distance=12")

    resultat2 = distance_vers_code(1)
    print(resultat2)  # attendu : (0, 0, 0)
    assert resultat2 == (0, 0, 0)
    print("OK distance=1")

    resultat3 = distance_vers_code(32768)
    print(resultat3)  # attendu : (29, 13, 32768-24577) = (29, 13, 8191)
    assert resultat3 == (29, 13, 8191)
    print("OK distance=32768 (valeur max)")



    
    symboles_lz77 = [65, 66, (2, 4)]  # A, B, (distance=2, longueur=4)
    evenements = lz77_vers_symboles_deflate(symboles_lz77)
    for e in evenements:
        print(e)


    
    symboles_lz77 = [65, 66, (2, 4)]
    evenements = lz77_vers_symboles_deflate(symboles_lz77)

    lit_lon, dist = separer_symboles(evenements)
    print("Littéraux/longueurs :", lit_lon)
    print("Distances :", dist)





    symboles_lz77 = [65, 66, (2, 4)]
    evenements = lz77_vers_symboles_deflate(symboles_lz77)
    lit_lon, dist = separer_symboles(evenements)

    freq_lit_lon = Counter(lit_lon)
    freq_dist = Counter(dist)

    arbre_lit_lon = huffman(dict(freq_lit_lon))
    arbre_dist = huffman(dict(freq_dist))

    codes_lit_lon = extract_code(arbre_lit_lon)
    codes_dist = extract_code(arbre_dist)

    print("Codes littéraux/longueurs :", codes_lit_lon)
    print("Codes distances :", codes_dist)

