#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : affiche un résumé des informations des alignements (ou mapping) de lectures (ou reads) issues
    du séquençage d’ADN sur une séquence dite de référence.
    Entrée : Fichier SAM + Fichiers de configuration et data.
    Sortie : Fichier SAM filtré, fichier de résultats, affichage ?

"""

#####################################################################################################################
##############################""" Partie import des fonctions nécessaires à Samy """#################################
#####################################################################################################################

import re, os, time
from argparse import ArgumentParser

from lib.saveAllData import saveAllData
from lib.dicoFlag import dicoFlag
from lib.wait import wait
from lib.filterReads import filterReads

#####################################################################################################################
##########################""" Partie Prise en compte des paramètres et du type d'OS """##############################
#####################################################################################################################

parser = ArgumentParser()
parser.add_argument("file", help="Input SAM file to parse.")
parser.add_argument("-a", "--all", action="store_true", help="Compute and display all statistics.")
parser.add_argument("-p", "--pairs", action="store_true", help="Compute and display pairs statistics.")
parser.add_argument("-i", "--info", action="store_true", help="Display header information.")
parser.add_argument("-sA", "--saveAll", action="store_true", help="Save all filtered pairs (MapNotMap & MapPartMap) in new sam files.")
parser.add_argument("-sMNM", "--saveMapNotMap", action="store_true", help="Save filtered MapNotMap pairs in a new sam file.")
parser.add_argument("-sMPM", "--saveMapPartMap", action="store_true", help="Save filtered MapPartMap pairs in a new sam file.")

args = parser.parse_args()

#####################################################################################################################
#########################################""" Fichiers Tests """######################################################
#####################################################################################################################

""" Test de fichier de travail en Système Linux """

# chemin = "/home/e20190010178/Documents/HMIN113M/Projet/exemple.sam" # test avec un fichier d'exemple
# chemin = "/home/e20190010178/Documents/HMIN113M/Projet/mapping.sam" # test avec le sam un peu plus gros

""" Test de fichier de travail en Système Windows """

#chemin = "C:/Users/Xï@V/Desktop/Master_BCD/HMIN113M/Projet/exemple.sam"  # petit fichier sous windows
#chemin = "C:/Users/Xï@V/Desktop/Master_BCD/HMIN113M/Projet/exemple1l.sam"  # petit fichier sous windows
#chemin = "C:/Users/Xï@V/Desktop/Master_BCD/HMIN113M/Projet/mapping.sam"  # gros fichier sous windows
#chemin = "C:/Users/Xï@V/Desktop/Master_BCD/HMIN113M/Projet/realSam.sam"  # ultra gros fichier de JayJay sous windows

#####################################################################################################################
##""" I. Lecture du fichier SAM au final, le nom du fichier sera passer en paramètre dans la ligne de commande """###
#####################################################################################################################

## Passer le fichier en paramètre

chemin = args.file

""" recuperation du nom de fichier sam """

nomfichierSAM = re.search(".*(/(.+).sam)$", chemin) # si le fichier n'a pas d'extension, il va y avoir un problème... Rajouter un if en amont...
# print(nomfichierSAM.group(2))

""" Parsing du fichier sam en dictionnaire """

reference = "unknown"
longueurRef = "unknown"
prog = "unknown"
version = "unknown"

allread = {}
with open(chemin, "r") as f:
    cpt = 0
    print("SAM file opening...")
    for line in f.readlines():
        if cpt == 0 and not re.search("^@", line) :
            print("WARNING!!! No header in input file. Input file may be corrupted.")
            wait()
        if re.search("^@", line):  # si ma ligne commence par @ alors je traite le header
            # print(line) # Balise pour voir les lignes header
            if (re.search("SN:(.*)\t", line)):
                reference = re.search("SN:(.*)\t", line).group(1) # récupère le nom du génome de référence
            if (re.search("LN:([0-9]*)", line)):
                longueurRef = re.search("LN:([0-9]*)", line).group(1) # récupère la longueur de la ref en bp
            if (re.search("ID:(.*)\tPN:", line)):
                prog = re.search("ID:(.*)\tPN:", line).group(1) # récupère le nom du programme d'alignement
            if (re.search("VN:(.*)\t", line)):
                version = re.search("VN:(.*)\t", line).group(1) # récupère la version du prog
        else:  # sinon je crée les objets dans un dictionnaire
            read = line.split("\t")
            if (len(read) < 11) :
                print("WARNING!!! Number of fields in input file is not compliant. Input file may be corrupted.")
                wait()
            saveAllData(read, allread)
        cpt += 1

# print("Infos fichier SAM :\n" + "Reference : " + reference + "\nLongueur de la reference : " + longueurRef + "\nProgramme allignement : " + prog + "\nVersion du Programme : " + version)
# print(allread) # vérification du remplissage du dictionnaire de reads
# print(allread[read[0]]) # Affichage de la structure de allread sur le premier read

#####################################################################################################################
########################################""" II. Traduction des codes Flag """########################################
#####################################################################################################################

tot = len(allread.keys()) - len(allread.keys()) % 10
if (tot == 0) :
    tot = 10

""" lecture de flag """

DicoSingle = {}
Dicofirst = {}
Dicosecond = {}
dicoFlag(allread, tot, DicoSingle, Dicofirst, Dicosecond)

# print(Dicofirst['Clone1-350000'])
# print(Dicosecond['Clone1-350000'])

"""Comptage des reads - comptage ligth"""

Map = 0 #utilise
nbSingle = 0 #utilise
nbtotPaires = 0 #utilise
MapNotmap = 0 # PAS utilise
notMap = 0 #utilise
nbFw = 0 # PAS utilise
nbRv = 0 # PAS utilise

for item in allread.keys() :

    """Paired-end or Single-end"""

    if Dicofirst[item]['paired'] == 0 :
        nbSingle += 1
    if Dicosecond[item]['paired'] == 0 :
        nbSingle += 1
    if Dicofirst[item]['paired'] == 1 :
        nbtotPaires += 1

    """Mapped or Not-Mapped"""

    if Dicofirst[item]['unmap'] == 1 :
        notMap += 1
    else :
        Map += 1
    if Dicosecond[item]['unmap'] == 1 :
        notMap += 1
    else :
        Map += 1

    """Forward or Reverse"""

    if Dicofirst[item]['strand'] == 0 :
        nbFw += 1
    else :
        nbRv += 1
    if Dicosecond[item]['strand'] == 0 :
        nbFw += 1
    else :
        nbRv += 1

    """Reads Pairs Mapped/NotMapped"""

    if Dicofirst[item]['unmap'] != Dicosecond[item]['unmap'] :
        MapNotmap += 1

#####################################################################################################################
#"""III. extraire les reads ”mal mappés”, Pour ce faire, vous allez devoir sélectionner les lignes du fichier SAM en#
############################################### fonction du CIGAR """################################################
#####################################################################################################################

listeNotMap = [] # Création d'une nouvelle liste des reads non mappés
listeMappe = [] # Création d'une nouvelle liste des reads mappés
listePartMap = [] # Création d'une nouvelle listes des reads partiellement mappés
listeMapNotMap = [] # Création d'une nouvele listes des couples de reads F et R Mappé/non-mappé
listeMapPartMap = [] # Création d'une nouvelle listes des couples de reads F et R Mappé/Partiellement-mappé
listeFullyMap = [] # Création d'une nouvelle listes de reads qui mappent à 100% de leur longueur, entièrement mappés

""" Création des listes de reads en fonction des infos du FLAG"""

i = 0
print("SAM file parsing...")
time.sleep(1)
for reads in allread.keys() :
    i = i + 1
    compteur = (i / tot) * 100
    if ((compteur % 5) == 0):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(str(round(compteur)) + " %")
    # print(allread[reads]['BINFLAG'][0][-3])
    # print(allread[reads]['BINFLAG'][0])
    # print(reads) # Clone1-350000
    for j in [0,1] :

        """First or Second read"""

        if (int(allread[reads]['BINFLAG'][j][-7]) == 1) : # Is the first read ?
            fr = '_1'
        elif (int(allread[reads]['BINFLAG'][j][-8]) == 1) : # Is the second read ?
            fr = '_2'

        """Mapped or Not Mapped"""

        if (int(allread[reads]['BINFLAG'][j][-3]) == 1) : # Is the read mapped ? 1 = notmapped
            listeNotMap.append(reads + fr)

        else: # if the read is mapped...
            listeMappe.append(reads + fr)
            if (int(allread[reads]['BINFLAG'][j][-4]) == 1 and reads not in listeMapNotMap) : # mate is mapped ? # 1 = mate mapped.
                listeMapNotMap.append(reads) # Read Pair mapped and not mapped
            if (re.search('^[0-9]+M$', allread[reads]['CIGAR'][j])): # Among Maped reads, CIGAR 100% M ? = fully mapped ?
                listeFullyMap.append(reads + fr)
            else: # Quels sont les reads partiellement mappés ? If not XXXM => Partially mapped.
                listePartMap.append(reads + fr)
                if (re.search('^[0-9]+M$', allread[reads]['CIGAR'][abs(j - 1)])) : # mate is XXXM ?
                    listeMapPartMap.append(reads)

#print(listeNotMap)
#print(listeMappe)

###############################################################################################################
##########################################""" Filtration """###################################################
###############################################################################################################

"""Creation d'un fichier sam de sortie filtré avec les paires de reads MapNotMap"""

if args.saveMapNotMap or args.saveAll :
    outputFile = "MapNotMap.sam"
    filterReads(chemin, outputFile, listeMapNotMap, tot)

"""Creation d'un fichier sam de sortie filtré avec les paires de reads MapPartMap"""

if args.saveMapPartMap or args.saveAll :
    outputFile = "MapPartMap.sam"
    filterReads(chemin, outputFile, listeMapPartMap, tot)

#####################################################################################################################
#"""IV. La dernière étape sera d’afficher le résumé des résultats obtenues, comme le nombre de reads et paires de####
###########chaque catégorie. Les sorties graphiques ne sont pas nécessaires."""######################################
#####################################################################################################################

os.system('cls' if os.name == 'nt' else 'clear') # netoyage du terminal

if args.info or args.all:
    print("Computed SAM file : " + nomfichierSAM.group(2))
    print('')
    print("SAM file header information :\n" + "Reference : " + reference + "\nReference length : " + longueurRef + "\nAllignment tool : " + prog + "\nVersion : " + version)
    print('')

print("Basic Statistics :")
print("Total number of reads : " + str(len(Dicofirst.keys()) + len(Dicosecond.keys())+ nbSingle))
print("Total number of read pairs : " + str(nbtotPaires))
print("Number of Single reads (non-paired) : " + str(nbSingle))
print("")
print("Mapping results :")
print("Number of mapped reads : " + str(Map))
print("Number of unmapped reads : " + str(notMap))
print("Number of partially mapped reads : " + str(len(listePartMap)))
print("Number of fully mapped reads : " + str(len(listeFullyMap)))

if args.pairs or args.all:
    print("")
    print("Read pairs statistics :")
    print("Sum of perfectly mapped + partially mapped reads : " + str(len(listePartMap) + len(listeFullyMap)))
    print("Number of read pairs with one mapped and not the other (MapNotMap) : " + str(len(listeMapNotMap)))
    print("Number of read pairs with one fully mapped and the other is partially mapped (MapPartMap) : "+ str(len(listeMapPartMap)))

###############################################################################################################
###############################################################################################################
########################################""" Miscellaneous """##################################################
###############################################################################################################
###############################################################################################################

# Qname = []
# Flag = []
#
# with open(chemin, "r") as f:
#     for line in f.readlines():
#         if re.search("^@", line):  # si ma ligne commence par @ alors je traite le header
#             print("header")
#         else:  # sinon je crée les objets dans un dictionnaire
#             read = line.split("\t")
#             # print(read) # balise de test
#             # print(read[0]) # balise de test
#
#             Qname.append(read[0])
#             Flag.append(read[1])
#
# """ Comptage des différents codes Flag """
#
# Flagordered = []
#
# for i in (set(Flag)):
#     Flagordered.append(i)
#
# Flagordered.sort()
# print(Flagordered)
#
# print([(i, Flag.count(i)) for i in Flagordered])
#
# flgbin = []
# for flg in Flagordered :
#     flgbin.append(bin(int(flg)))
#
# print(flgbin)