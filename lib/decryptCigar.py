#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : Fonction de Decryptage du CIGAR
    Entrée : CIGAR
    Sortie : Explication humainement compréhensible

"""

import re

def decryptCigar(cig) :
    # print("Décryption du CIGAR :")
    # Utilisation des Expressions régulières
    # problème avec Match or mismatch qui ne sont pas en début du CIGAR une solution mais pas convaincant
    if re.search("[0-9]+[MIDS]", cig) :
        if re.search("(([0-9]+)M)", cig) :
            print(re.search("(([0-9]+)M)", cig).group(2) + " matchs or mismatchs")
        if re.search("[0-9]+I", cig) :
            print(re.search("(([0-9]+)I)", cig).group(2) + " insertions")
        if re.search("[0-9]+D", cig) :
            print(re.search("(([0-9]+)D)", cig).group(2) + " deletions")
        if re.search("[0-9]+S", cig):
            print(re.search("(([0-9]+)S)", cig).group(2) + " soft clips")
        if re.search("[0-9]+H", cig):
            print(re.search("(([0-9]+)H)", cig).group(2) + " hard clips")
        if re.search("[0-9]+P", cig):
            print(re.search("(([0-9]+)P)", cig).group(2) + " padding")
        if re.search("(([0-9]+)M)", cig) :
            print(re.search(".*[IDS](([0-9]+)M)$", cig).group(2) + " matchs or mismatchs") # problème si ça fini pas par M...
    else :
        print("CIGAR non conforme : " + cig)
        return ""

# Test de la fonction :

# cig = "57M1D43M"
# decryptCigar(cig)