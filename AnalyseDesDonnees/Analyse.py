import os

from AnalyseDesDonnees.UtilAnalyse import recupResultats, boxplots, recupMaxParZone, creerBarGraph
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'figure.max_open_warning': 0})

PATH = "Resultats/"

videoName = "Mensonge_choquant_3_1593598816019.mp4.txt"

lstResultats = [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
lstResultats.sort()

if os.path.exists('resultats_bar.pdf'):
    os.remove("resultats_bar.pdf")

if os.path.exists('resultats_box.pdf'):
    os.remove("resultats_box.pdf")

pdfBar = PdfPages('resultats_bar.pdf')
pdfBox = PdfPages('resultats_box.pdf')

for name in lstResultats:
    resultats = recupResultats(PATH, name)
    maxParZone = recupMaxParZone(resultats)
    pdfBar.savefig(creerBarGraph(maxParZone, name))
    for i in range(resultats.shape[0]):
        if i == 0:
            pdfBox.savefig(boxplots(resultats[i], name, i + 1))
        else:
            pdfBox.savefig(boxplots(resultats[i], "", i + 1))


pdfBar.close()
pdfBox.close()



