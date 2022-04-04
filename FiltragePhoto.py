from skimage.io import imread
from skimage.io import imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io
import ProduitConvolution as pc


def detectWall(image,seuil,eps):
    # return un boolean répondant à la question suivante "Est-ce que l'image est un mur ?"

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

    for i in range(borneInf,borneSup):

        compteur += count[i]
    compteur *= 1/(n*p)
    if compteur > seuil: # Les pixels sont quasi tous à peu près de la même couleur

        return True
    else :

        return False

def detectVar(image,seuil):

    if np.var(image) < seuil:

        return True # C'est un mur
    else :

        return False

def concatenation(L1,L2):

    if len(L1) == len(L2):
        res=[]
        for i in range(len(L1)):
            res.append([L1[i],L2[i]])
    return res

def booleanHist(L):
    # L est de la forme [[float0,boolean0],[float1,boolean1], etc.]

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









