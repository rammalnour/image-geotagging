import ProduitConvolution as pc
import FiltragePhoto as fp
import DisplayFunctions as df

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imshow

import shutil


# Test

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
    #print(i)

    print(i)
    string = chemin + 'img' + str(i) + '.png'

    try : # Si la photo existe
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
            print(i)
        else :
            L.append(False)

    except : # Si la photo n'existe pas
        L.append(False)

Ltrie1 = L.copy()
print("--------")

L = [False]*iterationsFin

for i in range(len(L)):
    #print(i)

    if not L[i]:

        string = chemin + 'img' + str(i) + '.png'

        try : # Si la photo existe
            image = imread(string, as_gray=True)
            print("-----")
            print(i)
            print(np.var(image))
            imageConvu = pc.convuProduct(image)
            print(np.var(imageConvu))

            if fp.detectVar(imageConvu,seuilVar):
                print(True)
                if cond : # Afficher les images et histgrammes de chaque mur ?
                    image = imread(string, as_gray=True)
                    df.imageHist(image)

                cheminBinImage = str(cheminBDD+ '\\Murs\\img'+ str(i) + '.png')
                cheminBDDImage = str(cheminBDD+ '\\img'+ str(i) + '.png')
                shutil.move(cheminBDDImage, cheminBinImage)
                L[i] = True

        except : # Si la photo n'existe pas
            1+1


#print(Ltrie1)
#print("-------")
#print(L)

# -------- Tests | Cellule 1 --------

str1= chemin + 'img27.png'
str2= chemin + 'img28.png'
str3= chemin + 'img52.png'
str4= chemin + 'img49.png'
image = imread(str4,as_gray=False)
#df.showGrey(str4,True)
#df.showGrey(str2,True)
#df.showGrey(str3,True)
#df.showGrey(str4,True)

image27 = imread(str1, as_gray=True)
image28 = imread(str2,as_gray=True)
#print(np.var(image27))
#print(np.var(image28))
imageGrey27 = pc.convuProduct(image27)
imageGrey28 = pc.convuProduct(image28)
print('-----')
print(np.var(imageGrey27))
print(np.var(imageGrey28))
plt.show()









