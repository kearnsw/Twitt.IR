import nltk
import csv

filename = ""
f = open(filename)
tagged_sentences = csv.reader(f)
feature_set = [(words, category) for words, category in tagged_sentences]
train_set, test_set = feature_set[:(.9*len(feature_set))],\
                      feature_set[(.9*len(feature_set)):]
nb = nltk.NaiveBayesClassifier
nb.train(train_set)