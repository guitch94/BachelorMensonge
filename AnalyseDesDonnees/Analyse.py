#################################################################################################
# Auteur : Guillaume Blanco
#
# Date de dernière modification : 23.07.2020
#
# Description : Ce script crée deux fichier pdf permettant d'avoir une meilleure vision des
#               données. Le premier pdf (resultat_bar) montre le déplacement maximum des points
#               pour chaque zones et pour chaque fichier résultats proposés, sous forme
#               de bar chart. Le second, montre la moyenne des déplacements, pour chaque petites
#               vidéos et pour chaque zones du visage.
#
#
#################################################################################################
import logging
import os

from AnalyseDesDonnees.UtilAnalyse import recupResultats, boxplots, recupMaxParZone, creerBarGraph
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'figure.max_open_warning': 0})

PATH = "Resultats/"

if not os.path.exists(PATH):
    logging.warning('Pas de dossier resultats')
    exit()

lstResultats = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]

if not lstResultats:
    logging.warning('Pas de resultats a traiter')
    exit()

lstResultats.sort()

if os.path.exists('resultats_bar.pdf'):
    os.remove("resultats_bar.pdf")

if os.path.exists('resultats_box.pdf'):
    os.remove("resultats_box.pdf")

pdfBar = PdfPages('resultats_bar.pdf')
pdfBox = PdfPages('resultats_box.pdf')

for name in lstResultats:
    print("analyse de " + name + " en cours")
    resultats = recupResultats(PATH, name)
    maxParZone = recupMaxParZone(resultats)
    pdfBar.savefig(creerBarGraph(maxParZone, name))
    for i in range(resultats.shape[0]):
        if i == 0:
            pdfBox.savefig(boxplots(resultats[i], name, i + 1))
        else:
            pdfBox.savefig(boxplots(resultats[i], "", i + 1))
    print("analyse de " + name + " terminee")

pdfBar.close()
pdfBox.close()



