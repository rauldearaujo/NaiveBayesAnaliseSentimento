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

#tweets = tweetDAO.selectAll()
tweets = tweetDAO.selectClassesLimit(5000);

#for t in tweets: 
#	print t.tokens
#	print t.classe



melhorPeso, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento = treinarModelo(tweets, 1000)
print "####################################"
print 'Melhor peso: ' + str(melhorPeso)
print 'Precision: ' + str(precisionDoMelhor)
print 'Recall: ' + str(recallDoMelhor)
print 'F-Measure: ' + str(fmeasureDoMelhor)
