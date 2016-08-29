from pymongo import MongoClient
import cPickle
import sys
from AnnotweetClassifier import lexicon_classifier
from bson import json_util
import json

def pipeline(data):
    counts = count_vect.transform(data)
    tfidf = tfidf_transformer.transform(counts)
    return clf.predict(tfidf)

with open('concernClassifier.pk1', 'rb') as f:
    clf = cPickle.load(f)

with open('count_vect.pk1', 'rb') as f:
    count_vect = cPickle.load(f)

with open('tfidf.pk1', 'rb') as f:
    tfidf_transformer = cPickle.load(f)

output = open('../data/mistrustData.tsv', "wb")
output.write("Month\tDay\tCount\tTotal\n")

data = open('../data/subset.json', "wb")

client = MongoClient()
db = client["Twitter"]
charsToRemove = ['"', ".", "@", "'", ',', '(', ')', '[', ']', '-', '+', "_"]


def getTweets(date, type):
    for month in range(1, 13):
        for day in range(1, 32):
            print "Processing 2016-" + str(month) + "-" + str(day) + "..."
            tweets = []
            entries = []

            # Pull all english tweets from DB
            cursor = db["Zika"].find({"lang": "en"})
            for document in cursor:
                if document["created_at"].month == month:
                    if document["created_at"].day == day:
                        entries.append(document)
                        for char in charsToRemove:
                            document["text"].replace(char, " ")
                        tweets.append(document["text"].encode("unicode-escape").strip().lower())
            if len(tweets) == 0:
                break

            # Classify input perception
            if sys.argv[1] == "concern":
                predicted = pipeline(tweets)
            else:
                predicted = lexicon_classifier(tweets, sys.argv[1])

            #

            count = 0
            for i in range(len(predicted)):
                if predicted[i] == 1:
                    count += 1
            output.write(str(month) + "\t" + str(day) + "\t" + str(count) + "\t" + str(len(predicted)) + "\n")

            for i in range(len(entries)):
                if predicted[i] == 1:
                    json.dump(entries[i], data, default=json_util.default)
                    data.write(",\n")
                    db.Zika.update({"_id": entries[i]["_id"]},
                                   {"$set": {"humor": "true"}})

        # Store result in database

getTweets("2016-04-12", "humor")