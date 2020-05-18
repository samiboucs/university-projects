#! /usr/bin/env python3
# -*- coding:utf8 -*-

'''
Spécifications générales
=======================
Cours : Programmation Langage Java (Niveau 2)
Projet : Text to metrics
Enseignant responsable : Monsieur Claude PONTON
Étudiants : 
	*Sami BOUHOUCHE
	*Nicolas Leewys DAVID
Master 2 | Sciences du Langage | Industries de la Langue
Semestre 1 | Année universitaire 2018-2019
UFR LLASIC | Université Grenoble Alpes

À propos du script "ttw.py"
=======================
:auteurs: 
	*Sami BOUHOUCHE <sami.bouhouche@etu.univ-grenoble-alpes.fr>
	*Nicolas Leewys DAVID <nicolas-leewys.david@etu.univ-grenoble-alpes.fr>

Ce script Python prend en entrée un fichier .txt pour ensuite l'étiqueter au moyen de TreeTagger
Après avoir étiqueté le fichier .txt, le résultat de l'étiquetage est écrit dans un fichier .csv

** Entrée **
*Fichier au format .txt

** Sortie **
*Fichier au format .csv
'''

import treetaggerwrapper

filename = "fichier.txt"
f = open(filename, mode = 'r', encoding ='utf8')
text = f.read()
f.close()

#print (text)

# Construction et configuration du wrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGOPT='-token -lemma -sgml -no-unknown',TAGDIR='C:/TreeTagger',TAGINENC='utf-8',TAGOUTENC='utf-8')
# Utilisation
tags = tagger.TagText(text)


# for tag in tags:
	# print (tag)
	
with open('tags.csv', mode = 'w', encoding = 'cp1252') as Output_File:
	for tag in tags:	#Parcourir la liste des tokens/formes
		print(tag)
		print (tag, file=Output_File)	#Écriture du fichier étiqueté

print ("Étiquetage du fichier terminé !")
