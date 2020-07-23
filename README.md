# BachelorMensonge

Ce projet est composé de deux scripts principaux (LucasExtract.py & Analyse.py) ainsi que de deux scripts utilitaires (UtilExtract & UtilAnalyse). Un notebook python, fournissant une implémentation de l'algorithme T-SNE, est aussi présent. 

Vous trouverez aussi un dossier ApplicationMobile contenant une application Android permettant la récolte de données.

Les informations théorique sur ce projet sont disponible dans le fichier pdf relatif à ce travail de Bachelor.

## Mode d'emploi

Pour avoir la possibilité de reproduire ce projet le plus simplement possible, veuillez commencer par cloner ce "dépôt". Après avoir fait cela, il va vous falloir des données à extraire et à analyser. Vous pouvez soit utiliser l'application mobile fourni dans ce projet soit prendre vous même des vidéos de personne en train de dire la vérité ou de dire des mensonges (faire attention à bien cadrer la tête et faire en sorte que votre sujet ne bouge pas trop la tête). Après avoir fait cela, vous pourrez commencer la première étape, qui est d'extraire les données.

### Extraction des données 

Le script LucasExtract.py, se trouvant dans le dossier ExtractionDesDonnees, permet, lorsqu'on lui passe un dossier (nommé "Vidéos") rempli de vidéos à traiter, de calculer et stocker (dans un dossier "Resultats") la moyenne de la distance parcouru par les points, de chaque zone du visage.

Il est possible de choisir le nombre de points par zones dans le fichier "Utilitaires" pour améliorer la précision (au détriment de la vitesse d’exécution). 

Cette étape étant assez longue, vous pourrez trouver un dossier de résultats (nommé resultatsMobile) que nous avons utilisé pour la suite du travail. Il est le résultat de l’analyse de 43 vidéos ayant été réalisées à l'aide de l'application mobile. 

Certains résultats contiennent dans leur nom l'information "contient_des_NaN", cela est du au fait qu'à un certains moment de la vidéo le script n'a pas été capable de détecter un visage. Les données sont encore exploitable, il faut juste ne pas prendre en compte la "petite vidéo" contenant les "frames" incriminées.

### Analyse des données

Concernant l'analyse des données,





