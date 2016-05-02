from __future__ import print_function
import os
import re
import json
from bson import ObjectId
from Filter import Filter
from Request import Request


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

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
cursor = q.search(criteria).limit(1000)

# Open file I/O streams
directory = os.path.dirname(os.getcwd())
fn = "sample_" + str(months[month]) + "_" + str(day) + ".json"
f = open(directory + "/data/" + fn, "w+")

# load tweet with id
corpus = [{"text": "dummy"}]
tweetFilter = Filter(25)
i = 0
for document in cursor:
    document["_id"] = str(document["_id"])
    document["text"] = document["text"].replace('"', "'")
    for tweet in corpus:
        # If return a match then append to unique tweets
        status = tweetFilter.check_duplicates(document["text"], tweet["text"])
        if status:
            break
    if not status:
        corpus.append(document)
    i += 1
    if i > 100:
        break
    print(i)


# Remove header
corpus.pop(0)
json.dump(corpus, f)
