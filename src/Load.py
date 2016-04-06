from pymongo import MongoClient
import json
import sys

if len(sys.argv) >= 2:
    arg1 = sys.argv[1]
else:
    arg1 = "Virus"

if len(sys.argv) >= 3:
    arg2 = sys.argv[2]
else:
    arg2 = "Zika"

client = MongoClient()
db = client[arg1]
coll = db[arg2]

criteria = {"lang": "en"}

cursor = coll.find(criteria)
for document in cursor:
    print (document["text"])
