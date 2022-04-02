from skimage.io import imread
from skimage.io import imshow
from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
import PIL
from skimage import io
import ProduitConvolution as pc


#im = np.where(image1_Gray>128/256, 0, 1)
#imshow(im, cmap=plt.get_cmap('gray'))
#fig += 1

def imageHist(image):
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

def imageHistBis(str):

    image = io.imread(str)

    #_ = plt.hist(image.ravel(), bins = 256, color = 'Orange', )
    _ = plt.hist(image[:, :, 0].ravel(), bins = 256, color = 'Red', alpha = 0.5)
    _ = plt.hist(image[:, :, 1].ravel(), bins = 256, color = 'Green', alpha = 0.5)
    _ = plt.hist(image[:, :, 2].ravel(), bins = 256, color = 'Blue', alpha = 0.5)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
  #plt.show()

def detectWall(image,seuil,eps):

    n,p = np.shape(image)
    count = [0]*256
    for i in range(n):
        for j in range(p):
            count[int(image[i,j]*255)] += 1

    iMax = count.index(max(count))
    compteur = 0
    borneSup = min(iMax+eps,256)
    if iMax-eps < 0 :
        borneInf = 0
    else :
        borneInf = iMax - eps

    for i in range(borneInf,borneSup):

        compteur += count[i]
    compteur *= 1/(n*p)
    if compteur > seuil:

        return True
    else :

        return False

def showGrey(str,convul):
    # convul est un boolean
    plt.close()

    fig=1
    image = imread(str, as_gray=True)
    plt.figure(fig)
    imageHist(image)
    if convul:
        imageHist(pc.convuProduct(image))
    plt.show()

## Tests

seuil = 0.7
eps = 20
fig = 0
L=[]

for i in range(2,250):
    print(i)

    string = 'img' + str(i) + '.png'
    try :
        image = imread(string, as_gray=True)
        if detectWall(image,seuil,eps):
            print("oui")
            fig += 1
            image = imread(string, as_gray=True)
            plt.figure(fig)
            imageHist(image)
            plt.show()

            L.append(True)
            print(i)
        else :
            L.append(False)

    except :
        1+1




plt.close()
fig=0

str1='img28.png'
str2='img29.png'
str3='img52.png'
str4='img49.png'
#showGrey(str1,True)
#showGrey(str2,True)
showGrey(str3,True)
#showGrey(str4,True)

































