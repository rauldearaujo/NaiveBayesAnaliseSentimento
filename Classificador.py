#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database.Tweet import *
from naiveBayesClassifier.nbclassifier import *
from util import *
import os.path

path = "bestSet.csv"
tweets = []
tweetsPositivos = [] 
tweetsNegativos = []


#lê melhor trainning set caso exista
if os.path.isfile(path): 
	tweetsPositivos, tweetsNegativos = readCSVToTweets(path)
	tweets = tweetsPositivos + tweetsNegativos

	classificador = buildClassificador(tweetsPositivos, tweetsNegativos)
else:
	print 'Nenhuma base de treinamento encontrada'