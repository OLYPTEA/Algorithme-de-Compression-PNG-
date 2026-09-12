import heapq  
from collections import Counter

class Noeud:                                                                 #On definit la classe Noeud pour représenter les nœuds de l'arbre de Huffman
    def __init__(self, freq, symbol=None, gauche=None, droite=None):
        self.freq = freq
        self.symbol = symbol
        self.gauche = gauche
        self.droite = droite

def huffman(frequences: dict) -> Noeud:
    tas = []
    for symbole, freq in frequences.items():
        heapq.heappush(tas, (freq, id(symbole), Noeud(freq, symbole)))

    # Cas particulier : un seul symbole distinct -> forcer une profondeur de 1
    if len(tas) == 1:
        freq, _, feuille = tas[0]
        return Noeud(freq, symbol=None, gauche=feuille, droite=None)

    while len(tas) > 1:
        freq1, _, noeud1 = heapq.heappop(tas)
        freq2, _, noeud2 = heapq.heappop(tas)
        nouveau = Noeud(freq1 + freq2, gauche=noeud1, droite=noeud2)
        heapq.heappush(tas, (nouveau.freq, id(nouveau), nouveau))

    return tas[0][2]

def extract_code(noeud, chemin="", codes=None):
    if codes is None:
        codes = {}
    if noeud.symbol is not None:
        codes[noeud.symbol] = chemin
        return codes
    extract_code(noeud.gauche, chemin + "0", codes)
    if noeud.droite is not None:
        extract_code(noeud.droite, chemin + "1", codes)
    return codes

def huffman_encode(symboles: list, codes: dict) -> str:
    resultat = ""
    for symbole in symboles:
        resultat += codes[symbole]
    return resultat

def huffman_decode(bits: str, racine: Noeud) -> list:
    symboles = []
    noeud_courant = racine

    for bit in bits:
        if bit == "0":
            noeud_courant = noeud_courant.gauche
        else:
            noeud_courant = noeud_courant.droite

        if noeud_courant.symbol is not None:
            symboles.append(noeud_courant.symbol)
            noeud_courant = racine   # on repart du sommet pour le prochain symbole

    return symboles
