import ProduitConvolution as pc
import FiltragePhoto as fp
import DisplayFunctions as df

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
from skimage import exposure



def imageHist(image):
    # Génère et affiche l'histogramme d'une image (nuance de gris ou normal)
    # image est un array

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
    plt.show()




def showGrey(str,bol):
    # Affiche l'histogramme d'une image et si bol = True, d'une image filtrée
    # bol est un boolean qui permet d'afficher ou non l'histogramme de l'image filtrée

    image = imread(str, as_gray=True)
    imageHist(image)
    if bol:
        imageHist(pc.convuProduct(image))
    plt.show()








