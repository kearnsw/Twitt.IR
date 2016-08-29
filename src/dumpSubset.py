from pymongo import MongoClient
from config import MONGO_URI
import sys

query = sys.argv[1]

f = open("../data/" + query + ".txt", "wb")

# Import training data
client = MongoClient(MONGO_URI)
db = client.get_default_database()
subset = 'data.' + query
cursor = db["submissions"].find({subset: 'true'})

i = 0
for document in cursor:
    f.write(document["tweet"]["text"].encode("utf-8") + " \n")
    i += 1

print i
