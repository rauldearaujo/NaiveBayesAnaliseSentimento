#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tweet import *

class TweetDAO:
	
	def __init__(self, __conn):
		self.__conn = __conn
       
    #Retorna a lista de todas as rotas cadastrada no banco
	def selectAll(self):
		cur = self.__conn.cursor()
		cur.execute("""SELECT id, tokens, original, grupo from tweets order by grupo""")
		rows = cur.fetchall()
		cur.close()
		tweets = []
		for row in rows:
			tweet = Tweet(row[0],row[1],row[2],row[3])
			tweets.append(tweet)
		return tweets

	#Insere uma lista de tuplas na tabela rotas
	def executeMany(self, tweets):
		if(tweets == None):
			return 
		cur = self.__conn.cursor()
		cur.executemany("""INSERT INTO tweets (id, tokens, original, grupo) VALUES (%s,%s,%s,%s)""", tweets)
		self.__conn.commit()
		cur.close()