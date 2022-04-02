import ProduitConvolution as pc
import FiltragePhoto as fp
import matplotlib.pyplot as plt

# Test

plt.close()

# -------- Constantes --------
chemin = "../ImagesBDD/"
fig = 0
L=[]

# -------- Variables --------
seuil = 0.7 # Seuil à parir duquel on considère que l'image est un mur
eps = 20 # Marge d'acceptabilité des couleurs

# Afficher ou non l'image et histogramme de chaque mur
cond = False

# -------- Tests --------
for i in range(2,250):
    print(i)

    string = chemin + 'img' + str(i) + '.png'
    try : # Si la photo existe
        image = imread(string, as_gray=True)
        if detectWall(image,seuil,eps):

            if cond : # Afficher les images et histgrammes de chaque mur ?
                fig += 1
                image = imread(string, as_gray=True)
                plt.figure(fig)
                imageHist(image)
                plt.show()

            L.append(True)
            #print(i)
        else :
            L.append(False)

    except : # Si la photo n'existe pas
        1+1

fig=0

str1= chemin + 'img28.png'
str2= chemin + 'img29.png'
str3= chemin + 'img52.png'
str4= chemin + 'img49.png'
#fp.showGrey(str1,True)
#fp.showGrey(str2,True)
#fp.showGrey(str3,True)
#fp.showGrey(str4,True)