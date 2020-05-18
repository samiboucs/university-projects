Spécifications générales
=======================
Cours : TAL et apprentissage des langues
Projet : Python Corpus Processor and Analyzer
Enseignant responsable : Monsieur Mathieu LOISEAU
Étudiants : 
	*Sami BOUHOUCHE
	*Nicolas Leewys DAVID
Master 2 | Sciences du Langage | Industries de la Langue
Semestre 1 | Année universitaire 2018-2019
UFR LLASIC | Université Grenoble Alpes

À propos du script "pcpa.py"
=======================
:auteurs: 
	*Sami BOUHOUCHE <sami.bouhouche@etu.univ-grenoble-alpes.fr>
	*Nicolas Leewys DAVID <nicolas-leewys.david@etu.univ-grenoble-alpes.fr>

Ce script Python prend en entrée des fichiers .txt pour ensuite les étiqueter au moyen de TreeTagger. 
Il prend également en entrée un fichier .txt qui servira de référence. Après avoir étiqueté les fichiers,
le résultat de l'étiquetage est écrit dans un fichier .csv, pour chaque fichier .txt traité. Finalement,
il procède à l'analyse lexico-métrique des fichiers étiquetés ainsi qu'au calcul de différentes métriques
(à partir de la référence). Les résultats qui sont issus de cette analyse et de ce calcul sont écrits 
dans un fichier .csv, pour chaque fichier étiqueté analysé.

** Entrées **
./prod_txt 	: contenant les fichiers des productions au format .txt
./ref_txt 	: contenant le fichier de production de référence au format .txt

** Sortie/Entrée **
./tags_csv	: contenant les fichiers des étiquetages au format .csv

** Sortie **
./data_csv	: contenant les fichiers des résultats au format .csv

À propos du script "lsa_tm.py"
=======================
:auteur:
	*Avinash Navlani <https://www.datacamp.com/profile/avinashnvln8>
	
Ce script Python permet de réaliser un topic modelling sur des éléments textuels en utilisant 
le modèle LSA/LSI du module Gensim.