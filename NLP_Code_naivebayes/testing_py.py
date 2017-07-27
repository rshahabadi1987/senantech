import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import *
from sqlalchemy.sql.expression import all_


def nltk_stuff(lines):
    line = lines.split('#')
    review = line[4]
    
    stemmer = SnowballStemmer("english")
    stemmed = stemmer.stem(review)
    
    stopset = set(stopwords.words('english'))
    tokens=word_tokenize(str(stemmed))
    for w in tokens:
        if w not in stopset:
            tokens = w
    return tokens

def loadCsv():
    the_list = []
    with open("D:/Hemant/Projects/Python/rating_review_test.txt") as f:
        for lines in f:
            line = lines.split('#')
            review = line[4]
            rating = line[3]
#             the_list.append((review, rating))
            t_review = review
#             t_review = nltk_stuff(review) 
            if rating == '5':
                the_list.append((t_review, "pos"))
            else:
                the_list.append((t_review, "neg"))
    yield lines

def find_features(document):
    
    line = nltk_stuff(document)
    
    all_words = []
    for w in line:
        all_words.append(w.lower())
    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:5000]
    
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

def put_tag(lines):
    line = lines.split('#')
    the_list = []
    review = line[4]
    rating = line[3]
    if rating == '5':
        the_list.append((review, "pos"))
    else:
        the_list.append((review, "neg"))
    return the_list
    
def main():
    line = loadCsv()
    documents = put_tag(line)
    print("taged line: "+str(documents))
    features = find_features(line)
    featuresets = [(features, category) for (rev, category) in documents]
    random.shuffle(featuresets)
    training_set = featuresets[:10000]
    testing_set =  featuresets[10000:]
    
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
    classifier.show_most_informative_features(15)
    
main()





