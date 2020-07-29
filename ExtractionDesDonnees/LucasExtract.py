#################################################################################################
# Auteur : Guillaume Blanco
#
# Date de dernière modification : 28.07.2020
#
# Description : Ce script récupère toutes les vidéos stocker dans un dossier vidéos puis les
#               traite une par une. Il va découper chacunes des vidéos en plus petites vidéos
#               d'un nombre de image égal à NB_image_VIDEO. Il va ensuite, pour chacunes de ces
#               plus petites viédos calculer l'évolutions des déplacements des points préalablements
#               choisis. Ces déplacements sont ensuite stocker dans un dossier nommé Resultats
#
# Remarque : Une vidéo est un ensemble d'images mise bout à bout
#            Si vous avez beaucoup de vidéos à traiter, il est intéressant de commenter le code
#            affichant le dessin des points.
#################################################################################################
import os
import cv2
import sys
import dlib
import shutil
import logging
import numpy as np

from UtilExtract import shape_to_np, creerTabPoint, filtre, direction, moyenne, reductionBruit, traitementImage
from scipy.spatial import distance


PATH_VIDEOS = 'Videos/'

if len(sys.argv) > 1:
    PATH_VIDEOS = sys.argv[1]

if not os.path.exists(PATH_VIDEOS):
    logging.warning('Pas de dossier ' + PATH_VIDEOS)
    exit()

lstVideos = [f for f in os.listdir(PATH_VIDEOS) if os.path.isfile(os.path.join(PATH_VIDEOS, f))]

if not lstVideos:
    logging.warning('Pas de videos a traiter')
    exit()

NB_IMAGE_PAR_VIDEO = 15
PATH_RESULTATS = "Resultats/"
PATH_VIDEO_TRAITEE = "Videos/VideoTraitee/"
erreurNaN = 0

os.makedirs(PATH_RESULTATS, exist_ok=True)
os.makedirs(PATH_VIDEO_TRAITEE, exist_ok=True)



for video in lstVideos:


    print("analyse de " + video  + " en cours")

    # Vidéo qui va être analysée
    cap = cv2.VideoCapture(PATH_VIDEOS + video)
    
    # Initialise le detecteur de visage et le prédicteur de repère faciaux
    detecteur = dlib.get_frontal_face_detector()
    predicteur = dlib.shape_predictor("shape_predictor.dat")
    
    # Paramètre pour la détéction de flux optique (méthode Lucas-Kanade)
    lk_param = dict( winSize  = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    nbImageTot = 0
    
    if os.path.exists(PATH_RESULTATS + video + ".txt"):
      os.remove(PATH_RESULTATS + video + ".txt")
    fichier = open(PATH_RESULTATS + video + ".txt", "x")

    while(1):
    
        # Récupère la première image de chaque vidéo / ret est un booleen indiquant si l'image est exploitable
        ret, premiereImage = cap.read()

        nbImageTot += 1

        if premiereImage is None:
            break

        premiereImage = traitementImage(premiereImage)

        # transforme la première image en nuance de gris
        premImageGrise = cv2.cvtColor(premiereImage, cv2.COLOR_BGR2GRAY)

        # récupère un rectangle contenant le visage sur l'image (s'il n'y a pas de visage au format portrait, le script lance une erreur)
        rect = detecteur(premImageGrise, 1)

        try:
            # détérmine les points de repère faciaux
            shape = predicteur(premImageGrise, rect[0])
        except:
            logging.warning('Pas de visage détécté')
            for i in range(NB_IMAGE_PAR_VIDEO):
                ret, premiereImage = cap.read()
            erreurNaN = 1
            continue

        # définit les différents points que nous allons analysé
        points = creerTabPoint(shape_to_np(shape))
    
        #initialise un numpy array contenant les points à analyser
        p0 = np.array([[[0.,0.]]] * len(points), dtype='f')
        for i in range(len(points)):
            p0[i][0][0] = np.float32(points[i][0])
            p0[i][0][1] = np.float32(points[i][1])
    
        # Crée un masque sur lequel on pourra dessiner les déplacements des points
        masque = np.zeros_like(premiereImage)

        # initialisation des numpy arrays contenant l'évolution des points, de distances entre les points et le status des points
        evolPoints = np.array(points)
        evolDist = np.empty([1,len(points),1])
        evolSt = np.full((len(points),1),1)
    
    
        nbImage = 1
    
        while(1):

            # Permet de découpage de la vidéos en plus petite vidéos du nombre d'image souhaité
            if (nbImage % (NB_IMAGE_PAR_VIDEO + 1) == 0):
                break

            # Récupère l'image à traiter
            ret,image = cap.read()
    
            if image is None:
                break


            image = traitementImage(image)

            imageGrise = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # image en niveau de gris (0 à 255 par pixel)
    
    
            # calcul du flux optique selon l'algorithme de Lucas-Kanade
            p1, st, err = cv2.calcOpticalFlowPyrLK(premImageGrise, imageGrise, p0, None, **lk_param) # p1 désigne le prochain point(comment ils ont bougé)
                                                                                                     # st désigne le status d'un points (s'il est encore exploitable d'après l'algorithme
    

            evolPoints = np.append(evolPoints,p1).reshape(nbImage + 1,len(p0),2)

            # Calcul l'évolution de la distance des points
            for i in range(len(evolPoints[0])):
                if(nbImage == 1):
                    evolDist[nbImage - 1][i] = distance.euclidean([evolPoints[nbImage - 1][i][0], evolPoints[nbImage - 1][i][1]], [evolPoints[nbImage][i][0], evolPoints[nbImage][i][1]])
                else:
                    evolDist = np.append(evolDist, distance.euclidean([evolPoints[nbImage - 1][i][0], evolPoints[nbImage - 1][i][1]], [evolPoints[nbImage][i][0], evolPoints[nbImage][i][1]]))
            evolDist = evolDist.reshape(nbImage, len(p1),1)
    
            evolSt &= st


            # applique un filtre qui va indiquer si un points et exploitable ou non en fonction de la distance qu'il a parcouru d'une image à la suivante
            st = filtre(evolSt, evolDist[nbImage - 1],20)
            if np.sum(st) == 0:
                logging.warning("Plus aucuns point correct, il y aura des NaN")
                erreurNaN = 1

            # Calcul l'évolution de la direction des points
            if (nbImage == 1):
                evolDirection = np.array(direction(evolPoints[nbImage - 1], evolPoints[nbImage], evolDist[nbImage - 1]))
            else:
                evolDirection = np.append(evolDirection, direction(evolPoints[nbImage - 1], evolPoints[nbImage], evolDist[nbImage - 1])).reshape(nbImage, len(p1),1)
    
    
            # Selection des points considéré comme encore valable
            bonPoints = p1[st==1]
            bonPointsAncients = p0[st==1]
    
    
            # Dessine les points sur le masque et les affiches sur l'image actuelle
    
            '''for i,(actuels,anciens) in enumerate(zip(bonPoints,bonPointsAncients)):
                a,b = actuels.ravel()
                c,d = anciens.ravel()
                masque = cv2.line(masque, (a,b),(c,d), (120,234,243), 2)
                image = cv2.circle(image,(a,b),4,0,-1)
            img = cv2.add(image,masque)
    
            cv2.imshow('image' ,img)
    
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break'''

            # Mise à jour des l'image et des points précédents
            premImageGrise = imageGrise.copy()
            p0 = p1
    
            nbImage += 1
            nbImageTot += 1


        # supprime les fenêtres d'affichage
        cv2.destroyAllWindows()

        # Stockage de l'évolution de la distance moyenne parcourue par les points pour chaque zones du visage
        fichier.write("\n\n" + str(int(nbImageTot/NB_IMAGE_PAR_VIDEO)))
        fichier.write("\n----------------------------------------------------------------------------------\n")
        fichier.write(np.array2string(reductionBruit(moyenne(evolDist, evolSt))))
    
    
    fichier.close()
    cap.release()

    if erreurNaN == 1:
        os.rename(PATH_RESULTATS + video + ".txt" , PATH_RESULTATS + video + "_contient_des_NaN.txt")
        erreurNaN = 0

    # déplacement des vidéos traitée dans un dossier "video traitée"
    if os.path.exists(PATH_VIDEO_TRAITEE + video):
        os.remove(PATH_VIDEOS + video)
    else:
        shutil.move(PATH_VIDEOS + video, PATH_VIDEO_TRAITEE)

    print("analyse de " + video + " terminee")

