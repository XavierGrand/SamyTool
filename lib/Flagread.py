#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : Fonction de création des dictionnaires de FLAGS uniquement
    Entrée : allread, reads, j, Flagreads
    Sortie : dictionnaire contenant les informations de FLAG.

"""

def Flagread(allread, reads, j, Flagreads) :
    Flagreads['paired'] = int(allread[reads]['BINFLAG'][j][-1])
    Flagreads['proper'] = int(allread[reads]['BINFLAG'][j][-2])
    Flagreads['unmap'] = int(allread[reads]['BINFLAG'][j][-3])
    Flagreads['mateUnMap'] = int(allread[reads]['BINFLAG'][j][-4])
    Flagreads['strand'] = int(allread[reads]['BINFLAG'][j][-5])
    Flagreads['mateStrand'] = int(allread[reads]['BINFLAG'][j][-6])
    Flagreads['first'] = int(allread[reads]['BINFLAG'][j][-7])
    Flagreads['second'] = int(allread[reads]['BINFLAG'][j][-8])
    Flagreads['alignment1'] = int(allread[reads]['BINFLAG'][j][-9])
    Flagreads['QC'] = int(allread[reads]['BINFLAG'][j][-10])
    Flagreads['duplicate'] = int(allread[reads]['BINFLAG'][j][-11])
    return Flagreads