#! /usr/bin/env python3
# -*- coding:utf8 -*-

"""
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
"""

#Import des modules/librairies nécessaires
import os
import re
import sys
import glob
import time
import nltk
import os.path
import treetaggerwrapper
from nltk.metrics import *
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

#Mise en place d'une mesure du temps d'exécution du programme
time0 = time.time()

#Messages affichés lors du début de l'exécution du programme
print("***** Python Corpus Processor and Analyzer *****\n")

print("Début de l'exécution du programme !\n")

print("Programme en cours d'exécution...\n")

print("Étiquetage des productions en cours...\n")

#Récupération des fichiers contenant les productions
txt_files_list = glob.glob('./corpus_files/prod_txt/*.txt')

#Mise en place d'un compteur pour mesurer le nombre de productions étiquetées
txt_files_count = 0

#Récupération du fichier contenant la production de référence
ref_file = './corpus_files/ref_txt/ref.txt'

#Mise en place et traitement de la production de référence
ref = open(ref_file, encoding='utf8').read()
ref_tokens = nltk.word_tokenize(ref)
reference = [ref_tokens]
reference_set = set(ref_tokens)
cc = SmoothingFunction()

#Chaîne de traitement de chaque fichier .txt
##Phase de l'étiquetage de chaque production au moyen de TreeTagger
###Écriture des étiquetages dans un fichier
for file_name in txt_files_list:
		
	input_file = open(file_name, mode = 'r', encoding = 'utf8')
	
	tags_list = []

	for line in input_file:
		tagger = treetaggerwrapper.TreeTagger(TAGLANG = 'fr', TAGDIR = 'C:/TreeTagger', TAGINENC = 'utf-8', TAGOUTENC = 'utf-8')
		tags = tagger.TagText(line)
		for tag in tags:
			tags_list.append(tag+"\n")
	
	input_file.close()
	
	output_file = open(os.path.join('./corpus_files/tags_csv', os.path.basename(file_name[:-4]+"_tags.csv")), mode='w', encoding='utf8')
	
	for line in tags_list:
		output_file.write(line)
	
	output_file.close()
	
	txt_files_count += 1

print("Étiquetage des productions terminé !\n")

print(str(txt_files_count)+" productions ont été étiquetées !\n")

#Récupération des fichiers contenant les productions étiquetées
csv_files_list = glob.glob('./corpus_files/tags_csv/*.csv')

#Mise en place d'un compteur pour mesurer le nombre de productions étiquetées qui seront analysées
csv_files_count = 0

print("Analyse des productions étiquetées en cours...\n")

#Chaîne de traitement de chaque fichier .csv
##Phase de l'analyse lexico-métrique
for file_name in csv_files_list:
	
	#Ouverture du fichier d'entrée
	input_file = open(file_name, mode = 'r', encoding = 'utf8')
	
	#Mise en place de 4 listes qui contiendront :
	##les formes, les catégories, les lemmes et les couples lemmes-catégories
	forms_list = []
	categories_list = []
	lemmas_list = []
	cat_lem_list = []
	
	#Remplissage des listes
	for line in input_file:
		line = line.strip() 
		f_c_l = line.split("\t") 
		
		if len(f_c_l) == 3:
			form, category, lemma = f_c_l
		
		forms_list.append(form) 
		categories_list.append(category) 
		lemmas_list.append(lemma)
		cat_lem_list.append((category,lemma))
	
	#Mise en place et traitement des candidats (par rapport à la référence)
	candidate = forms_list
	test_set = set(forms_list)	
	
	#Calcul du score BLEU
	score = sentence_bleu(reference, candidate, weights=(1, 0, 0, 0), smoothing_function=cc.method1)
	
	#Calcul du nombre de formes/tokens
	nbTokens = len(forms_list)
	
	#Recherche des mots au moyen d'une expression régulière
	words_list = []
	nbCharacters = 0
	for word in forms_list:
		if (re.match(r"[A-Z|a-z|àâäéèêëîïöôùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]+(\.|-|')?[A-Z|a-z|àâäéèêëîïöôùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]?",word)):
			words_list.append(word)
			#Calcul du nombre de caractères
			for character in word:
				if character:
					nbCharacters+=1			
	
	#Calcul du nombre de mots
	nbWords = len(words_list)
	
	#Calcul du nombre moyen de caractères contenus dans chaque mot
	word_length_average = round(nbCharacters/nbWords)

	#Recherche des phrases au moyen d'une expression régulière
	sentences_list = []
	for sentence in categories_list:
		if (re.match(r'SENT',sentence)):
			sentences_list.append(sentence)
	
	#Calcul du nombre de phrases
	nbSentences = len(sentences_list)
	
	#Calcul du nombre moyen de mots contenus dans chaque phrase
	if nbSentences != 0 :
		sentence_length_average = round(nbWords/nbSentences)
	
	#Calcul du nombre de types de mots en complément de leur fréquence
	words_frequency = {}
	for word in words_list:
		if word not in words_frequency.keys():
			words_frequency[word]=1
		else:
			words_frequency[word]+=1
	
	#Calcul du nombre de types de mots
	nbWordTypes = len(words_frequency)
	
	#Calcul du nombre d'occurrences de chaque catégorie
	cat_frequency = {}
	nbCategories = 0 
	for element in categories_list :
		if element not in cat_frequency.keys():
			cat_frequency[element] = 1 
			nbCategories+=1
		else:
			cat_frequency[element]+=1
	
	#Tri par fréquence décroissante du nombre d'occurrences de chaque catégorie
	cat_freq_sorted=sorted(cat_frequency.items(), key = lambda e:e[1], reverse=True)
	
	#Calcul du nombre d'occurrences des couples lemmes-catégories
	cat_lem_frequency = {}
	for element in cat_lem_list:
		if element not in cat_lem_frequency.keys():
			cat_lem_frequency[element]=1 
		else:
			cat_lem_frequency[element]+=1
	
	#Calcul des hapax
	nbHapax = 0
	for key, value in words_frequency.items():
		if value == 1:
			nbHapax+=1		
	
	#Tri par fréquence décroissante du nombre d'occurrences des couples lemmes-catégories
	cat_lem_sorted=sorted(cat_lem_frequency.items(), key = lambda e:e[1], reverse=True)

	#Fermeture du fichier d'entrée
	input_file.close()
	
	#Ouverture du fichier de sortie
	output_file = open(os.path.join('./corpus_files/data_csv', os.path.basename(file_name[:-9]+"_data.csv")), mode='w', encoding='utf8')
	
	#Écriture des résultats de l'analyse dans le fichier de sortie 
	output_file.write("Les données suivantes sont issues de l'analyse de la production : "+os.path.basename(file_name[:-9])+"\n\n")
	output_file.write("Cette production contient : \n\n")
	output_file.write("\t"+str(nbTokens)+" forme(s)/token(s)\n\n")
	output_file.write("\t"+str(nbWords)+" mot(s)\n\n")
	output_file.write("\t"+str(nbHapax)+" hapax\n\n")
	output_file.write("\t"+str(nbCharacters)+" caractère(s)\n\n")
	output_file.write("\tUne moyenne de "+str(word_length_average)+" caractère(s) par mot\n\n")
	output_file.write("\t"+str(nbSentences)+" phrase(s)\n\n")
	
	if nbSentences != 0 :
		output_file.write("\tUne moyenne de "+str(sentence_length_average)+" mot(s) par phrase\n\n")
	
	output_file.write("\t"+str(nbWordTypes)+" type(s) de mots dont la distribution fréquentielle est la suivante :\n\n")
	
	for word, frequency in words_frequency.items():
		output_file.write("\t\t"+word+" : "+str(frequency)+"\n")
	
	output_file.write("\n\tListe (triée par fréquence décroissante) du nombre d'occurrences de chaque catégorie : \n\n")
	
	for element in cat_freq_sorted:
		output_file.write("\t\t"+str(element)+"\n")
	
	output_file.write("\n\tListe (triée par fréquence décroissante) des lemmes et de leurs catégories : \n\n")
	
	for element in cat_lem_sorted:
		output_file.write("\t\t"+str(element)+"\n")
	
	#Calcul et écriture des métriques
	output_file.write("\n\tRichesse lexicale (Type-Token Ratio) : "+str(nbWordTypes/nbWords)+"\n\n")
	output_file.write("\tScore BLEU : "+str(score)+"\n\n")
	output_file.write("\tPrécision : "+str(precision(reference_set, test_set))+"\n\n")
	output_file.write("\tRappel : "+str(recall(reference_set, test_set))+"\n\n")
	output_file.write("\tF-mesure : "+str(f_measure(reference_set, test_set))+"\n\n")
	
	#Fermeture du fichier de sortie
	output_file.close()
	
	csv_files_count += 1

#Messages affichés au terme de l'exécution du programme
##Affichage du nombre de productions étiquetées qui ont été analysées
###Affichage du temps d'exécution du programme
print("Analyse des productions étiquetées terminée !\n")

print(str(csv_files_count)+" productions étiquetées ont été analysées !\n")

print("Fin de l'exécution du programme !\n")

print("Programme exécuté en : "+str(time.time()-time0)+" seconde(s)")