import nltk
import random
from TopicModel import read_sample


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    for bigram in bigram_features:
        features['contains({})'.format(bigram)] = (bigram in document)
    return features


class Classifier:
    def __init__(self, tweets):
        self.documents = []
        self.tweets = tweets
        self.tag = ""

    def tag_sample(self, tag):
        self.tag = tag
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

    def test(self, test_set, classifier):
        print(nltk.classify.accuracy(classifier, test_set))
        classifier.show_most_informative_features(10)
        count = 0
        for item in test_set:
            if classifier.classify(item[0]) == self.tag:
                count += 1
        print ("Found " + str(count) + " tweets in the " + self.tag + " category.")

        return count

    def run(self, tag):
        self.tag_sample(tag)
        feature_set = self.features()
        train_set = feature_set[:int((.9 * len(feature_set)))]
        test_set = feature_set[int((.9 * len(feature_set))):]
        classifier = self.train(train_set)
        self.test(test_set, classifier)

tweets = read_sample("sample_4_18_tram.tsv")
tweets = tweets + read_sample("sample_4_04_tram.csv")
tweets = tweets + read_sample("sample_4_06_tram.csv")
tweets = tweets + read_sample("sample_4_08_tram.csv")
tweets = tweets + read_sample("sample_4_10_tram.csv")
tweets = tweets + read_sample("sample_4_12_tram.csv")
tweets = tweets + read_sample("sample_4_19_tram.tsv")
tweets = tweets + read_sample("sample_4_20_tram.tsv")
tweets = tweets + read_sample("sample_4_21_tram.tsv")

# tweets = [tweet for tweet_set in tweets for tweet in tweet_set]
corpus = []
dictionary = []

for tweet in tweets:
    corpus.append(tweet[1])
    random.shuffle(corpus)

vocab = [word for tweet in corpus for word in tweet.split()]

# create unigram features
all_words = nltk.FreqDist(w.lower() for w in vocab)
word_features = list(all_words)[:1000]

# create bigram features
finder = nltk.BigramCollocationFinder.from_words(vocab,
                                                 window_size=3)
finder.apply_freq_filter(4)
bigram_features = []
bigram_measures = nltk.collocations.BigramAssocMeasures
for k, v in finder.ngram_fd.items():
    bigram = " ".join(k)
    bigram_features.append(bigram)

print ("Classifying humor...")
humor_classifier = Classifier(tweets)
humor_classifier.run("humor")

print ("Classifying mistrust...")
mistrust_classifier = Classifier(tweets)
mistrust_classifier.run("mistrust")

print ("Classifying relief...")
relief_classifier = Classifier(tweets)
relief_classifier.run("relief")

print ("Classifying concern...")
concern_classifier = Classifier(tweets)
concern_classifier.run("concern")

