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

#### Scripts & graphique

Concernant l'analyse des données, il vous faut créer un dossier Resultats et y placer les résultats que vous avez obtenu grâce à l'extraction des données. Le script Analyse créer deux PDF contenant des représentations graphiques de nos données. Le PDF resultats_bar est un graphique bar chart représentant le déplacement maximum de chaque zones du visage pour chaque "petite vidéo" (il est possible de choisir le nombre de petites vidéos que vous voulez traiter). Le PDF resultats_box est un graphique boxplot représentant les "boîte à moustache" pour chaque zones pour chaque "petites vidéos".

Cette étape étant, elle aussi, assez longue, vous trouverez les PDFs dans le dossier AnalyseDesDonnees. Nous n'avons utilisé que 41 des 43 résultats obtenus car deux ne fournissaient pas assez de "frames" à étudier (nous avions mis une limite à 10 petites vidéos de 15 "frames"). Les résultats suivants ont été retirés : "Vérité_normal_4_1593005176949.mp4.txt" et "Mensonge_normal_1_1593027647192.mp4.txt".

#### Notebook & T-SNE

Pour utiliser le notebook, il vous faut aussi créer un fichier "Resultats" contenant les résultats obtenus à l'aide du script d'extraction de données. Il faut cependant être vigilant au fichier contenant des NaN. Si ceux-ci apparaissent dans les données que vous aller exploiter, il vous faut les supprimer, sinon le notebook ne fonctionnera pas.

C'est pourquoi si vous voulez utiliser nos données pour reproduire expérience et que vous aussi souhaitez ne traiter que les 10 premières "petites vidéos", il vous faut supprimer les fichiers suivants du dossier "Resultats" :  "Vérité_choquant_1_1593621468067.mp4_contient_des_NaN.txt" et "Vérité_choquant_2_1593599077190.mp4_contient_des_NaN.txt" (ce qui réduit à l'analyse de 39 résultats)

Il faut aussi faire attention à vos noms de fichier. Si vous décidez d'utiliser d'autre vidéos et résultats que ceux proposés, il faut que les noms de vos résultats commence par un M pour un mensonge ou par un V si c'est une vérité.

