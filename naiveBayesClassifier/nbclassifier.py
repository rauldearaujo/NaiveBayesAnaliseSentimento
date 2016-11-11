#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import log
import random as rnd
import copy

POSITIVE = 'positive'
NEGATIVE = 'negative'

def treinarModelo(tweets, qtdLoops):
	qtdTweets = len(tweets)
	qtdTreino = int(qtdTweets * 0.7)
	melhorPeso = 0.0
	melhorBaseTreinamento = []
	precisionDoMelhor = 0.0
	recallDoMelhor = 0.0
	fmeasureDoMelhor = 0.0
	for i in range(qtdLoops):
		rnd.shuffle(tweets)
		tweetsTreinamento = tweets[0:qtdTreino]
		tweetsTeste = tweets[qtdTreino:qtdTweets]
		naiveBayesClassifier = NaiveBayes(tweetsTreinamento)
		print "V: " + str(naiveBayesClassifier.V)
		precision, recall, f_measure = classificar(tweetsTeste, naiveBayesClassifier)
		pesoAtual = f_measure
		print 'Precision: ' + str(precision) + '; Recall: - ' + str(recall) +  '; F-Measure - ' + str(f_measure)
		if pesoAtual > melhorPeso:
			melhorPeso = pesoAtual
			precisionDoMelhor = precision
			recallDoMelhor = recall
			fmeasureDoMelhor = f_measure
			melhorBaseTreinamento = copy.copy(tweets)
	return (melhorPeso, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento)		

def classificar(tweetsTeste, naiveBayesClassifier):
	TP = 0 #Positivo
	FP = 0
	TN = 0 #Negativo
	FN = 0	
	for tweet in tweetsTeste:
		if tweet.classe == POSITIVE:
			if tweet.classe == naiveBayesClassifier.classificarMensagem(tweet.tokens):
				TP+=1
			else:
				FP+=1
		elif tweet.classe == NEGATIVE:
			if tweet.classe == naiveBayesClassifier.classificarMensagem(tweet.tokens):
				TN+=1
			else:
				FN+=1
	precision = TP/float(TP+FP)
	recall = TP / float(TP + FN)
	f_measure = 2 * ((precision * recall)/(precision + recall))
	return (precision, recall, f_measure)

class NaiveBayes:

	def __init__(self, tweets):
		self.tweets = tweets
		self.POSITIVE = 'positive'
		self.NEGATIVE = 'negative'
		self.positiveMapCount = {}
		self.negativeMapCount = {}
		self.prepararVetorCaracteristico()

	def prepararVetorCaracteristico(self):
		self.vetorCaracteristico = []
		self.COUNT_P = 0
		self.COUNT_N = 0
		for tweet in self.tweets:
			tokens = tweet.tokens.split()
			if(tweet.classe == self.POSITIVE):
				self.COUNT_P += 1
				self.mapCount(tokens, self.positiveMapCount)
			else: 
				self.COUNT_N += 1
				self.mapCount(tokens, self.negativeMapCount)
			for token in tokens:
				if token not in self.vetorCaracteristico:
					self.vetorCaracteristico.append(token)
		self.V = len(self.vetorCaracteristico)

	def mapCount(self, tokens, cmap):
		for token in tokens:
			if token not in cmap:
				cmap[token] = 1
			else:
				cmap[token] += 1

	def tokenCount(self, cmap, token):
		try:
			return cmap[token]
		except Exception, e:
			return 0
	
	def probabilidade(self, token, classe):
		if classe == self.POSITIVE:
			return (self.tokenCount(self.positiveMapCount, token) + 1)/(1.0*(self.COUNT_P + self.V))
		else:
			return (self.tokenCount(self.negativeMapCount, token) + 1)/(1.0*(self.COUNT_N + self.V))

	def classificarMensagem(self, tokens):
		probabilidadeP = 0
		probabilidadeN = 0
		listTokens = tokens.split(' ')
		for token in listTokens:
			probabilidadeP += log(self.probabilidade(token, self.POSITIVE))
			probabilidadeN += log(self.probabilidade(token, self.NEGATIVE))
		if probabilidadeP > probabilidadeN:
			return self.POSITIVE
		else:
			return self.NEGATIVE
