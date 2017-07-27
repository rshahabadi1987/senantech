import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.classify.scikitlearn import SklearnClassifier
from sqlalchemy.sql.expression import all_
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import pickle
import ast
import pandas as pd
import numpy    
from dask.array.fft import scipy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



#      Load file
the_list = []
#     open_txt = open("D:/Hemant/Projects/Python/rating_review_test.txt","r").read()
file = open("temp.txt","w")
with open("D:/Hemant/Projects/Python/rating_review_full_test.txt") as f:
    for lines in f:
        line = lines.split('#')
        print(line)
        review = line[4]
        rating = line[3]
            
        file.write(review + '\n')
            
        t_review = review
        if ast.literal_eval(rating) > 4 :
            the_list.append((t_review, "5"))
        elif ast.literal_eval(rating) > 3:
            the_list.append((t_review, "4"))
        elif ast.literal_eval(rating) > 2:
            the_list.append((t_review, "3"))
        elif ast.literal_eval(rating) > 1:
            the_list.append((t_review, "2"))
        elif ast.literal_eval(rating) > 0:
            the_list.append((t_review, "1"))
                
    print(the_list)
#     print(the_list)
    
#     save_documents = open("documents.pickle","wb")
#     pickle.dump(the_list, save_documents)
#     save_documents.close()
    
open_txt = open("temp.txt","r").read()
    
all_words = []
    
tokens = word_tokenize(open_txt)
    
for w in tokens:
    all_words.append(w.lower())
    
all_words = nltk.FreqDist(all_words)

word_features5k_f = open("word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

# word_features = list(all_words.keys())[:3000]
    
#     save_word_features = open("word_features5k.pickle","wb")
#     pickle.dump(word_features, save_word_features)
#     save_word_features.close()
    
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features
    
    
featuresets = [(find_features(rev),category) for (rev,category) in the_list]


random.shuffle(featuresets)
    
training_set = featuresets[:1000]
testing_set = featuresets[1000:]

output = open("sentiment_output_toyota_4.csv","a")

with open("D:/Hemant/Projects/Python/toyota_data.txt") as x:
    for lines in x:
        line = lines.split('#')
        sentence = line[4].rstrip()
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(sentence)
        print("{:-<65} {}".format(sentence, str(vs)))
        output.write("{:-<65} {}".format(sentence, str(vs)) + '\n')









