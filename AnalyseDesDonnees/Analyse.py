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
import shutil

from AnalyseDesDonnees.UtilAnalyse import recupResultats, boxplots, recupMaxParZone, creerBarGraph
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'figure.max_open_warning': 0})

PATH_RESULTATS = "Resultats/"

PATH_RESULTAT_TRAITE = "Resultats/ResultatTraite/"

if not os.path.exists(PATH_RESULTATS):
    logging.warning('Pas de dossier resultats')
    exit()

lstResultats = [f for f in os.listdir(PATH_RESULTATS) if os.path.isfile(os.path.join(PATH_RESULTATS, f))]

if not lstResultats:
    logging.warning('Pas de resultats a traiter')
    exit()

lstResultats.sort()

os.makedirs(PATH_RESULTAT_TRAITE, exist_ok=True)

if os.path.exists('resultats_bar.pdf'):
    os.remove("resultats_bar.pdf")

if os.path.exists('resultats_box.pdf'):
    os.remove("resultats_box.pdf")

pdfBar = PdfPages('resultats_bar.pdf')
pdfBox = PdfPages('resultats_box.pdf')

for name in lstResultats:
    print("analyse de " + name + " en cours")
    try:
        resultats = recupResultats(PATH_RESULTATS, name)
    except:
        logging.warning('Verifiez le nombre de mini vidéo du fichier ' + name +'. Il faut qu il soit plus grand ou égal à nbMiniVideo')
        os.makedirs(PATH_RESULTATS + "ResultatsTropPetits", exist_ok=True)
        shutil.move(PATH_RESULTATS + name, PATH_RESULTATS + "ResultatsTropPetits/")
        continue
    maxParZone = recupMaxParZone(resultats)
    pdfBar.savefig(creerBarGraph(maxParZone, name))
    for i in range(resultats.shape[0]):
        if i == 0:
            pdfBox.savefig(boxplots(resultats[i], name, i + 1))
        else:
            pdfBox.savefig(boxplots(resultats[i], "", i + 1))
    print("analyse de " + name + " terminee")

    # déplacement des vidéos traitée dans un dossier "video traitée"
    if os.path.exists(PATH_RESULTAT_TRAITE + name):
        os.remove(PATH_RESULTATS + name)
    else:
        shutil.move(PATH_RESULTATS + name, PATH_RESULTAT_TRAITE)

pdfBar.close()
pdfBox.close()



