#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : Fonction de création des dictionnaires Single, fisrt et second reads
    Entrée : allread, reads, j, Flagreads, DicoSingle, Dicofirst, Dicosecond
    Sortie : dictionnaire contenant les informations de FLAG.

"""

import os, time
from lib.Flagread import *

def dicoFlag(allread, tot,  DicoSingle, Dicofirst, Dicosecond):
    i = 0
    print("Flags parsing...")
    time.sleep(1)
    for reads in allread.keys():
        i = i + 1
        compteur = (i / tot) * 100
        if ((compteur % 5) == 0):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(str(round(compteur)) + " %") # affichage d'un compteur de progression du parsing

        if (int(allread[reads]['BINFLAG'][0][-1]) == 1) :
            for j in [0, 1]:
                Flagreads = {}
                Flagread(allread, reads, j, Flagreads)
                if (int(Flagreads['first']) == 1):  # Is the first read ?
                    Dicofirst[reads] = Flagreads

                elif (int(Flagreads['first']) == 0):  # Is the second read ?
                    Dicosecond[reads] = Flagreads

        elif (int(allread[reads]['BINFLAG'][0][-1]) == 0) :
            j = 0
            Flagreads = {}
            Flagread(allread, reads, j, Flagreads)
            DicoSingle[reads] = Flagreads

    print("Flags parsed !")
    time.sleep(1)
    return Dicofirst, Dicosecond, DicoSingle

# {'paired': 1, 'proper': 1, 'unmap': 0, 'mateUnMap': 0, 'strand': 0, 'mateStrand': 1, 'first': 1, 'second': 0, 'alignment1': 0, 'QC': 0, 'duplicate': 0}
# {'paired': 1, 'proper': 1, 'unmap': 0, 'mateUnMap': 0, 'strand': 1, 'mateStrand': 0, 'first': 0, 'second': 1, 'alignment1': 0, 'QC': 0, 'duplicate': 0}