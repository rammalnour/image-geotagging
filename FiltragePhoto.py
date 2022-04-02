from skimage.io import imread
from skimage.io import imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io
import ProduitConvolution as pc


def imageHist(image):
    # Génère l'histogramme d'une image

    _, axis = plt.subplots(ncols=2, figsize=(12, 3))
    if (image.ndim == 2):
        # Grascale image

        axis[0].imshow(image, cmap=plt.get_cmap('gray'))
        axis[1].set_title('Histogram')
        axis[0].set_title('Grayscale Image')
        hist = exposure.histogram(image)
        axis[1].plot(hist[0])
    else:
        # Color image

        axis[0].imshow(image, cmap='gray')
        axis[1].set_title('Histogram')
        axis[0].set_title('Colored Image')
        rgbcolors = ['red', 'green', 'blue']
        for i, mycolor in enumerate(rgbcolors):
            axis[1].plot(exposure.histogram(image[...,i])[0], color=mycolor)


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

def showGrey(str,convul):
    # convul est un boolean qui permet d'afficher ou non l'histogramme de l'image filtrée

    fig = 1
    image = imread(str, as_gray=True)
    plt.figure(fig)
    imageHist(image)
    if convul:
        imageHist(pc.convuProduct(image))
    plt.show()


































