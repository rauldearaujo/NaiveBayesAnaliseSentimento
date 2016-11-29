#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tweet import *

class TweetDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
       
    #Retorna a lista de todas as rotas cadastrada no banco
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute(""" SELECT id, tokens, original, classe, emojis FROM tweets WHERE tokens != '' """)
		rows = cur.fetchall()
		cur.close()
		tweets = []
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3], row[4])
			tweets.append(tweet)
		return tweets

	#Retorna a lista de todas as rotas cadastrada no banco
	def selectAllNoEmoji(self):
		cur = self.__conn.cursor()
		cur.execute(""" SELECT id, tokens, original, classe, emojis FROM tweets WHERE tokens != '' and classe='NoEmoji' """)
		rows = cur.fetchall()
		cur.close()
		tweets = []
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3], row[4])
			tweets.append(tweet)
		return tweets	

	#Retorna a lista de todas as rotas cadastrada no banco
	def selectClassesLimit(self, limit):
		tweetsPositivos = []
		tweetsNegativos = []
		#Pegando Positivos
		cur = self.__conn.cursor()
		sql = """ SELECT id, tokens, original, classe, emojis FROM tweets WHERE classe='positive' and tokens != '' limit {0}"""
		sql = sql.format(limit)
		cur.execute(sql)
		
		rows = cur.fetchall()
		cur.close()
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3],row[4])
			tweetsPositivos.append(tweet)

		#Pegando Negativos	
		cur = self.__conn.cursor()
		sql = """ SELECT id, tokens, original, classe, emojis FROM tweets WHERE classe='negative' and tokens != '' limit {0}"""
		sql = sql.format(limit)

		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3],row[4])
			tweetsNegativos.append(tweet)
		return tweetsPositivos, tweetsNegativos
	

	#Insere uma lista de tuplas na tabela rotas
	def executeMany(self, tweets):
		if(tweets == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO tweets (id, tokens, original, classe, emojis, data) VALUES (%s,%s,%s,%s,%s,%s)""", tweets)
		self.__conn.commit()
		cur.close()

	#Insere uma lista de tuplas na tabela rotas
	def executeManyClassificados(self, tweets):
		if(tweets == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO tweetsClassificados (id, classe) VALUES (%s,%s)""", tweets)
		self.__conn.commit()
		cur.close()