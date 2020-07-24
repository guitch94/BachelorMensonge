#################################################################################################
# Auteur : Guillaume Blanco
#
# Date de dernière modification : 23.07.2020
#
# Description : Ce script contient différentes fonctions utile au script d'analyse
#				des données.
#
# Remarque nbMiniVideo est le nombre de "petites videos" que l'on veut prendre en compte
#################################################################################################
import numpy as np

from matplotlib import pyplot as plt, gridspec
from ExtractionDesDonnees.UtilExtract import ZONE_VISAGE, reductionBruit

NB_IMAGES = 15 # nombre de d'images par "petites vidéos"
NB_ZONE_VISAGE = 17


# récupère les résultats d'un fichier texte et les renvoie sous forme d'un tableau numpy
def recupResultats(path, videoName, nbMiniVideo = 10):

    fichier = open(path + videoName, "r")
    strRes = fichier.read()
    debutMultiTab = 0

    resultats = np.empty([nbMiniVideo, NB_ZONE_VISAGE, NB_IMAGES])

    for i in range(nbMiniVideo):
        debutMultiTab = strRes.find("[[", debutMultiTab + 1)
        debutTab = 0
        finTab = 0
        for j in range(NB_ZONE_VISAGE):
            if j == 0:
                debutTab = strRes.find("[", debutMultiTab + debutTab + 1)
                finTab = strRes.find("]", debutMultiTab + finTab + 2)
            else:
                debutTab = strRes.find("[", debutTab + 1)
                finTab = strRes.find("]", finTab + 2)

            resultats[i][j] = np.fromstring(strRes[debutTab + 1: finTab], dtype=float, sep=' ')

    fichier.close()
    return resultats

# renvoie un numpy array contenant le maximum de chaque petites vidéos pour chaque zone
def recupMaxParZone(resultats , nbMiniVideo = 10):

    maxParZone = np.empty([NB_ZONE_VISAGE, nbMiniVideo])
    for i in range(nbMiniVideo):
        for j in range(NB_ZONE_VISAGE):
            maxParZone[j][i] = np.max(resultats[i][j])
    return maxParZone

# créer un graphique "bar chart" avec comme titre le nom de la vidéo
def creerBarGraph(donnee, videoName, nbMiniVideo = 10):

    fig = plt.figure(figsize=(5, 20))
    grid = gridspec.GridSpec(ncols=1, nrows=NB_ZONE_VISAGE, hspace=0, figure=fig)
    for i in range(NB_ZONE_VISAGE):
        if i == 0:
            fig.add_subplot(grid[i, 0]).set_title(videoName)
        else:
            fig.add_subplot(grid[i, 0])
        plt.bar(range(1, nbMiniVideo + 1), donnee[i], width=0.3)
        plt.ylabel(ZONE_VISAGE.get(i + 1), fontsize=5.5)
        plt.ylim(0, 15)

    axes = fig.axes
    for a in axes:
        plt.setp(a.get_yticklabels()[-1], visible=False)

    return fig

# créer un graphique de "boîte à moustache"  avec comme titre le nom de la vidéo
def boxplots(donnee, videoName, videoNum):
    NCOLS = 4
    NROWS = 5
    fig = plt.figure(figsize=(10, 15))
    grid = gridspec.GridSpec(ncols=NCOLS, nrows=NROWS, figure=fig)
    for i in range(NROWS):
        for j in range(NCOLS):
            if i * NCOLS + j == 0 :
                fig.add_subplot(grid[i, j]).set_title(videoName + "\n" + "Mini vidéo num : " + str(videoNum) + "\n" + ZONE_VISAGE.get(i * NCOLS + j + 1))
            else:
                fig.add_subplot(grid[i, j]).set_title(ZONE_VISAGE.get(i * NCOLS + j + 1))
            plt.boxplot(donnee[i * NCOLS + j])
            plt.ylim(0, 5)
            if i * NCOLS + j >= NB_ZONE_VISAGE - 1:
                break
    return fig

