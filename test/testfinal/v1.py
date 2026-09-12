import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from compression.lz77 import lz77, lz77_decode, lz77_2
from codec.jsp import lz77_vers_symboles_deflate, separer_symboles
from collections import Counter
from compression.Huffman import huffman, huffman_encode, huffman_decode, extract_code
from codec.deflate import encoder_bloc_deflate

if __name__ == "__main__":
    symboles_lz77 = [65, 66, (2, 4)]
    evenements = lz77_vers_symboles_deflate(symboles_lz77)
    lit_lon, dist = separer_symboles(evenements)

    freq_lit_lon = Counter(lit_lon)
    freq_dist = Counter(dist)
    arbre_lit_lon = huffman(dict(freq_lit_lon))
    arbre_dist = huffman(dict(freq_dist))
    codes_lit_lon = extract_code(arbre_lit_lon)
    codes_dist = extract_code(arbre_dist)

    encoded = encoder_bloc_deflate(evenements, codes_lit_lon, codes_dist)
    print("Flux encodé :", list(encoded))
    print("Longueur en octets :", len(encoded))