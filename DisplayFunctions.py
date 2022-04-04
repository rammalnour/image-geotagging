import ProduitConvolution as pc
import FiltragePhoto as fp
import DisplayFunctions as df

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow
from skimage import exposure



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
    plt.show()

def showGrey(str,convul):
    # convul est un boolean qui permet d'afficher ou non l'histogramme de l'image filtrée

    image = imread(str, as_gray=True)
    imageHist(image)
    if convul:
        imageHist(pc.convuProduct(image))
    plt.show()

def booleanHist(L):
    # L est de la forme [[float0,boolean0],[float1,boolean1], etc.]

    varMaxFalse = 0
    varMinFalse = 0
    varMoyFalse = 0

    varMaxTrue = 0
    varMinTrue = 0
    varMoyTrue = 0

    for i in range(len(L)):
        if L[i][1]:
            varMaxTrue = max(varMaxTrue,L[i][0])
            varMinTrue = min(varMinTrue,L[i][0])
            varMoyTrue += L[i][0]
        else :
            varMaxFalse = max(varMaxFalse,L[i][0])
            varMinFalse = min(varMinFalse,L[i][0])
            varMoyFalse += L[i][0]

    # Préparation de la figure
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])

    etiquettes = ['False', 'True']
    valeurs = [varMaxFalse,varMaxTrue]
    print(valeurs)

    # Affichage des données
    ax.bar(etiquettes, valeurs)

    plt.title("Histogramme")  # Titre du graphique
    plt.ylabel('Variances')  # Titre de l'axe y
    plt.xlabel("L\' imag est-elle un mur ?")
    plt.show()  # Affichage d'une courbe


##
    # Préparation de la figure
    names = ['Mur', 'Pas mur']

    valuesMax = [varMaxFalse, varMaxTrue]
    valuesMin = [varMinFalse, varMinTrue]
    valuesMoy = [varMoyFalse, varMoyTrue]
    ic = [0.1,0.1]

    plt.bar(names, valuesMoy, color = "#A0AAE4", edgecolor="black",
            yerr=[0,0], ecolor = "#A0AAE4",capsize = 0)
    plt.bar(names, valuesMax, color = "#A0AAE4", edgecolor="black",
            yerr=[0,0], ecolor = "#A0AAE4",capsize = 0)
    plt.bar(names, valuesMin, color = "#A0AAE4", edgecolor="black",
            yerr=[0,0], ecolor = "#A0AAE4",capsize = 0)

    plt.show()







