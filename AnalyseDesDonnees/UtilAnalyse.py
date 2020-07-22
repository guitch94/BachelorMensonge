import numpy as np
import os
from matplotlib import pyplot as plt, gridspec
from matplotlib.backends.backend_pdf import PdfPages
from ExtractionDesDonnees.UtilExtract import ZONE_VISAGE, reductionBruit

NB_MULTI_TAB = 10 # nombre de "petites videos" que l'on veut prendre en compte
NB_IMAGES = 15 # nombre de d'images par "petites vidéos"
NB_ZONE_VISAGE = 17


# récupère les résultats d'un fichier texte et les renvoie sous forme d'un tableau numpy
def recupResultats(path, videoName):

    fichier = open(path + videoName, "r")
    strRes = fichier.read()
    debutMultiTab = 0

    resultats = np.empty([NB_MULTI_TAB, NB_ZONE_VISAGE, NB_IMAGES])

    for i in range(NB_MULTI_TAB):
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
def recupMaxParZone(resultats):

    maxParZone = np.empty([NB_ZONE_VISAGE, NB_MULTI_TAB])
    for i in range(NB_MULTI_TAB):
        for j in range(NB_ZONE_VISAGE):
            maxParZone[j][i] = np.max(resultats[i][j])
    return maxParZone

# créer un graphique "bar chart"
def creerBarGraph(donnee, videoName):

    fig = plt.figure(figsize=(5, 20))
    grid = gridspec.GridSpec(ncols=1, nrows=NB_ZONE_VISAGE, hspace=0, figure=fig)
    for i in range(NB_ZONE_VISAGE):
        if i == 0:
            fig.add_subplot(grid[i, 0]).set_title(videoName)
        else:
            fig.add_subplot(grid[i, 0])
        plt.bar(range(1, NB_MULTI_TAB + 1), donnee[i], width=0.3)
        plt.ylabel(ZONE_VISAGE.get(i + 1), fontsize=5.5)
        plt.ylim(0, 15)

    axes = fig.axes
    for a in axes:
        plt.setp(a.get_yticklabels()[-1], visible=False)

    return fig

# créer un graphique de "boîte à moustache" pour la moyenne de déplacement de chacunes des zones
def boxplots(donnee):
    fig = plt.figure(figsize=(10, 10))
    grid = gridspec.GridSpec(ncols=4, nrows=5, hspace=0, figure=fig)
	for i in range(NB_ZONE_VISAGE):
		creerBoxplot(donnee[i],(6,3,i+1), ZONE_VISAGE.get(i + 1))


# crée un graphique de "boîte à moustache"
def creerBoxplot(points, numPlot, nomZone):

    plt.subplot(numPlot[0],numPlot[1],numPlot[2])
    plt.boxplot(points)
    plt.ylim(0, 5)
    plt.title(nomZone)
'''
lstResultats = os.listdir(PATH)

if os.path.exists('resultats.pdf'):
    os.remove("resultats.pdf")
lstResultats.sort()
pp = PdfPages('resultats.pdf')

for name in lstResultats:
    resultats = recupResultats(PATH, name)
    maxParZone = recupMaxParZone(resultats)
    pp.savefig(creerBarGraph(maxParZone, name))

pp.close()'''