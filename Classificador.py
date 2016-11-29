#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocessor.PreProcessor import *
from database.TweetDAO import *
from database.Tweet import *
from database.Connection import *
from naiveBayesClassifier.nbclassifier import *
from util import *
import os.path

connectionFactory = ConnectionFactory()
tweetDAO = TweetDAO(connectionFactory.getConnection())

#Ler twetts do csv e salvar no banco, necessário só na primeira vez
#tweets = readCSV('input/tweetsNoEmoji.csv')
#cria taxistaDAO
#tweetDAO.executeMany(tweets)

tweetsNoEmoji = tweetDAO.selectAllNoEmoji();
print "Total de tweets a serem classificados: " + str(len(tweetsNoEmoji))

path = "bestSet.csv"
tweets = []
tweetsPositivos = [] 
tweetsNegativos = []


#lê melhor trainning set caso exista
if os.path.isfile(path): 
	tweetsPositivos, tweetsNegativos = readCSVToTweets(path)
	tweets = tweetsPositivos + tweetsNegativos

	classificador = buildClassificador(tweetsPositivos, tweetsNegativos)
	count = 0
	tweetsSql = []
	for tweet in tweetsNoEmoji:
		classificadoComo = classificador.classificarMensagem(tweet.tokens)
		tweetsSql.append((tweet.id, classificadoComo))	
		count += 1
		print "Tweet: " + str(count)
	tweetDAO.executeManyClassificados(tweetsSql)
else:
	print 'Nenhuma base de treinamento encontrada'