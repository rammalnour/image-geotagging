import gc
import numpy as np
from PIL import Image
import tensorflow as tf

class Geoguessr:
    def __init__(self,
                 inputShape=(300,600,3), gridCount=12,
                 hidden1=256, hidden2=512):


        # load restnet model
        restnet = tf.keras.applications.resnet50.ResNet50(include_top=False,
                                                            weights='imagenet',
                                                            input_shape=inputShape)
        self.model = tf.keras.models.Sequential()
        self.model.add(restnet)

        # freeze resnet model

        self.model.layers[0].trainable = False

        self.model.add(tf.keras.layers.Conv2D(hidden1, (3, 3), activation='relu',
                                                input_shape=inputShape))
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
        self.model.add(tf.keras.layers.Dropout(0.25))
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dense(hidden2, activation='relu'))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(tf.keras.layers.Dense(gridCount, activation="softmax"))

        self.model.compile(loss=tf.keras.losses.categorical_crossentropy,
                            optimizer=tf.keras.optimizers.Adam(),
                            metrics=['categorical_accuracy'])

Lreg=[
"Auvergne-Rhône-Alpes",
"Bourgogne-Franche-Comté",
"Bretagne",
"Centre-Val de Loire",
"Grand Est",
"Hauts-de-France",
"Normandy",
"Nouvelle-Aquitaine",
"Occitanie",
"Pays de la Loire",
"Provence-Alpes-Côte d'Azur",
"Île-de-France"]

def getReg(file):
    """obtient la région d'un file InfoX.txt"""
    K= 2
    lines=file.readlines()
    file.close()
    Goodlines=[]
    for line in lines:
            if "formatted" in line:
                Goodlines.append(line)

    Good=Goodlines[-K].split(":")[1].split(",")[0][2:]
    return Good

def transfo(i,k):
    L=[0]*k
    L[i]=1
    return L

geoModel = Geoguessr().model
print(geoModel.summary)

step=200
nbmax=19999

pathimg="../input/imagesfrance/"
pathinfo="../input/infosfrance/Infos/"

Lx=[]
Ly=[]
  for batch in range(0,nbmax,step):

      for i in range(batch,batch+step):
          try:
              img0=Image.open(pathimg+"img{}.png".format(i))
              img=np.reshape(img0,[300,600,3])
              img0.close()
              info=open(pathinfo+"Info{}.txt".format(i))
              reg=getReg(info)
              info.close()
              indice=Lreg.index(reg)

              Lx.append(np.array(img))
              Ly.append(transfo(indice,12))

          except: # il manque des images aores nettoyage mais c'est parfaitement normal
              pass

      if len(Ly)!=0:
            Lx=np.array(Lx,dtype="float64")
            Ly=np.array(Ly)
            geoModel.fit(Lx,Ly,batch_size=4)
            del Lx
            del Ly
            gc.collect()
            Lx=[]
            Ly=[]
            
            

!pip install tensorflowjs
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(geoModel,"./kaggle/working/ModelJS")


def getCorr():
    dico=dict()
    for i in range(19999):
        try:
            info=open(pathinfo+"Info{}.txt".format(i))
            reg=getReg(info)
            info.close()
            dico[i]=reg
        except (FileNotFoundError, ValueError) as e:
            pass
    return dico

dico=getCorr()


#evaluation des perfs

Lx=[]
Ly=[]
for i in range(19999-2000,19999):
    try:
                img0=Image.open(pathimg+"img{}.png".format(i))
                img=np.reshape(img0,[300,600,3])
                img0.close()
                info=open(pathinfo+"Info{}.txt".format(i))
                reg=getReg(info)
                info.close()
                indice=Lreg.index(reg)
    
                Lx.append(np.array(img))
                Ly.append(transfo(indice,12))
    
            except:
                pass # pas de soucis s'il manque une image
                
geoModel.evaluate(Lx,Ly)
