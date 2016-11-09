import csv

def readCSV(path):
	with open(path, 'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';') 
		tweets = [];
		for row in reader:
			tweet = [row['id'], row['tokens'], row['original']];
			if('group' in row):
				tweet.append(row['group'])
			else:
				tweet.append(0);
			tweets.append(tuple(tweet));
		return tweets