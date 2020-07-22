#################################################################################################
# Auteur : Guillaume Blanco
#
# Date de dernière modification : 23.07.2020
#
# Description : Ce script contient différentes fonctions utile au script d'extraction
#				de caractéristique ainsi qu'au script d'analyse de données.
#
#
#################################################################################################


import math
import cv2
import imutils
import itertools
import numpy as np

from scipy.spatial import distance
from _collections import OrderedDict


# adapte les points proposé par le prédicteur à un numpy array
def shape_to_np(shape, dtype="int"):
	coords = np.zeros((68, 2), dtype=dtype)
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
	return coords


# dictionnaire contenant les indexs des regions faciales proposées par le predicteur
INDEX_REPERE_FACIAUX = OrderedDict([
	("bouche", (48, 68)),
	("sourcil_droit", (17, 22)),
	("sourcil_gauche", (22, 27)),
	("oeil_droit", (36, 42)),
	("oeil_gauche", (42, 48)),
	("nez", (27, 36)),
	("machoire", (0, 17))
])

# dictionnaire contenant les zones du visage créé par nos soins
ZONE_VISAGE = {
	1 : "front_droit",
	2 : "front_milieu",
	3 : "front_gauche",
	4 : "sourcil_droit_externe",
	5 : "sourcil_droit_interne",
	6 : "sourcil_gauche_externe",
	7 : "sourcil_gauche_interne",
	8 : "coin_oeil_droit",
	9 : "oeil_droit",
	10: "coin_oeil_gauche",
	11: "oeil_gauche",
	12: "pommette_droite",
	13: "pommette_gauche",
	14: "bouche_haute",
	15: "bouche_basse",
	16: "bouche_gauche",
	17: "bouche_droite",
	18: "nez"
}

NB_POINT = 3 # nombre de points par arêtes d'une zone

# creation des matrices de points définissant les différentes zones du visage
def creerTabPoint(shape):
	TiersDuMilieu = shape[34][1] - shape[22][1] # différence entre le bas des sourcils jusqu'à la racine du nez

	l1 = getFrontDroit(shape[INDEX_REPERE_FACIAUX['sourcil_droit'][0]:INDEX_REPERE_FACIAUX['sourcil_droit'][1]], TiersDuMilieu)

	l2 = getFrontMilieu(shape[INDEX_REPERE_FACIAUX['sourcil_droit'][0]:INDEX_REPERE_FACIAUX['sourcil_droit'][1]],
							shape[INDEX_REPERE_FACIAUX['sourcil_gauche'][0]:INDEX_REPERE_FACIAUX['sourcil_gauche'][1]],
							TiersDuMilieu)
	l3 = getFrontGauche(shape[INDEX_REPERE_FACIAUX['sourcil_gauche'][0]:INDEX_REPERE_FACIAUX['sourcil_gauche'][1]], TiersDuMilieu)

	l4 = getSourcilExternDroit(shape[INDEX_REPERE_FACIAUX['sourcil_droit'][0]:INDEX_REPERE_FACIAUX['sourcil_droit'][1]])

	l5 = getSourcilInternDroit(shape[INDEX_REPERE_FACIAUX['sourcil_droit'][0]:INDEX_REPERE_FACIAUX['sourcil_droit'][1]],
							   shape[INDEX_REPERE_FACIAUX['nez'][0]:INDEX_REPERE_FACIAUX['nez'][1]])

	l6 = getSourcilExternGauche(shape[INDEX_REPERE_FACIAUX['sourcil_gauche'][0]:INDEX_REPERE_FACIAUX['sourcil_gauche'][1]])

	l7 = getSourcilInternGauche(shape[INDEX_REPERE_FACIAUX['sourcil_gauche'][0]:INDEX_REPERE_FACIAUX['sourcil_gauche'][1]],
							   shape[INDEX_REPERE_FACIAUX['nez'][0]:INDEX_REPERE_FACIAUX['nez'][1]])

	l8 = getCoinsDroitOeil(shape[INDEX_REPERE_FACIAUX['oeil_droit'][0]:INDEX_REPERE_FACIAUX['oeil_droit'][1]],
							   shape[INDEX_REPERE_FACIAUX['sourcil_droit'][0]:INDEX_REPERE_FACIAUX['sourcil_droit'][1]])

	l9 = getOeilDroit(shape[INDEX_REPERE_FACIAUX['oeil_droit'][0]:INDEX_REPERE_FACIAUX['oeil_droit'][1]])

	l10 = getCoinOeilGauche(shape[INDEX_REPERE_FACIAUX['oeil_gauche'][0]:INDEX_REPERE_FACIAUX['oeil_gauche'][1]],
						   shape[INDEX_REPERE_FACIAUX['sourcil_gauche'][0]:INDEX_REPERE_FACIAUX['sourcil_gauche'][1]])
	
	l11 = getOeilGauche(shape[INDEX_REPERE_FACIAUX['oeil_gauche'][0]:INDEX_REPERE_FACIAUX['oeil_gauche'][1]])

	l12 = getPommetteDroite(shape[INDEX_REPERE_FACIAUX['oeil_droit'][0]:INDEX_REPERE_FACIAUX['oeil_droit'][1]],
							shape[INDEX_REPERE_FACIAUX['nez'][0]:INDEX_REPERE_FACIAUX['nez'][1]])

	l13 = getPommetteGauche(shape[INDEX_REPERE_FACIAUX['oeil_gauche'][0]:INDEX_REPERE_FACIAUX['oeil_gauche'][1]],
						   shape[INDEX_REPERE_FACIAUX['nez'][0]:INDEX_REPERE_FACIAUX['nez'][1]])

	l14 = getBoucheHaute(shape[INDEX_REPERE_FACIAUX['bouche'][0]:INDEX_REPERE_FACIAUX['bouche'][1]])

	l15 = getBoucheBasse(shape[INDEX_REPERE_FACIAUX['bouche'][0]:INDEX_REPERE_FACIAUX['bouche'][1]])

	l16 = getBoucheGauche(shape[INDEX_REPERE_FACIAUX['oeil_gauche'][0]:INDEX_REPERE_FACIAUX['oeil_gauche'][1]],
					   shape[INDEX_REPERE_FACIAUX['bouche'][0]:INDEX_REPERE_FACIAUX['bouche'][1]])

	l17 = getBoucheDroite(shape[INDEX_REPERE_FACIAUX['oeil_droit'][0]:INDEX_REPERE_FACIAUX['oeil_droit'][1]],
						shape[INDEX_REPERE_FACIAUX['bouche'][0]:INDEX_REPERE_FACIAUX['bouche'][1]])

	l18 = getNez(shape[INDEX_REPERE_FACIAUX['nez'][0]:INDEX_REPERE_FACIAUX['nez'][1]])

	return list(itertools.chain(l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11,l12,l13,l14,l15,l16,l17,l18))



def getFrontDroit(sourcil_droit, TiersDuMilieu):
	sizeX = sourcil_droit[3][0] - sourcil_droit[1][0]
	sizeY = int(TiersDuMilieu / 2)
	startingPoint = (sourcil_droit[1][0], sourcil_droit[1][1] - sizeY)
	return getZone(sizeX, sizeY - (sizeY/5), startingPoint)

def getFrontMilieu(sourcil_droit, sourcil_gauche,TiersDuMilieu):
	sizeX = sourcil_gauche[0][0] - sourcil_droit[4][0]
	sizeY = int(TiersDuMilieu / 2)
	startingPoint = (sourcil_droit[4][0], sourcil_droit[3][1] - sizeY)
	return getZone(sizeX, sizeY - (sizeY/5), startingPoint)

def getFrontGauche(sourcil_gauche, TiersDuMilieu):
	sizeX = sourcil_gauche[3][0] - sourcil_gauche[1][0]
	sizeY = int(TiersDuMilieu / 2)
	startingPoint = (sourcil_gauche[1][0], sourcil_gauche[1][1] - sizeY)
	return getZone(sizeX, sizeY - (sizeY/5), startingPoint)

def getSourcilExternDroit(sourcil_droit):
	sizeX = sourcil_droit[3][0] - sourcil_droit[0][0]
	sizeY = sourcil_droit[2][0] - sourcil_droit[1][0]
	startingPoint = (sourcil_droit[0][0] , sourcil_droit[2][1])
	return getZone(sizeX, sizeY, startingPoint)

def getSourcilInternDroit(sourcil_droit, nez):
	sizeX = nez[0][0] - sourcil_droit[3][0]
	sizeY = sourcil_droit[2][0] - sourcil_droit[1][0]
	startingPoint = (sourcil_droit[3][0] , sourcil_droit[3][1])
	return getZone(sizeX, sizeY, startingPoint)

def getSourcilExternGauche(sourcil_gauche):
	sizeX = sourcil_gauche[4][0] - sourcil_gauche[1][0]
	sizeY = sourcil_gauche[3][0] - sourcil_gauche[2][0]
	startingPoint = (sourcil_gauche[1][0] , sourcil_gauche[2][1])
	return getZone(sizeX, sizeY, startingPoint)

def getSourcilInternGauche(sourcil_gauche, nez):
	sizeX = sourcil_gauche[1][0] - nez[0][0]
	sizeY = sourcil_gauche[3][0] - sourcil_gauche[2][0]
	startingPoint = (nez[0][0] , sourcil_gauche[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getCoinOeilGauche(oeil_gauche, sourcil_gauche):
	sizeX = sourcil_gauche[4][0] - oeil_gauche[3][0]
	sizeY = oeil_gauche[5][1] - oeil_gauche[1][1]
	startingPoint = (sourcil_gauche[3][0], oeil_gauche[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getOeilGauche(oeil_gauche):
	sizeX = oeil_gauche[3][0] - oeil_gauche[0][0]
	sizeY = oeil_gauche[5][1] - oeil_gauche[2][1]
	startingPoint = (oeil_gauche[0][0], oeil_gauche[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getCoinsDroitOeil(oeil_droit, sourcil_droit):
	sizeX = oeil_droit[0][0] - sourcil_droit[0][0]
	sizeY = oeil_droit[5][1] - oeil_droit[1][1]
	startingPoint = (sourcil_droit[0][0], oeil_droit[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getOeilDroit(oeil_droit):
	sizeX = oeil_droit[3][0] - oeil_droit[0][0]
	sizeY =  oeil_droit[5][1] - oeil_droit[2][1]
	startingPoint =  (oeil_droit [0][0], oeil_droit[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getPommetteDroite(oeil_droit, nez):
	sizeX = oeil_droit[3][0] - oeil_droit[0][0]
	sizeY = nez[2][1] - nez[1][1]
	startingPoint = (oeil_droit[0][0], nez[1][1])
	return getZone(sizeX, sizeY, startingPoint)

def getPommetteGauche(oeil_gauche, nez):
	sizeX = oeil_gauche[3][0] - oeil_gauche[0][0]
	sizeY = nez[2][1] - nez[1][1]
	startingPoint = (oeil_gauche[0][0] , nez[1][1])
	return getZone(sizeX, sizeY, startingPoint)


def getBoucheHaute(bouche):
	sizeX = bouche[6][0] - bouche[0][0]
	sizeY = bouche[0][1] - bouche[2][1]
	startingPoint = (bouche[0][0], bouche[2][1])
	return getZone(sizeX, sizeY, startingPoint)

def getBoucheBasse(bouche):
	sizeX = bouche[6][0] - bouche[0][0]
	sizeY = bouche[9][1] - bouche[0][1]
	startingPoint = (bouche[0][0], bouche[0][1])
	return getZone(sizeX, sizeY, startingPoint)

def getBoucheGauche(oeil_gauches, bouche):
	sizeX = oeil_gauches[3][0] - bouche[6][0]
	sizeY = bouche[9][1] - bouche[3][1]
	startingPoint = (bouche[6][0], bouche[4][1])
	return getZone(sizeX, sizeY, startingPoint)


def getBoucheDroite(oeil_droits, bouche):
	sizeX = int((bouche[0][0] - oeil_droits[0][0]) / 2)
	sizeY = bouche[9][1] - bouche[3][1]
	startingPoint = (oeil_droits[1][0], bouche[3][1])
	return getZone(sizeX, sizeY, startingPoint)

def getNez(nez):
	sizeX = nez[7][0] - nez[5][0]
	sizeY = nez[6][1] - nez[3][1]
	startingPoint = (nez[5][0], nez[2][1])
	return getZone(sizeX, sizeY, startingPoint)

def getZone(sizeX, sizeY, startingPoint):
	return matricePoints(startingPoint,  NB_POINT, sizeX, sizeY)

# crée une matrice en fonction d'un point de départ, du nombre de points dans la matrice et de la taille de cette dernière
def matricePoints(startingPoint, nbPoints, sizeX, sizeY):
	sizeBetweenPointsX =  int(sizeX/(nbPoints - 1))
	sizeBetweenPointsY =  int(sizeY/(nbPoints - 1))
	newPoints = [None] * nbPoints ** 2
	for i in range(nbPoints):
		for j in range(nbPoints):
			newPoints[i * nbPoints + j] =  [startingPoint[0] + sizeBetweenPointsX * j, startingPoint[1] + sizeBetweenPointsY * i]
	return newPoints


# renvoie un tableau de status de points avec une limite de déplacement d'une image à l'autre
def filtre(st, evolDist, limite):
	for i in range(len(evolDist)):
		if(evolDist[i] > limite):
			st[i] = 0
	return st

# Calcul la direction des points (8 directions possible : nord, sud, est, ouest, nord-ouest, nord-est, sud-ouest, sud-est).
def direction(tabPointDebut, tabPointFin, tabDist):

	tabDir = [0] * len(tabPointDebut)
	for i in range(len(tabPointDebut)):

		xDiff = tabPointFin[i][0] - tabPointDebut[i][0]
		yDiff = tabPointFin[i][1] - tabPointDebut[i][1]
		a = tabDist[i]
		c = distance.euclidean([1, 0], [xDiff, yDiff])
		if(a != 0):
			angle = round(math.degrees(math.acos((a ** 2 + 1 - c ** 2) / (2 * a))))
		else:
			angle = 0

		if (yDiff <= 0):
			tabDir[i] = round(angle / 45)
		else:
			tabDir[i] = round(((180 - angle) / 45) + 4) % 8

	return tabDir


# Calcul la moyenne de déplacement des points par zones
def moyenne(points, st ):

	nbFrame = int(len(points))
	nbPointsParZone = NB_POINT**2
	nbPointsParFrame = len(points[0])
	nbZone = int(nbPointsParFrame / nbPointsParZone)
	pointParZone = points.reshape(nbFrame * nbZone, nbPointsParZone)
	tabMoyenne = np.empty([nbZone,nbFrame])
	pointAEffacer = []
	for i in range(len(pointParZone[0])):
		if(st[i] == 0):
			pointAEffacer.append(i)

	pointParZone =  np.delete(pointParZone, pointAEffacer, axis=1)

	cnt = 0
	for i in range(nbFrame):
		for j in range(nbZone):
			tabMoyenne[j][i] = np.mean(pointParZone[cnt])
			cnt += 1

	return tabMoyenne

# réduit le bruit (déplacement de la tête d'une personne) en se basant sur la position du nez
def reductionBruit(tabMoyenne):
	for i in range(len(tabMoyenne) - 1):
		tabMoyenne[i] = tabMoyenne[i] - tabMoyenne[len(tabMoyenne) - 1]
		for j in range(len(tabMoyenne[i])):
			if(tabMoyenne[i][j] < 0):
				tabMoyenne[i][j] = 0
	return tabMoyenne


# traite l'image pour qu'elle soit exploitable par le script
def traitementImage(image):
	# retourne l'image si elle est en mode paysage
	if (image.shape[0] < image.shape[1]):
		image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
	# redimension la première image
	image = imutils.resize(image, width=500)
	return image



