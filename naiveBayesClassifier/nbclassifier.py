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
		tweetsTreinamento = tweets[0:qtdTreino]
		tweetsTeste = tweets[qtdTreino:qtdTweets]
		naiveBayesClassifier = NaiveBayes(tweetsTreinamento)
		print "V: " + str(naiveBayesClassifier.V)
		accuracy, precision, recall, f_measure, TP, FP, TN, FN  = classificar(tweetsTeste, naiveBayesClassifier)
		pesoAtual = accuracy
		print 'Precision: ' + str(precision) + '; Recall: - ' + str(recall) +  '; F-Measure - ' + str(f_measure)
		if pesoAtual > melhorPeso:
			melhorPeso = pesoAtual
			precisionDoMelhor = precision
			recallDoMelhor = recall
			fmeasureDoMelhor = f_measure
			melhorBaseTreinamento = copy.copy(tweets)
		rnd.shuffle(tweets)
	return (melhorPeso, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento)		

def treinarModeloDatasetsDiferentes(tweetsPositivos, tweetsNegativos, qtdLoops):
	qtdTweetsPositivos = len(tweetsPositivos)
	qtdTweetsNegativos = len(tweetsNegativos)

	qtdTreino = int(qtdTweetsPositivos * 0.7)
	indiceUltimoTeste = qtdTweetsPositivos
	if(len(tweetsNegativos) < len(tweetsPositivos)):
		qtdTreino = int(qtdTweetsNegativos * 0.7)
		indiceUltimoTeste = qtdTweetsNegativos

	qtdTreinoPositivos = qtdTreino
	qtdTreinoNegativos = qtdTreino
	
	melhorPeso = 0.0
	melhorBaseTreinamento = ()
	precisionDoMelhor = 0.0
	recallDoMelhor = 0.0
	fmeasureDoMelhor = 0.0
	accuracyDoMelhor = 0.0
	bestConfusionMatrix = []
	for i in range(qtdLoops):

		tweetsTreinamentoPositivos = tweetsPositivos[0:qtdTreinoPositivos]
		tweetsTreinamentoNegativos = tweetsNegativos[0:qtdTreinoNegativos]
		tweetsTreinamento = tweetsTreinamentoPositivos + tweetsTreinamentoNegativos

		tweetsTestePositivos = tweetsPositivos[qtdTreinoPositivos:indiceUltimoTeste]
		tweetsTesteNegativos = tweetsNegativos[qtdTreinoNegativos:indiceUltimoTeste]
		tweetsTeste = tweetsTestePositivos + tweetsTesteNegativos

		naiveBayesClassifier = NaiveBayes(tweetsTreinamento)
		accuracy, precision, recall, f_measure, TP, FP, TN, FN = classificar(tweetsTeste, naiveBayesClassifier)
		pesoAtual = accuracy
		if pesoAtual > melhorPeso:
			print 'Accuracy:' + str(accuracy) + '; Precision: ' + str(precision) + '; Recall: - ' + str(recall) +  '; F-Measure - ' + str(f_measure)
			print 'TP: ' + str(TP) + "; FP: " + str(FP) + "; TN: " + str(TN) + '; FN: ' + str(FN)
			melhorPeso = pesoAtual
			precisionDoMelhor = precision
			recallDoMelhor = recall
			fmeasureDoMelhor = f_measure
			accuracyDoMelhor = accuracy
			melhorBaseTreinamento = (copy.copy(tweetsPositivos), copy.copy(tweetsNegativos))
			bestConfusionMatrix = [TP, FP, TN, FN]
		#shuffle list
		rnd.shuffle(tweetsPositivos)
		rnd.shuffle(tweetsNegativos)
		print "Treino: " + str(i)
	return (melhorPeso, accuracyDoMelhor, precisionDoMelhor, recallDoMelhor, fmeasureDoMelhor, melhorBaseTreinamento, bestConfusionMatrix)		


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
				FN+=1
		elif tweet.classe == NEGATIVE:
			if tweet.classe == naiveBayesClassifier.classificarMensagem(tweet.tokens):
				TN+=1
			else:
				FP+=1
	precision = TP/float(TP+FP)
	recall = TP / float(TP + FN)
	f_measure = 2 * ((precision * recall)/(precision + recall))
	accuracy = (TP + TN)/float(len(tweetsTeste)) 
	return (accuracy, precision, recall, f_measure, TP, FP, TN, FN)

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
