#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tweet import *

class TweetDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
       
    #Retorna a lista de todas as rotas cadastrada no banco
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute(""" SELECT max(id), max(tokens), original, max(classe) FROM tweets WHERE tokens != '' GROUP BY original""")
		rows = cur.fetchall()
		cur.close()
		tweets = []
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3])
			tweets.append(tweet)
		return tweets

	#Retorna a lista de todas as rotas cadastrada no banco
	def selectClassesLimit(self, limit):
		tweets = []
		#Pegando Positivos
		cur = self.__conn.cursor()
		sql = """ SELECT max(id), max(tokens), original, max(classe) FROM tweets WHERE classe='positive' and tokens != '' GROUP BY original limit {0}"""
		sql = sql.format(limit)
		cur.execute(sql)
		
		rows = cur.fetchall()
		cur.close()
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3])
			tweets.append(tweet)

		#Pegando Negativos	
		cur = self.__conn.cursor()
		sql = """ SELECT max(id), max(tokens), original, max(classe) FROM tweets WHERE classe='negative' and tokens != '' GROUP BY original limit {0}"""
		sql = sql.format(limit)

		cur.execute(sql)
		rows = cur.fetchall()
		cur.close()
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3])
			tweets.append(tweet)
		return tweets
	

	#Insere uma lista de tuplas na tabela rotas
	def executeMany(self, tweets):
		if(tweets == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO tweets (id, tokens, original, classe) VALUES (%s,%s,%s,%s)""", tweets)
		self.__conn.commit()
		cur.close()