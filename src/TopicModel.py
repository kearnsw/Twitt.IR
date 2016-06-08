# Part of this code is taken from:
# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck <L.J.Buitinck@uva.nl>
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause

from __future__ import print_function
import os
import csv
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def read_sample(fn):
    if os.path.basename(os.getcwd()) == "src":
        directory = os.path.dirname(os.getcwd()) + "/data/"
    else:
        directory = os.getcwd() + "/data/"
    tweets = []
    with open(directory + fn, 'rb') as f:
        reader = csv.reader(f, delimiter='\t', quotechar="|")
        for row in reader:
            row = row[0:6]
            tweets.append(row)
    tweets.pop(0)
    return tweets


class TopicModel:

    def __init__(self, _corpus, _num_topics, _num_words):
        self.corpus = _corpus
        self.num_topics = _num_topics
        self.num_words = _num_words
        self.tfidf_feature_names = []

    def calculate_tfidf(self):

        print("calculate tf-idf...")
        t0 = time()
        # create bag of words representation
        vectorizer = CountVectorizer(min_df=1, stop_words='english')
        X = vectorizer.fit_transform(self.corpus)

        # transform to tf-idf
        tfidf_vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(self.corpus)
        self.tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        print("done in %0.3fs." % (time() - t0))
        return tfidf

    def calculate_nmf(self, tfidf):
        # calculate
        print("Fitting NMF model with tf-idf features...")
        t0 = time()
        nmf = NMF(n_components=self.num_topics).fit(tfidf)
        print("done in %0.3fs." % (time() - t0))

        print("Topics in NMF model:")

        print_top_words(nmf, self.tfidf_feature_names, self.num_words)

    def calculate_lda(self, tfidf):
        print("Fitting LDA models with tf features...")
        lda = LatentDirichletAllocation(n_topics=self.num_topics, max_iter=5,
                                        learning_method='online', learning_offset=50.,
                                        random_state=0)
        t0 = time()
        lda.fit(tfidf)

        print("Topics in LDA model:")
        print_top_words(lda, self.tfidf_feature_names, self.num_words)
        print("done in %0.3fs." % (time() - t0))


'''if len(sys.argv) > 2:
    extracted_corpus = sys.argv[1]
else:
    extracted_corpus = "parsed04-19-14-46.json"


f_in = open("../data/" + extracted_corpus)
documents = json.load(f_in)

corpus = []
n_topics = 3
num_words = 10

print("Loading dataset...")
t0 = time()
# Load data
for document in documents:
    for key in document:
        parsed = document[key]
        description = parsed["description"]
        corpus.append(description)
print("done in %0.3fs." % (time()-t0))
'''




"""
        tokens = nltk.word_tokenize(description.lower())
        bagOfWords = dict()
        for token in tokens:
            if token in bagOfWords:
                bagOfWords[token] += 1
            else:
                bagOfWords[token] = 1

        sorted_words = sorted(bagOfWords.items(), key=operator.itemgetter(1), reverse=True)
        print sorted_words
"""