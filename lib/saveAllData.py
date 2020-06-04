#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : Fonction de création du dictionnaire étendu, Parsing complet du fichier SAM
    Entrée : nom de read et dictionnaire.
    Sortie : dictionnaire contenant les informations du SAM.

"""
import re
from lib.bin import bin

def saveAllData(read, allread) :

    ListeHeader = ['QNAME', 'FLAG', 'RNAME', 'POS', 'MAPQ', 'CIGAR', 'RNEXT', 'PNEXT', 'TLEN', 'SEQ', 'QUAL', 'BINFLAG', 'NM:i:', 'MD:Z:', 'AS:i:',	'XS:i:']

    # read = ['Clone1-350000', 99, 'Reference', 658711, 27, '100M', '=', 658812, 201, 'CACCAACTTCAAGAAGCAGAAGAAGAACAACAACAATCCTAATCAGGATGAGAGGACTTGCTTTGTGTGTGGCCAAGTTGGTCATCTGGCTAGGAAGTGT', 'CCCCCGGGFGGGE1G>GGGGBGGGGGGG1GGGGGGGGGGGGGGGGGGGGGGGGGGDGGGGFGGGGGGGFGGGGGGGD=GGGG=GGGGGGEFGGGGGFGFG', 'NM:i:0', 'MD:Z:100', 'AS:i:100', 'XS:i:100', 'XA:Z:Reference,+486320,100M,0;Reference,+518199,98M2S,3;']

    if read[0] in allread :
        Listeflag = allread[read[0]][ListeHeader[1]]
        Listeflag.append(read[1])
        ListeBinFlag = allread[read[0]][ListeHeader[11]]
        ListeBinFlag.append(bin(int(read[1])))
        ListeCigar = allread[read[0]][ListeHeader[5]]
        ListeCigar.append(read[5])
        ListeMDZ = allread[read[0]][ListeHeader[13]]
        if (re.search("(MD:Z:(.*))", read[12])) :
            mdz = re.search("(MD:Z:(.*))", read[12]).group(2) # si il exite un MDZ
        else : # Si pas de MDZ
            mdz = ""
        ListeMDZ.append(mdz)
        allread[read[0]] = {ListeHeader[1] : Listeflag, ListeHeader[11] : ListeBinFlag, ListeHeader[5] : ListeCigar, ListeHeader[13] : ListeMDZ}

    else :
        Listeflag = []
        Listeflag.append(read[1])
        ListeBinFlag = []
        ListeBinFlag.append(bin(int(read[1])))
        ListeCigar = []
        ListeCigar.append(read[5])
        ListeMDZ = []
        if (re.search("(MD:Z:(.*))", read[12])):
            mdz = re.search("(MD:Z:(.*))", read[12]).group(2)  # si il exite un MDZ
        else:  # Si pas de MDZ
            mdz = ""
        ListeMDZ.append(mdz)
        allread[read[0]] = {ListeHeader[1] : Listeflag, ListeHeader[11] : ListeBinFlag, ListeHeader[5] : ListeCigar, ListeHeader[13] : ListeMDZ}

    return(allread)

# Structure de allread :
# allread['Clone1-350000'] = {'FLAG': ['99', '147'], 'BINFLAG': ['00001100011', '00010010011'], 'CIGAR': ['100M', '100M'], 'MD:Z:': ['100', '100']}
