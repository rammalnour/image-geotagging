# Produit de Convultion

from skimage.io import imread, imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io



def convuLocal(portionImage,filtre):
    """
    - portionImage : np.ndarray
    - filtre : np.ndarray

    - Génère ValueError si les matrices ne sont pas de même taille

    Renvoie le produit le convolution entre les deux matrices
    """


    if np.shape(portionImage)!=np.shape(filtre):
        raise ValueError("Matrices de dimensions différentes")

    else:
        n,p = np.shape(portionImage)
        somme = 0
        for i in range(n):
            for j in range(p):
                somme += filtre[i][j]*portionImage[i][j]

        return somme



def convuProduct(image):
    """
    - image : np.ndarray de dimension n,p

    renvoie le produit de convolution de image par le filtre f de dim(3x3)

    f = -1, 0, 1,
        -1, 0, 1,
        -1, 0, 1,

    """
    n,p = np.shape(image)

    dimFiltre = 3                           # Filtre est de la forme :
    filtre = np.array([[-1,0,1]]*dimFiltre) #    -1 0 1
    matrice = np.zeros((n,p))               #    -1 0 1
    halfDimFiltre = int(dimFiltre/2)        #    -1 0 1

    # On applique le produit de convolution à chaque matrice extraite 3x3
    for i in range(1,n-1): # On parcourt toute la matrice sauf les bords
        for j in range(1,p-1):
            portionImage=np.zeros([dimFiltre,dimFiltre])

            # Création de la matrice extraite
            for l in range(dimFiltre):
                L = image[i+halfDimFiltre-l][j-halfDimFiltre :j+halfDimFiltre +1]
                portionImage[l]=L

            # On calcule le produit de convolution entre la matrice extraite et le filtre
            resij = convuLocal(portionImage,filtre)
            matrice[i][j]+=resij

    # On enlève tous les bords pour avoir une matrice de dimension (n-1)x(p-1)
    L=[]
    for i in range(1,n-1):
        L.append(matrice[i][1:-1])
    return np.array(L)
