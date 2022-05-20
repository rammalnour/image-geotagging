import ProduitConvolution as pc

from skimage.io import imread
from skimage.io import imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io



def detectWall(image,seuil,eps):
    """
    - image : np.ndarray
    - seuil : float
    - eps : float

    renvoie un booleen valant True si l'image est un mur, selon un critère basé sur la prédominance d'une couleur sur les autres
    """
    n,p = np.shape(image)

    # Compte le nombre de pixels qu'il y a pour chaque nuance de gris
    count = [0]*256
    for i in range(n):
        for j in range(p):
            count[int(image[i,j]*255)] += 1

    # Détermine s'il y a une prédomiance d'une couleur sur le mur
    iMax = count.index(max(count)) # Nuance de gris du pixel le plus présent sur l'image en nuance de gris
    compteur = 0
    borneSup = min(iMax+eps,256)
    if iMax-eps < 0 :
        borneInf = 0
    else :
        borneInf = iMax - eps

    # Compte le nombre de pixel ayant une couleur entre [borneInf,borneSup]
    for i in range(borneInf,borneSup):
        compteur += count[i]
    compteur *= 1/(n*p) # Calul de la moyenne

    # Critère de prédominance
    if compteur > seuil: # Les pixels sont quasi tous à peu près de la même couleur
        return True
    else :
        return False



def detectVar(image,seuil):
    """
    - image : np.ndarray
    - seuil : float

    renvoie un booleen valant True si l'image est un mur, selon un critère basé sur la variance de l'image

    """
    # Critère de variance
    if np.var(image) < seuil:
        return True # On considère que l'image est un mur
    else :
        return False





def booleanHist(L):
    """
    - L : Liste,

    L est de la forme [[float0,boolean0],[float1,boolean1], ...]



    Permet de préparer des données pour faire un histogramme statistiques
    Utilisable pour des étudier les statistiques

    renvoie le couple de triplet [varMaxTrue,varMoyTrue/nbr,varMinTrue],[varMaxFalse,varMoyFalse/nbr,varMinFalse
    (notation : varMaxTrue = variance maximale tel qu'un mur est détecté)
    """
    varMaxFalse = 0
    varMinFalse = 10
    varMoyFalse = 0

    varMaxTrue = 0
    varMinTrue = 10
    varMoyTrue = 0

    nbr = len(L)

    for i in range(nbr):
        if L[i][1]:
            varMaxTrue = max(varMaxTrue,L[i][0])
            varMinTrue = min(varMinTrue,L[i][0])
            varMoyTrue += L[i][0]
        else :
            varMaxFalse = max(varMaxFalse,L[i][0])
            varMinFalse = min(varMinFalse,L[i][0])
            varMoyFalse += L[i][0]

    return [varMaxTrue,varMoyTrue/nbr,varMinTrue],[varMaxFalse,varMoyFalse/nbr,varMinFalse]




"""
def concatenation(L1,L2):
    # Sert juste à tester le code

    if len(L1) == len(L2):
        res=[]
        for i in range(len(L1)):
            res.append([L1[i],L2[i]])
    return res
"""
