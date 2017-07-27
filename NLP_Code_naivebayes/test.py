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

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

def main():
    
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
            if rating == '5':
                the_list.append((t_review, "pos"))
            else:
                the_list.append((t_review, "neg"))
        print(the_list)
#     print(the_list)
    
    save_documents = open("pickled_algos/documents.pickle","wb")
    pickle.dump(the_list, save_documents)
    save_documents.close()
    
    open_txt = open("temp.txt","r").read()
    
    all_words = []
    
    tokens = word_tokenize(open_txt)
    
    for w in tokens:
        all_words.append(w.lower())
    
    all_words = nltk.FreqDist(all_words)
    word_features = list(all_words.keys())[:3000]
    
    save_word_features = open("pickled_algos/word_features5k.pickle","wb")
    pickle.dump(word_features, save_word_features)
    save_word_features.close()
    
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
    
    cl = nltk.NaiveBayesClassifier.train(training_set)
    print("Naive Bayes classifier: ", (nltk.classify.accuracy(cl,testing_set))*100)
    cl.show_most_informative_features(15)
    
    save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
    pickle.dump(cl, save_classifier)
    save_classifier.close()
    
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
    
    save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    
    
    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)
    print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

    save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
    
    save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    
    
    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)
    print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
    
    save_classifier = open("pickled_algos/SGDClassifier_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
    
    save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    
    
    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier.train(training_set)
    print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
    
    save_classifier = open("pickled_algos/NuSVC_classifier5k.pickle","wb")
    pickle.dump(MNB_classifier, save_classifier)
    save_classifier.close()    
    
    voted_classifier = VoteClassifier(
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

    
main()