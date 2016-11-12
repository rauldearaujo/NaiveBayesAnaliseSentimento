#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from database.Tweet import *

header = ['id','tokens','original','classe']
POSITIVE = 'positive'
NEGATIVE = 'negative'

def readCSV(path):
	with open(path, 'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
		tweetsPositivos = [];
		tweetsNegativos = [];
		
		for row in reader:
			tweet = Tweet(row['id'], row['tokens'], row['original'], row['classe']);
			if(tweet.classe == POSITIVE):
				tweetsPositivos.append(tweet);
			else:
				tweetsNegativos.append(tweet);

		return tweetsPositivos,tweetsNegativos

def writeCSV(tweets, path):
	with open(path, 'wb') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=';',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	    spamwriter.writerow(header)
	    for tweet in tweets:
	    	spamwriter.writerow([tweet.id, tweet.tokens, tweet.original, tweet.classe])