import os
import sys
import nltk
import random
from TopicModel import read_sample


def read_data():
    tweets = []
    if os.path.basename(os.getcwd()) == "src":
        directory = os.path.dirname(os.getcwd()) + "/data/train"
    else:
        directory = os.getcwd() + "/data/train"
    for f in os.listdir(directory):
        tweets += read_sample("train/" + f)
    return tweets


def extract_features(tweets):
    corpus = []
    for tweet in tweets:
        corpus.append(tweet[1])

    vocab = [word for tweet in corpus for word in tweet.split()]

    # collect unigram features
    word_dist = nltk.FreqDist(w.lower() for w in vocab)
    word_features = list(word_dist)[:2000]

    # collect bigram features
    finder = nltk.BigramCollocationFinder.from_words(vocab, window_size=3)
    finder.apply_freq_filter(4)
    bigram_features = []
    for key, value in finder.ngram_fd.items():
        bigram = " ".join(key)
        bigram_features.append(bigram)

    # collect features to be returned
    features = dict()
    features["word_features"] = word_features
    features["bigram_features"] = bigram_features
    return features


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    for bigram in bigram_features:
        features['contains({})'.format(bigram)] = (bigram in document)
    return features


class Classifier:
    def __init__(self, tweets, tag):
        self.documents = []
        self.tweets = tweets
        self.tag = tag

    def tag_sample(self):
        tag = self.tag
        for tweet in self.tweets:
            if tweet[2] == "1" and tag == "humor":
                self.documents.append((tweet[1].lower().split(), "humor"))
            if tweet[3] == "1" and tag == "mistrust":
                self.documents.append((tweet[1].lower().split(), "mistrust"))
            if tweet[4] == "1" and tag == "relief":
                self.documents.append((tweet[1].lower().split(), "relief"))
            if tweet[5] == "1" and tag == "concern":
                self.documents.append((tweet[1].lower().split(), "concern"))
            else:
                self.documents.append((tweet[1].lower().split(), "other"))

    def features(self):
        return [(document_features(doc), cat) for (doc, cat) in self.documents]

    def train(self, training_set):
        return nltk.NaiveBayesClassifier.train(training_set)

    def test(self, document_set, classifier):
        print(nltk.classify.accuracy(classifier, document_set))
        classifier.show_most_informative_features(10)
        count = 0
        for document in document_set:
            if classifier.classify(document[0]) == self.tag:
                count += 1
        print ("Found " + str(count) + " tweets in the " + self.tag + " category.")

        return count

    def run(self, document):
        self.tag_sample()
        random.shuffle(self.documents)
        feature_set = self.features()
        train_set = feature_set[:int((.9 * len(feature_set)))]
        classifier = self.train(train_set)

        if document is None:
            test_set = feature_set[int((.9 * len(feature_set))):]
            self.test(test_set, classifier)

        return classifier

# Create and train the four classifiers
tweets = read_data()
features = extract_features(tweets)
word_features = features["word_features"]
bigram_features = features["bigram_features"]

print ("Training humor classifier...")
humor = Classifier(tweets, "humor")
humor_classifier = humor.run(None)

print ("Training concern classifier...")
concern = Classifier(tweets, "concern")
concern_classifier = concern.run(None)

print ("Training mistrust classifier...")
mistrust = Classifier(tweets, "mistrust")
mistrust_classifier = mistrust.run(None)

print ("Training relief classifier...")
relief = Classifier(tweets, "relief")
relief_classifier = relief.run(None)

# Run classifiers on a dataset
print("Classifying twitter data...")
fn = sys.argv[1]
data = read_sample(fn)

for document in data:
    tweet = document[1].lower().split()
    features = document_features(tweet)

    concern_value = concern_classifier.classify(features)
    # mistrust_value = mistrust_classifier.classify(features)
    # relief_value = relief_classifier.classify(features)
    # humor_value = humor_classifier.classify(features)
    if concern_value == "concern":
        print concern_value
        print document[1]

"""
    if humor_value == "humor":
        print humor_value

    if mistrust_value == "mistrust":
        print mistrust_value

    if relief_value == "relief":
        print relief_value
"""






