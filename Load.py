from pymongo import MongoClient
import json

client = MongoClient()
db = client["Virus"]
coll = db["Zika"]

criteria = {"lang": "en", "retweeted_status.retweet_count": {"$gt": 1000}}

cursor = coll.find(criteria)
for document in cursor:
    print (document["text"])
