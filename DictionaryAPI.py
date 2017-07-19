import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

filename = "USFordSentiments.csv"
f= open(filename, "a")
headers = " Review , Score \n"
f.write(headers)
df = pd.read_csv("US_Ford.csv", usecols=['comments'])
print(df.comments)
TEXT = df.comments
analyzer = SentimentIntensityAnalyzer()
for sentence in TEXT:
	vs = analyzer.polarity_scores(sentence)
	print("{:-<65} {}".format(sentence, str(vs)))
	f.write (sentence + ","+ str(vs)+ "\n")
f.close()
