#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import log

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