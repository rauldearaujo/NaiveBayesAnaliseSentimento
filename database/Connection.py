#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2

class ConnectionFactory:
	
	#Conexão com o banco de dados
	def getConnection(self):
		try:
		    __conn = psycopg2.connect("dbname='analisetweets' user='postgres' host='localhost' password='postgres'")
		    return __conn
		except:
		    print "Error connecting database"
		    return None