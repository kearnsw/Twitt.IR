import os
import csv
from TopicModel import TopicModel
from TopicModel import read_sample
import nltk


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))


# Read in Data
tweet_data = read_sample("sample_3_31.tsv")
corpus = []
for item in tweet_data:
    corpus.append(item[1])
"""
model = TopicModel(corpus, 8, 5)
tfidf = model.calculate_tfidf()
model.calculate_nmf(tfidf)
"""
tweets = read_sample("sample_4_04.tsv")
tweets.append(read_sample("sample_4_06.tsv"))
tweets.append(read_sample("sample_4_08.tsv"))

humor = []
misinformation = []
relief = []
concern = []

print ("Classifying tweets...")
for tweet in tweets:
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

print("-----------------------------------------------")

concern_model = TopicModel(concern, 3, 5)
tfidf = concern_model.calculate_tfidf()
concern_model.calculate_nmf(tfidf)

print("-----------------------------------------------")

relief_model = TopicModel(relief, 3, 5)
tfidf = relief_model.calculate_tfidf()
relief_model.calculate_nmf(tfidf)

print("-----------------------------------------------")

misinformation_model = TopicModel(misinformation, 2, 5)
tfidf = misinformation_model.calculate_tfidf()
misinformation_model.calculate_nmf(tfidf)



