import csv

def readCSV(path):
	with open(path, 'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';') 
		tweets = [];
		for row in reader:
			tweet = [row['id'], row['tokens'], row['original'], row['classe']];
			tweets.append(tuple(tweet));
		return tweets