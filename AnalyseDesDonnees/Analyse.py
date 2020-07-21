import numpy as np
import os
from matplotlib import pyplot as plt, gridspec
from Utils import ZONE_VISAGE
from matplotlib.backends.backend_pdf import PdfPages

NB_MULTI_TAB = 10
NB_FRAME = 15
NB_ZONE_VISAGE = 17
PATH = "Resultats/"
VIDEO_NAME = "Mensonge_normal_2_1593197813162.txt"

def recupResultats(path, videoName):

    fichier = open(path + videoName, "r")
    strRes = fichier.read()
    debutMultiTab = 0

    resultats = np.empty([NB_MULTI_TAB, NB_ZONE_VISAGE, NB_FRAME])

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

def recupMaxParZone(resultats):

    maxParZone = np.empty([NB_ZONE_VISAGE, NB_MULTI_TAB])
    for i in range(NB_MULTI_TAB):
        for j in range(NB_ZONE_VISAGE):
            maxParZone[j][i] = np.max(resultats[i][j])
    return maxParZone


def creerGraph(maxParZone, videoName):

    fig = plt.figure(figsize=(5, 20))
    grid = gridspec.GridSpec(ncols=1, nrows=NB_ZONE_VISAGE, hspace=0, figure=fig)
    for i in range(NB_ZONE_VISAGE):
        if i == 0:
            fig.add_subplot(grid[i, 0]).set_title(videoName)
        else:
            fig.add_subplot(grid[i, 0])
        plt.bar(range(1, NB_MULTI_TAB + 1), maxParZone[i], width=0.3)
        plt.ylabel(ZONE_VISAGE.get(i + 1), fontsize=5.5)
        plt.ylim(0, 15)

    axes = fig.axes
    for a in axes:
        plt.setp(a.get_yticklabels()[-1], visible=False)

    return fig

lstVideo = os.listdir(PATH)
if os.path.exists('resultats.pdf'):
    os.remove("resultats.pdf")
lstVideo.sort()
pp = PdfPages('resultats.pdf')

for name in lstVideo:
    resultats = recupResultats(PATH, name)
    maxParZone = recupMaxParZone(resultats)
    pp.savefig(creerGraph(maxParZone, name))

pp.close()