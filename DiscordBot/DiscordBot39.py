from headless_browser_vm import GetRepIA
from config import TOKEN, ListNum
import discord
import random
import math
import numpy as np

Lregions=[
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

def get_score(path, user):
    """
    - path : String
    - user : discord.user.User

    renvoie le score de "user" dans la base de données placée en "path"
    """
    file = open(path, 'r')
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        line = lines[i]
        line = line.strip()
        line = line.split(" ")
        name = line[0]
        if name == str(user):
            return int(line[1])

    # is user not in database we add said user

    file = open(path, "a")
    file.write(str(user) + " 0\n")
    file.close()
    return 0


def set_score(path, user, score):
    """"

    - path : String
    - user : discord.user.User
    - score : int

    fixe le score de 'user' à la valeur 'score' dans la bdd placée en 'path'

    """

    file = open(path, 'r')
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        line = lines[i]
        line = line.strip()
        line = line.split(" ")
        name = line[0]

        if name == str(user):
            indiceuser = i

    file = open(path, "w")
    for k in range(indiceuser):
        line = lines[k]
        file.write(line)

    file.write(str(user) + " {} \n".format(score))

    for k in range(indiceuser+1, len(lines)):
        line = lines[k]
        file.write(line)

    file.close()


def update(path, user, add):
    """"
    - path : String
    - user : discord.user.User
    - add : int

    ajoute "add" au score de "user" dans la BDD placée en "path"
    appelle get_score et set_score
    """
    score = get_score(path, user)
    score += add
    set_score(path, user, score)


def getloc(num):
    """
    num : int
    num doit être compris entre 0 et 99

    renvoie l'indice de la région associé au numéro num"""

    file = open("./reg99.txt")
    lines = file.readlines()
    line = lines[num].strip()
    return Lregions.index(line)


def get_REG_IA(path):
    """
    - path : String
    path contient le chemin d'accès a l'image qu'on soumet a l'IA

    renvoie la région correspondant au choix de l'IA

    """
    # renvoie la région prédite par L'IA
    L = GetRepIA(path)
    i = np.argmax(np.array(L))
    return Lregions[i]


async def geoguess(msg, stage):

    """
    msg : discord.message.Message
    stage : int (0 ou 1)


    lance une partie de geoGuess
    """

    content = msg.content[8:]

    if stage == 0:
        # si le stage vaut 0 on montre l'image et invite le joueur a répondre
        global numImg
        numImg = random.choice(ListNum)
        print(numImg)
        path_img = "/home/nferet/DiscordBot/Images/img{}.png".format(numImg)

        await Confirm(msg, "Lancement de la partie, veuillez patienter Quelques instants")
        global region_ia
        region_ia = get_REG_IA(path_img)
        await msg.channel.send("Dans quelle région de France a été prise cette photo ?", file=discord.File(path_img))
        await Confirm(msg, "??guess NomRegion pour répondre")
        await Confirm(msg, "??stop pour arreter")
        return 1

    if stage == 1:
        # a l'étape 1 on attend encore la réponse du joueur

        print(content)

        try:
            indice = Lregions.index(content)

        except ValueError:
            # si la région proposée n'est pas valide
            await Confirm(msg, "Votre région n'est pas valide, elle doit être un des suivants : {}".format(Lregions))
            return 0

        print("loc=", getloc(numImg))

        if indice == int(getloc(numImg)):
            # si la région propose est la bonne on maj le score et on annonce au joueur qu'il a gagné, on lui affiche aussi la prédiction de l'IA (correcte ou non)
            update("/home/nferet/DiscordBot/scores.txt", msg.author.id, 1)

            await Confirm(msg, "Bien joué !")
            await Confirm(msg, "L'ia avait prédit : {}".format(region_ia))
            return -1  # on renvoie -1 pour revenir a l'état 0 au prochain appel de geoGuess

        await Confirm(msg, "Non, ce n'est pas cette région :( ")
        # si la region n'est pas la bonne, on reste a la même étape (nouvel essai de joueur)
        return 0


async def Confirm(msg, txt):
    """
    - txt : String
    - msg : discord.message.Message

    envoie le message 'txt' dans le canal du message recu
    """
    await msg.channel.send(txt)


async def showLeaderboard(path, msg, nblines=10):
    """
    - path : String, chemin de la BDD
    - msg : discord.message.Message
    - nblines : int, nombre de lignes du tableau a afficher

    affiche le Leaderboard par odre décroissant de score
    (score = nombre de réussite au jeu geoGuess)
    """

    def f(line):
        return -1*int(line.strip().split(" ")[1])

    file = open(path, "r")
    lines = file.readlines()
    print(lines)
    file.close()

    lines.sort(key=f)
    nblines = min(len(lines), nblines)
    for i in range(nblines):
        infos = lines[i].strip().split(" ")
        id, score = infos[:2]
        try:
            username = await client.fetch_user(id)
            await Confirm(msg, str(username) + " : " + score)
        except (discord.errors.NotFound, discord.errors.HTTPException) as e:
            # si le joueur n'est pas sur le serveur
            await Confirm(msg, "Joueur Inconnu : "+score)


if __name__ == '__main__':
    compteur = 0
    path = "./scores.txt"
    client = discord.Client()

    @client.event
    async def on_ready():
        print("Bot is running")

    @client.event
    async def on_message(msg):
        userid = msg.author.id
        username = str(await client.fetch_user(userid))
        content = msg.content.lower()  # rendre les commandes non if content==-sensitive
        tmp = content.split(" ")
        command = tmp[0]
        global compteur

        # on ne veut pas que le bot interagisse avec ses propres messages
        if str(userid) == "967730112999071784":
            return None
        # if not command
        if content[:2] != "??":
            return None
        if command=="ping":
            await Confirm(msg,"Pong !")

        # geoguess
        if content == '??play' or (compteur > 0 and content[:7] == "??guess") or content == "??stop":
            if content == "??stop":
                await Confirm(msg, "Dommage !")
                compteur = 0

            else:
                rep = await geoguess(msg, compteur)
                compteur += rep  # 0 ou 1, ( next step ou non)

        if command == "??showleader":
            # appelle showleaderbord avec les arguments correspondants
            lenght = math.inf
            if len(tmp) == 2:
                try:
                    lenght = int(tmp[1])
                except ValueError:
                    await Confirm(msg, "Argument invalide ignoré")

            await showLeaderboard(path, msg, nblines=lenght)

        if command == "??score":
            if len(tmp) == 1:
                await Confirm(msg, "Ton score est :{}".format(get_score(path, str(msg.author.id))))

            else:
                id = content.split(" ")[1][2:-1]
                print(id)
                try:
                    x = await client.fetch_user(id)
                    print(x)
                    score = get_score(path, id)
                    await Confirm(msg, "Son score est:" + str(score))

                except (discord.errors.HTTPException, discord.errors.NotFound) as e:
                    await Confirm(msg, "User not found")

        if content == "??help":
            # affiche la liste des commandes possibles
            txt = "Liste des commandes : score, showleader, play, help, ping"
            await Confirm(msg, txt)

    client.run(TOKEN)
