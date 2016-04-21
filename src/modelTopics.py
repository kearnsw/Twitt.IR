import os
import csv
from TopicModel import TopicModel


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

# Read in Data
directory = os.path.dirname(os.getcwd()) + "/data/"
tweets = []
with open(directory + "sample_4_04.tsv", 'rb') as f:
    reader = csv.reader(f, delimiter='\t', quotechar="|")
    for row in reader:
        row = row[0:6]
        tweets.append(row)
tweets.pop(0)
print tweets

humor = []
misinformation = []
relief = []
concern = []

print ("Classifying tweets...")
for tweet in tweets:
    print tweet[1]
    if tweet[2] == "1":
        humor.append(tweet[1])
    if tweet[3] == "1":
        misinformation.append(tweet[1])
    if tweet[4] == "1":
        relief.append(tweet[1])
    if tweet[5] == "1":
        concern.append(tweet[1])

humor_model = TopicModel(humor, 2, 5)
tfidf = humor_model.calculate_tfidf()
humor_model.calculate_nmf(tfidf)




