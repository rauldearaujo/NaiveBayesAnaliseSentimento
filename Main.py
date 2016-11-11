#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocessor.PreProcessor import *
from database.TweetDAO import *
from database.Tweet import *
from database.Connection import *
from naiveBayesClassifier.nbclassifier import * 
import random as rnd

connectionFactory = ConnectionFactory()
tweetDAO = TweetDAO(connectionFactory.getConnection())

'''
tweets = readCSV('input/tweets.csv')
#print tweets

#abre conexão
#cria taxistaDAO
tweetDAO.executeMany(tweets);
'''

tweets = tweetDAO.selectAll()
#for t in tweets: 
#	print t.tokens
#	print t.classe

'''	
tweet1 = Tweet(1, "Chinese Beijing Chinese", "Chinese Beijing Chinese", 'positive')
tweet2 = Tweet(2, "Chinese Chinese Shangai", "Chinese Shangai Chinese", 'positive')
tweet3 = Tweet(3, "Chinese Macao", "Chinese Macao", 'positive')
tweet4 = Tweet(4, "Tokyo Japan Chinese", "Tokyo Japan Chinese", 'negative')
tweets = [tweet1,tweet2,tweet3,tweet4]
'''

melhorPeso, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento = treinarModelo(tweets)
print "####################################"
print 'Melhor peso: ' + str(melhorPeso)
print 'Precision: ' + str(precisionDoMelhor)
print 'Recall: ' + str(recallDoMelhor)
print 'F-Measure: ' + str(fmeasureDoMelhor)