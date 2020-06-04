#!/usr/bin/env python3

"""

    Auteur : Xavier Grand
    Date : 05/01/2020
    But du programme : transforme un entier en bianire
    Entrée : entier.
    Sortie : binaire.

"""

""" Fonction de conversion en binaire """
""" Cette fonction sera utilisée pour binariser le FLAG pour rendre sa lecture plus directe """

def bin(n):
    """Convertit un nombre en binaire"""
    q = -1
    res = ''
    while q != 0:
        q = n // 2
        r = n % 2
        res = str(r) + res
        n = q
    while len(res) < 11 :
        res = '0' + res
    return res

# print("99 en binaire donne : " + str(bin(int('99'))))
# print("77 en binaire donne : " + str(bin(int('77'))))
# print("141 en binaire donne : " + str(bin(int('141'))))