from pymongo import MongoClient
from config import MONGO_URI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import sys
import numpy as np
from random import shuffle
import cPickle

charsToRemove = ['"', ".", "@", "'", ',', '(', ')', '[', ']', '-', '+', "_"]

def lexicon_classifier(tweets, concept):
    if concept == "humor":
        features = ["U0001f602", "lol", "lmao", "rofl", "haha", "hahaha",
                    "welp", "arse", "ass", "U0001f606", "Drumpf",
                    "skeeter", "fun", "head", "damn", "bite", "great"]
    elif concept == "mistrust":
        features = ["illegal", "illegals", "immigrants", "mexicans", "prince",
                    "false", "fake", "scheme", "hoax", "conspiracy",
                    "monsanto", "depopulation", "gmo" "hype", "bio-warfare",
                    "fabricating", "fabrication", "prince", "aretha", "franklin",
                    "fabricating", "god", "vaccines", "system", "created", "vaxxed",
                    "border", "admits"]
    elif concept == "relief":
        features = ["test", "fight", "fda", "unveils", "uniforms", "scientists", "zikaproof",
                    "ebola", "approval", "diagnostics", "drop"]

    predictions = []

    for tweet in tweets:
        for char in charsToRemove:
            tweet = tweet.replace(char, " ")
        parsed = tweet.encode("unicode-escape").split("\\")
        parsed = " ".join(parsed).lower().split()

        for feature in features:
            if feature.lower() in parsed:
                prediction = 1
                break
            else:
                prediction = 0

        predictions.append(prediction)

    return predictions

# Import training data
client = MongoClient(MONGO_URI)
db = client.get_default_database()
cursor = db["submissions"].find({})

submissions = []
for document in cursor:
    if "tweet" in document:
        submissions.append(document)

shuffle(submissions)

corpus = []
target = []
humor_words = []
query = sys.argv[1]
inputFile = sys.argv[2]
count = 0


for submission in submissions:
    for char in charsToRemove:
            submission["tweet"]["text"] = submission["tweet"]["text"].replace(char, " ")
    corpus.append(submission["tweet"]["text"].encode("unicode-escape").strip().lower())
    if submission["data"][query] == "true":
        target.append(1)
        count += 1
    else:
        target.append(0)
print count

if inputFile == "test":
    train_corpus = corpus[:int((.9 * len(corpus)))]
    train_target = target[:int((.9 * len(corpus)))]
    test_corpus = corpus[int((.9 * len(corpus))):]
    test_target = target[int((.9 * len(corpus))):]

# Count features
count_vect = CountVectorizer(ngram_range=(1, 2))
train_counts = count_vect.fit_transform(train_corpus)
with open("count_vect.pk1", "wb") as f:
    cPickle.dump(count_vect, f)

# Convert to tfidf
tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_counts)
with open("tfidf.pk1", "wb") as f:
    cPickle.dump(tfidf_transformer, f)

# Train classifier
clf = MultinomialNB().fit(train_tfidf, train_target)

# Transform test data
test_counts = count_vect.transform(test_corpus)
test_tfidf = tfidf_transformer.transform(test_counts)

# Predict test values
if query == "concern":
    predicted = clf.predict(test_tfidf)
else:
    predicted = lexicon_classifier(test_corpus, query)

print predicted

print np.mean(predicted == test_target)
print "--------------------------------------"

metrics = metrics.classification_report(test_target, predicted,
                                        target_names=['other', query])

for i in range(len(predicted)):
    if predicted[i] != test_target[i] and test_target[i] == 0:
        print("False Positive: " + test_corpus[i])
    elif predicted[i] != test_target[i] and test_target[i] == 1:
        print("False Negative: " + test_corpus[i])
    else:
        if test_target[i] == 1:
            print("Correctly Identified: " + test_corpus[i])

print metrics

with open("concernClassifier.pk1", "wb") as f:
    cPickle.dump(clf, f)
"""
features = extract_features(submissions)
unigram_features = features["word_features"]
bigram_features = features["bigram_features"]
"""
