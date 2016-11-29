import csv

def readCSV(path):
	with open(path, 'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';') 
		tweets = [];
		for row in reader:
			if(len(row.keys()) > 6):
				continue;
			data = 0
			if 'data' in row:
				data = row['data']
			tweet = [row['id'], row['tokens'], row['original'], row['classe'], row['emojis'], data];
			tweets.append(tuple(tweet));
		return tweets