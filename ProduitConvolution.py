# Produit de Convultion

from skimage.io import imread, imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io

def convuLocal(portionImage,filtre):
    # portionImage est de même dimension que filtre

    n,p = np.shape(portionImage)
    somme = 0
    if(n,p == np.shape(filtre)):

        for i in range(n):
            for j in range(p):
                somme += filtre[i][j]*portionImage[i][j]
    return somme

def convuProduct(image):
    # Dans le cas où dimFiltre = 3

    n,p = np.shape(image)

    dimFiltre = 3
    filtre = np.array([[-1,0,1]]*dimFiltre)
    matrice = np.zeros((n,p))
    halfDimFiltre = int(dimFiltre/2)

    for i in range(1,n-1):
        for j in range(1,p-1):

            portionImage=np.zeros([dimFiltre,dimFiltre])
            for l in range(dimFiltre):

                L = image[i+halfDimFiltre-l][j-halfDimFiltre :j+halfDimFiltre +1]
                portionImage[l]=L

            resij = convuLocal(portionImage,filtre)
            matrice[i][j]+=resij
    L=[]
    for i in range(1,n-1):
        L.append(matrice[i][1:-1])
    return np.array(L)





























