import heapq  
from collections import Counter

class Noeud:                                                                 #On definit la classe Noeud pour représenter les nœuds de l'arbre de Huffman
    def __init__(self, freq, symbol=None, gauche=None, droite=None):
        self.freq = freq
        self.symbol = symbol
        self.gauche = gauche
        self.droite = droite

def huffman(frequences : dict):                                              #on construit l'arbre de Huffman à partir des fréquences des symboles
    tas = []                                                                 # on creer un tas
    for symbol, freq in frequences.items():                                  #On parcourt le dict creer avec Counter
        heapq.heappush(tas, (freq, Noeud(freq, symbol)))                     #on ajoute chaque symbole et sa fréquence dans le tas 

    while len(tas) > 1:                                                     #ici on boucle jusqu'à la racine de l'arbre de Huffman soit construite
        freq1, _, noeud1 = heapq.heappop(tas)                               # On prend les 2 plus petits elements du tas (grace a heapush c'est facile) et on les supprime du tas
        freq2, _, noeud2 = heapq.heappop(tas)
        nouveau = Noeud(freq1 + freq2, gauche=noeud1, droite=noeud2)        #On cree un nouveau noeud avec la somme des frequences des 2 plus petits elements 
    return tas[0][2]

def extract_code(noeud : Noeud, chemin : str = "", codes : dict = None):    
    if codes is None:                                                        #prevenir la valeur par défaut mutable
        codes = {}
    if noeud.symbol is not None:                                             #Si le noeud est une feuille on ajoute le symbole et son code binaire correspondant au dictionnaire codes
        codes[noeud.symbol] = chemin                                         
        return codes
    extract_code(noeud.gauche, chemin + "0", codes)                         # On parcourt le sous-arbre gauche et on ajoute "0" au chemin
    extract_code(noeud.droite, chemin + "1", codes)                         # On parcourt le sous-arbre droit et on ajoute "1" au chemin
    return codes
