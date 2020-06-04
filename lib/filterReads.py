#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : Fonction de création du dictionnaire étendu, Parsing complet du fichier SAM
    Entrée : nom de read et dictionnaire.
    Sortie : dictionnaire contenant les informations du SAM.

"""

import re, os, time

def filterReads(chemin, outputFile, list2save, tot):
    print(outputFile)
    with open(chemin, "r") as f:
        print("SAM file filtering...")
        time.sleep(1)
        i = 0
        with open(outputFile, "w") as o:
            for line in f.readlines():
                i = i + 1
                compteur = (i / tot) * 100
                if ((compteur % 5) == 0):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(str(round(compteur)/2) + " %")  # affichage d'un compteur de progression du parsing
                if (re.search("^@", line)):  # si ma ligne commence par @ alors je traite le header
                    o.write(line)
                else :
                    if (line.split("\t", 2)[0] in list2save) :
                        o.write(line)
            o.close()
            print("SAM file filtered !")
            time.sleep(1)



###################################Back-up############################################################


# def filterReads(chemin, outputFile, list2save):
#     print(outputFile)
#     with open(chemin, "r") as f:
#         print("Filtration du fichier SAM...")
#         with open(outputFile, "w") as o:
#             for line in f.readlines():
#                 if (re.search("^@", line)):  # si ma ligne commence par @ alors je traite le header
#                     o.write(line)
#                 else :
#                     if (line.split("\t", 2)[0] in list2save) :
#                         o.write(line)
#             o.close()
