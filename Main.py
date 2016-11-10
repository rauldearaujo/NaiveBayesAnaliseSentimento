#!/usr/bin/env python
# -*- coding: utf-8 -*-

from preprocessor.PreProcessor import *
from database.TweetDAO import *
from database.Tweet import *
from database.Connection import *
from naiveBayesClassifier.nbclassifier import * 

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
qtdTweets = len(tweets)
qtdTreino = int(qtdTweets * 0.7)
naiveBayesClassifier = NaiveBayes(tweets[0:qtdTreino])
print naiveBayesClassifier.V

qtdT = 0
qtdF = 0
for tweet in tweets[qtdTreino:qtdTweets]:
	if tweet.classe == naiveBayesClassifier.classificarMensagem(tweet.tokens):
		qtdT+=1
	else:
		qtdF+=1
print qtdT
print qtdF