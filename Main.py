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

'''
tweets = readCSV('input/tweets.csv')
#print tweets

#abre conexão
#cria taxistaDAO
tweetDAO.executeMany(tweets);
'''

path = "bestSet.csv"
tweets = []
tweetsPositivos = [] 
tweetsNegativos = []


#lê melhor trainning set caso exista
if os.path.isfile(path): 
	tweetsPositivos, tweetsNegativos = readCSVToTweets(path)
	tweets = tweetsPositivos + tweetsNegativos
else:
	tweets = tweetDAO.selectAll()
	tweetsPositivos, tweetsNegativos = tweetDAO.selectClassesLimit(4500);
#for t in tweets: 
#	print t.tokens
#	print t.classe

#melhorPeso, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento = treinarModelo(tweets, 1000)
melhorPeso, accuracyDoMelhor, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento, bestConfusionMatrix = treinarModeloDatasetsDiferentes(tweetsPositivos, tweetsNegativos, 1000)

print "####################################"
print 'Melhor peso: ' + str(melhorPeso)
print 'Accuracy: ' + str(accuracyDoMelhor)
print 'Precision: ' + str(precisionDoMelhor)
print 'Recall: ' + str(recallDoMelhor)
print 'F-Measure: ' + str(fmeasureDoMelhor)

print "####################################"

print "\t" + "P\t" + "N\t"
print "P" + "\t" + str(bestConfusionMatrix[0]) + "\t" + str(bestConfusionMatrix[3])
print "N" + "\t" + str(bestConfusionMatrix[2]) + "\t" + str(bestConfusionMatrix[1])

#salva o melhor trainning set
bestSet = melhorBaseTreinamento[0] + melhorBaseTreinamento[1]
writeCSVFromTweets(bestSet, path)