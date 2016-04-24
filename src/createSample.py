from __future__ import print_function
import os
import re
import random
from time import time
from Filter import Filter
from Request import Request

# Create request object to handle user input.
q = Request()
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}
date = q.date.split()
month = date[0]
day = date[1]

# connect to Mongo and search based on criteria
q.connect()
criteria = {"lang": "en", "created_at": {'$regex': q.date},
            "text": {"$not": re.compile("RT")}}
cursor = q.search(criteria, {"text": 1})

# load tweet with id
corpus = []
ids = []
tweet_filter = Filter(25)
for document in cursor:
    text = ' '.join(document["text"].encode("utf-8").split())
    corpus.append(text)
    ids.append(document["_id"])

# filter repeated tweets
t0 = time()
i = 0
status = -1
unique_tweets = ["Dummy Tweet"]
length = len(corpus)

print("Filtering tweets may take a few minutes...")
for document in corpus:
    for tweet in unique_tweets:
        status = tweet_filter.check_duplicates(document, tweet)
        if status:
            break
    if not status:
        unique_tweets.append(document)
    i += 1
    if i > 3000:
        break

print("done in %0.3fs." % (time() - t0))
unique_tweets.pop(0)
corpus = unique_tweets
# create sample by bootstrap sampling
random_indices = random.sample(range(0, len(corpus)), q.num_of_docs)

# Open file I/O streams
directory = os.getcwd()
fn = "sample_" + str(months[month]) + "_" + str(day) + ".tsv"
f = open(directory + "/data/" + fn, "w+")
urls = open(directory + "/data/urls.json", "w+")

# Write samples of URLs and tweets linked by Mongo id
count = 0
print ("Creating a sample from the collection in the " + q.database +
       " database for the date " + q.date + "...")

urls.write("{ ")
f.write("ID\t TEXT\t HUMOR\t MISINFORMATION\t DOWNPLAY\t CONCERN\t GENERAL INFORMATION \n")
for index in random_indices:
    f.write(str(ids[index]) + "\t" + corpus[index] +
            "\t \t \t \t \t \n")
    # Extract URL
    tokens = corpus[index].split()
    num_urls = 0
    for token in tokens:
        if "http" in token and num_urls == 0:
            tokens.remove(token)
            if count > 0:
                urls.write(", \n")
            # json.dump({str(document["_id"]): token}, urls)
            urls.write('"' + str(ids[index]) + '": "' + token + '"')
            count += 1
            num_urls += 1
urls.write("}")
