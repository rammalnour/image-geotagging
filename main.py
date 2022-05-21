import ProduitConvolution as pc
import FiltragePhoto as fp
import DisplayFunctions as df

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow

import shutil



plt.close()

# -------- Constantes --------
chemin = "../ImagesBDD/"
cheminBDD = 'C:\\Users\\utilisateur\\Documents\\Télécom SudParis\\Cours S6\DEV Info\\ImagesBDD'
fig = 0
L=[]
Lvar=[]

# -------- Variables --------

seuil = 0.7 # Seuil à parir duquel on considère que l'image est un mur
seuilVar = 0.03
eps = 20 # Marge d'acceptabilité des couleurs
iterationsFin = 20000
# Afficher ou non l'image et histogramme de chaque mur
cond = False

# -------- Tests | Cellule 1 --------
for i in range(iterationsFin):
    string = chemin + 'img' + str(i) + '.png'

    try :
        image = imread(string, as_gray=True)
        Lvar.append(np.var(image))

        if fp.detectWall(image,seuil,eps):

            if cond : # Afficher les images et histgrammes de chaque mur ?
                image = imread(string, as_gray=True)
                df.imageHist(image)

            L.append(True)
            cheminBinImage = str(cheminBDD+ '\\Murs\\img'+ str(i) + '.png')
            cheminBDDImage = str(cheminBDD+ '\\img'+ str(i) + '.png')
            shutil.move(cheminBDDImage, cheminBinImage)
        else :
            L.append(False)

    except : # Si la photo n'existe pas
        L.append(False)

Ltrie1 = L.copy()


L = [False]*iterationsFin

for i in range(len(L)):

    if not L[i]:

        string = chemin + 'img' + str(i) + '.png'
        try : # Si la photo existe
            image = imread(string, as_gray=True)
            imageConvu = pc.convuProduct(image)
            if fp.detectVar(imageConvu,seuilVar):
                if cond : # Afficher les images et histgrammes de chaque mur ?
                    image = imread(string, as_gray=True)
                    df.imageHist(image)

                cheminBinImage = str(cheminBDD+ '\\Murs\\img'+ str(i) + '.png')
                cheminBDDImage = str(cheminBDD+ '\\img'+ str(i) + '.png')
                shutil.move(cheminBDDImage, cheminBinImage)
                L[i] = True
        except : # Si la photo n'existe pas
            pass
