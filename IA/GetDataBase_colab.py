""" Signs a URL using a URL signing secret """

import hashlib
import hmac
import base64
import urllib.parse as urlparse


def sign_url(input_url=None, secret=None):
    """ Sign a request URL with a URL signing secret.
      Usage:
      from urlsigner import sign_url
      signed_url = sign_url(input_url=my_url, secret=SECRET)
      Args:
      input_url - The URL to sign
      secret    - Your URL signing secret
      Returns:
      The signed request URL
  """

    if not input_url or not secret:
        raise Exception("Both input_url and secret are required")

    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()
  # Import PyDrive and associated libraries.


# This only needs to be done once in a notebook.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authenticate and create the PyDrive client.
# This only needs to be done once in a notebook.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


!mkdir /content/PRO3600_DATA
!mkdir /content/PRO3600_DATA/Images
!mkdir /content/PRO3600_DATA/Infos

from shapely import geometry

import urllib.parse as parse

import requests
import random

from PIL import Image
import io
import base64
import numpy as np
import time

API_KEY=""
secret=''

path="/content/PRO3600_DATA"
params='size=600x300&source=outdoor&radius=500'

Nb_img=20000 # on veut X images

def getcos():
    """
    renvoie -au hasard uniforme- un couple lat lon de reels bornés
    """
    point=geometry.Point((0,0))

    latmin=40
    latmax=51

    longmin=-2
    longmax=8
    while not point.within(France): #tant que le point généré n'est pas valide
      lat=random.random()
      long=random.random()

      lat = lat*(latmax-latmin)+ latmin
      long = long*(longmax-longmin)+ longmin # rd[0,1] -> rd[min,max]

      lat=round(lat,6)
      long=round(long,6) # on met le bon nombre de decimales
      point=geometry.Point(lat,long)

    return lat, long


def GetMetaRequete(address,params=params):
    """renvoie la requete __METADATA__
     utilisé pour savoir si la requet est valide ou non

     param = arg1=value1&arg2=value2    """

    url="https://maps.googleapis.com/maps/api/streetview/metadata?{}&location={}".format(params,address)

    url=url+"&key="+API_KEY # ajout de ka clé api a la requete

    signed_url=sign_url(url,secret) # on signe la requete

    req=requests.get(signed_url) # on envoie a l'api de metadonnées
    return req



def GetImage(req):
    """
    req étant composé de bits, on traduit en un array 'usuel"
    renvoie l'array
    """
    bits=req.content # on prend le contenu de la requete
    b=bits.strip()
    c=io.BytesIO(b) # on décode les bits
    img=Image.open(c)
    return np.array(img) # pour ensuite récupérer sous forme de matrice


def GetRequeteReverseGeo(lat,lng):
    """
    - lat : float
    - lng : float

    envoie une requete a l'api de reverse geocoding pour obtenir les infos sur l'endroit auquel correspondent les coordonées
    """

    url="https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}".format(lat,lng)
    url=url+"&key="+API_KEY

    req=requests.get(url) # pas besoin de signer l'url
    return req


def getaddress(geodata):
  """renvoie l'adresse associée a un objet geodata"""
  string = geodata.content.decode() # on recup le string a partir de la requete
  lines = string.split("\n") # on découpe le bloc  en lignes
  ok=True
  for line in lines:
    if "formatted_address" in line and ok: # on prend la 1ere occurence de la ligne formatted
      ok=False
      GoodLine=line

  GoodLine=GoodLine.split(":") # on découpe juste le bout qui nous interesse
  GoodLine=GoodLine[1][2:-2]
  GoodLine=GoodLine.split(" ")
  GoodLine=GoodLine[-2]+GoodLine[-1]


  return GoodLine # on renvoie l'adresse


def saveInfo(geodata,nameinfo):
  """enregistre les données geodata au format txt"""
  pathinfo=path+"/Infos/"+nameinfo
  string = geodata.content.decode()
  file = open(pathinfo,"w")
  file.write(string)
  file.close()


def saveimg(mat,nom):

    """
    - mat : np.ndarray

    enregistre la matrice mat sous forme d'image sous le nom "nom" au chemin "pathimg"
    """
    pathimg=path+"/Images/"
    img=Image.fromarray(mat)
    img.save(pathimg+nom)


def saveToDrive(pathimg,id):
  """
  enregistre l'image au chemin pathimg sur le drive, avec le nom pathimg
  """

  gfile = drive.CreateFile({'parents': [{'id': id}]}) #crée le fichier vide
  upload_file=pathimg
  gfile.SetContentFile(upload_file) # ajoute le contenu de pathimg au fichier
  gfile.Upload() #upload au drive


def GetRequeteFromAddress(address,params=params):
  """
  - address : String

  renvoie la resultat de la requete API a l'adresse donnée """
  address=parse.quote(address)
  url= "https://maps.googleapis.com/maps/api/streetview?{}&location={}".format(params,address)
  url=url+"&key="+API_KEY
  signed_url=sign_url(url,secret)
  req=requests.get(signed_url)
  return req


def main():

  compteur=0
  while compteur<Nb_img: # pour le nombre d'images voulues

    time.sleep(0.1) # on rajoute 0.1s de délai par précaution(?)
    lat,lng=getcos() # on genere un point sur la france
    print(lat,lng)

    geodata=GetRequeteReverseGeo(lat,lng) # on recup les geodonnées de l'api
    address=getaddress(geodata) # on extrait l'adresse

    print("Image : ",compteur , "Addresse : ", address)
    req=GetRequeteFromAddress(address) # on prend la street view

    img=GetImage(req) # on récup l'image

    # on enregistre sur le drive l'image et le fichier d'infos associé

    nameimg="img{}.png".format(compteur)
    nameinfo="Info{}.txt".format(compteur)

    saveimg(img,nameimg)
    saveInfo(geodata,nameinfo)

    ImageFolderID='1hPhwEse7OiL1-Q511pqwnJZYgDJsKpdE'
    saveToDrive(path+"/Images/"+nameimg,ImageFolderID)

    InfoFolderID = '1T_UlkbKyxbu6skvkb1AjhL_jEuLnCW7T'
    saveToDrive(path+"/Infos/"+nameinfo,InfoFolderID)
    print("Done")
    compteur+=1
    print(compteur)





def createPoly():
  """renvoie le polygone représentant la france"""
  Lpoints=[[43.525093, -1.134750],[42.741205, 2.447694],[43.888962, 2.987746],[43.894815, 6.840072],[46.605900, 5.612790],[48.774532, 7.390237],[50.630174, 2.315648],[49.137655, -0.284608],[49.585080, -1.555339],[48.608597, -1.188893],[48.608597, -1.188893],[46.346987, -0.413643]]
  PointList=[]
  for pt in Lpoints:
      PointList.append((pt[0],pt[1])) #on remplace les listes par des tuples

  poly=geometry.Polygon(PointList)
  return poly # on renvoie le polygone généré

France=createPoly()
main()


assert getcos()[0]<=51
