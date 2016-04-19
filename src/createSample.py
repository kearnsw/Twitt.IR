from pymongo import MongoClient
import sys
import re
import os
import random
import json


class Request:

    def __init__(self):

        if len(sys.argv) >= 2:
            self.database = sys.argv[1]
        else:
            self.database = "Virus"

        if len(sys.argv) >= 3:
            self.collection = sys.argv[2]
        else:
            self.collection = "Zika"

        if len(sys.argv) >= 5:
            self.num_of_docs = sys.argv[4]
        else:
            self.num_of_docs = 100

        if len(sys.argv) >= 4:
            self.date = sys.argv[3]
        else:
            self.date = "Mar 31"

# Create request object to handle user input.
q = Request()
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}
date = q.date.split()
month = date[0]
day = date[1]

# Open file I/O streams
directory = os.getcwd() + "/data/"
fn = "sample_" + str(months[month]) + "_" + str(day) + ".tsv"
f = open(directory + fn, "w+")
urls = open(directory + "urls.txt", "w+")

# Open connection to client
client = MongoClient()
db = client[q.database]
coll = db[q.collection]

# Set search criteria
criteria = {"lang": "en", "created_at": {'$regex': q.date},
            "text": {"$not": re.compile("RT")}}
cursor = coll.find(criteria, {"text": 1})

# load tweet with id
corpus = []
ids = []
for document in cursor:
    text = ' '.join(document["text"].encode("utf-8").split())
    corpus.append(text)
    ids.append(document["_id"])

# create sample by bootstrap sampling
random_indices = random.sample(range(0, len(corpus)), q.num_of_docs)

# write URLs and create tsv file for training
count = 0
print ("Creating a sample from the " + q.collection + " collection in the " + q.database +
       " database for the date " + q.date + "...")
urls.write("{ ")
f.write("ID\t TEXT\t HUMOR\t MISINFORMATION\t DOWNPLAY\t CONCERN\t GENERAL INFORMATION \n")

for index in random_indices:
    f.write(str(ids[index]) + "\t" + corpus[index] +
            "\t \t \t \t \t \n")
    # Extract URL
    tokens = corpus[index].split()
    for token in tokens:
        if "http" in token:
            tokens.remove(token)
            if count > 0:
                urls.write(", \n")
            # json.dump({str(document["_id"]): token}, urls)
            urls.write('"' + str(ids[index]) + '": "' + token + '"')
            count += 1

urls.write("}")