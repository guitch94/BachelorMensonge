from AnalyseDesDonnees.UtilAnalyse import recupResultats, boxplots
from matplotlib import pyplot as plt

PATH = "Resultats/"

videoName = "Mensonge_choquant_3_1593598816019.mp4.txt"

resultats = recupResultats(PATH,videoName)
print(resultats[0].shape)
boxplots(resultats[0])
plt.show()