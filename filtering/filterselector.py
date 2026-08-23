from filtering.filter import filtre0, filtre1, filtre2, filtre3, filtre4
from filtering.unfilter import unfiltre0, unfiltre1, unfiltre2, unfiltre3, unfiltre4

def score_ligne(L: bytes):
    score = 0
    for i in range(len(L)):
        score += min(L[i], 256 - L[i])
    return score

def meilleur_filtre(L: bytes, M: bytes, bpp: int):
    resultats = []
    for f in [filtre0, filtre1, filtre2, filtre3, filtre4]:
        if f == filtre0:
            filtered = f(L)
        elif f == filtre1:
            filtered = f(L, bpp)
        elif f == filtre2:
            filtered = f(L, M)
        else:
            filtered = f(L, M, bpp)
        resultats.append((filtered, score_ligne(filtered)))

    scores = [s for (_, s) in resultats]
    meilleur_index = scores.index(min(scores))
    meilleure_ligne = resultats[meilleur_index][0]

    return meilleur_index, meilleure_ligne    # <- retourne bien un tuple

def filtrer_image(lignes: list[bytes], bpp: int) -> bytes:
    resultat = bytearray()
    M = None  
    for L in lignes:
        filter_type, ligne_filtree = meilleur_filtre(L, M, bpp)
        resultat.append(filter_type)     
        resultat.extend(ligne_filtree)   
        M = L  
    return bytes(resultat)

def defiltrer_image(flux: bytes, largeur_ligne: int, bpp: int) -> list[bytes]:
    ligne = []
    M = None
    offset = 0

    while offset < len(flux):
        filter_type = flux[offset]
        offset += 1
        ligne_filtree = flux[offset:offset + largeur_ligne]
        offset += largeur_ligne

        if filter_type == 0:
            L = unfiltre0(ligne_filtree)
        elif filter_type == 1:
            L = unfiltre1(ligne_filtree, bpp)
        elif filter_type == 2:
            L = unfiltre2(ligne_filtree, M)
        elif filter_type == 3:
            L = unfiltre3(ligne_filtree, M, bpp)
        elif filter_type == 4:
            L = unfiltre4(ligne_filtree, M, bpp)
        else:
            raise ValueError(f"Type de filtre inconnu : {filter_type}")

        ligne.append(L)
        M = L

    return ligne