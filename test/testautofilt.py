import sys
import os

# Remonte d'un dossier (test/ -> racine du projet) pour que Python
# trouve les packages "filtering"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filtering.filter import filtre0, filtre1, filtre2, filtre3, filtre4
from filtering.unfilter import unfiltre0, unfiltre1, unfiltre2, unfiltre3, unfiltre4
from filtering.filterselector import score_ligne, meilleur_filtre, filtrer_image, defiltrer_image

# ============================================================
# PARTIE 1 : round-trip des 5 filtres pris individuellement
# ============================================================

def test_filtres_individuels():
    ligne_precedente = bytes([10, 20, 30, 40, 50, 60])
    ligne_courante   = bytes([15, 25, 35, 100, 110, 120])
    bpp = 3

    print("=== Partie 1 : filtres individuels ===")

    f0 = filtre0(ligne_courante)
    r0 = unfiltre0(f0)
    assert r0 == ligne_courante, f"KO filtre0 : {list(r0)}"
    print("OK filtre0 :", list(f0))

    f1 = filtre1(ligne_courante, bpp)
    r1 = unfiltre1(f1, bpp)
    assert r1 == ligne_courante, f"KO filtre1 : {list(r1)}"
    print("OK filtre1 :", list(f1))

    f2 = filtre2(ligne_courante, ligne_precedente)
    r2 = unfiltre2(f2, ligne_precedente)
    assert r2 == ligne_courante, f"KO filtre2 : {list(r2)}"
    print("OK filtre2 :", list(f2))

    f3 = filtre3(ligne_courante, ligne_precedente, bpp)
    r3 = unfiltre3(f3, ligne_precedente, bpp)
    assert r3 == ligne_courante, f"KO filtre3 : {list(r3)}"
    print("OK filtre3 :", list(f3))

    f4 = filtre4(ligne_courante, ligne_precedente, bpp)
    r4 = unfiltre4(f4, ligne_precedente, bpp)
    assert r4 == ligne_courante, f"KO filtre4 : {list(r4)}"
    print("OK filtre4 :", list(f4))


def test_cas_bord_premiere_ligne():
    ligne_courante = bytes([15, 25, 35, 100, 110, 120])
    bpp = 3

    print("\n=== Partie 1bis : première ligne (previous = None) ===")

    f2 = filtre2(ligne_courante, None)
    r2 = unfiltre2(f2, None)
    assert r2 == ligne_courante, f"KO filtre2 bord : {list(r2)}"
    print("OK filtre2 (previous=None) :", list(f2))

    f3 = filtre3(ligne_courante, None, bpp)
    r3 = unfiltre3(f3, None, bpp)
    assert r3 == ligne_courante, f"KO filtre3 bord : {list(r3)}"
    print("OK filtre3 (previous=None) :", list(f3))

    f4 = filtre4(ligne_courante, None, bpp)
    r4 = unfiltre4(f4, None, bpp)
    assert r4 == ligne_courante, f"KO filtre4 bord : {list(r4)}"
    print("OK filtre4 (previous=None) :", list(f4))


def test_cas_extremes():
    print("\n=== Partie 1ter : débordement modulo 256 ===")

    bpp = 3
    ligne_extreme = bytes([0, 255, 128, 1, 254, 127])
    prev_extreme  = bytes([255, 0, 200, 3, 100, 50])

    for nom, f, uf, args in [
        ("filtre1", filtre1, unfiltre1, (bpp,)),
        ("filtre2", filtre2, unfiltre2, (prev_extreme,)),
        ("filtre3", filtre3, unfiltre3, (prev_extreme, bpp)),
        ("filtre4", filtre4, unfiltre4, (prev_extreme, bpp)),
    ]:
        filtered = f(ligne_extreme, *args)
        recon = uf(filtered, *args)
        assert recon == ligne_extreme, f"KO {nom} (extreme) : {list(recon)}"
        print(f"OK {nom} (extreme) :", list(filtered))


# ============================================================
# PARTIE 2 : score_ligne et meilleur_filtre
# ============================================================

def test_score_ligne():
    print("\n=== Partie 2 : score_ligne ===")
    s = score_ligne(bytes([0, 1, 255, 128]))
    assert s == 130, f"KO score_ligne : attendu 130, obtenu {s}"
    print("OK score_ligne :", s)


def test_meilleur_filtre():
    print("\n=== Partie 2bis : meilleur_filtre ===")
    ligne_precedente = bytes([10, 20, 30, 40, 50, 60])
    ligne_courante   = bytes([15, 25, 35, 100, 110, 120])
    bpp = 3

    filter_type, ligne_filtree = meilleur_filtre(ligne_courante, ligne_precedente, bpp)
    print("Filtre choisi :", filter_type)
    print("Ligne filtrée :", list(ligne_filtree))

    # Vérifie que le filtre choisi donne bien le score minimal parmi les 5
    scores = []
    for f_type, f, args in [
        (0, filtre0, ()),
        (1, filtre1, (bpp,)),
        (2, filtre2, (ligne_precedente,)),
        (3, filtre3, (ligne_precedente, bpp)),
        (4, filtre4, (ligne_precedente, bpp)),
    ]:
        filtered = f(ligne_courante, *args)
        scores.append(score_ligne(filtered))

    assert score_ligne(ligne_filtree) == min(scores), "Le filtre choisi n'a pas le score minimal !"
    print("OK meilleur_filtre : score minimal confirmé parmi les 5 candidats")


# ============================================================
# PARTIE 3 : pipeline complet sur une image (plusieurs lignes)
# ============================================================

def test_roundtrip_image_complete():
    print("\n=== Partie 3 : round-trip image complète ===")

    lignes = [
        bytes([10, 20, 30, 40, 50, 60]),
        bytes([15, 25, 35, 100, 110, 120]),
        bytes([12, 22, 32, 90, 95, 100]),
    ]
    bpp = 3
    largeur_ligne = len(lignes[0])

    flux = filtrer_image(lignes, bpp)
    print("Flux complet :", list(flux))
    print("Longueur obtenue :", len(flux))

    longueur_attendue = len(lignes) * (1 + largeur_ligne)
    assert len(flux) == longueur_attendue, (
        f"KO longueur flux : attendu {longueur_attendue}, obtenu {len(flux)}"
    )
    print("OK : longueur du flux correcte")

    lignes_reconstruites = defiltrer_image(flux, largeur_ligne, bpp)
    assert lignes_reconstruites == lignes, (
        f"KO round-trip image : {lignes_reconstruites} != {lignes}"
    )
    print("OK : round-trip complet de l'image validé")


def test_roundtrip_image_plus_grande():
    """Image plus réaliste : 5 lignes, grayscale (bpp=1), largeur 8."""
    print("\n=== Partie 3bis : round-trip image plus grande (grayscale) ===")

    bpp = 1
    largeur_ligne = 8
    lignes = [
        bytes([0, 10, 20, 30, 40, 50, 60, 70]),
        bytes([5, 12, 22, 33, 44, 55, 66, 77]),
        bytes([200, 200, 200, 200, 150, 100, 50, 0]),
        bytes([255, 254, 253, 252, 251, 250, 249, 248]),
        bytes([1, 1, 1, 1, 1, 1, 1, 1]),
    ]

    flux = filtrer_image(lignes, bpp)
    longueur_attendue = len(lignes) * (1 + largeur_ligne)
    assert len(flux) == longueur_attendue, "KO longueur flux (image plus grande)"

    lignes_reconstruites = defiltrer_image(flux, largeur_ligne, bpp)
    assert lignes_reconstruites == lignes, "KO round-trip (image plus grande)"
    print("OK : round-trip validé sur image 5 lignes x 8 octets (grayscale)")


if __name__ == "__main__":
    test_filtres_individuels()
    test_cas_bord_premiere_ligne()
    test_cas_extremes()
    test_score_ligne()
    test_meilleur_filtre()
    test_roundtrip_image_complete()
    test_roundtrip_image_plus_grande()

    print("\n✅ Tous les tests de l'étape 2 (filtrage) sont passés.")