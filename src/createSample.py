from pymongo import MongoClient
import sys
import re
import nltk

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
date = 'Mar 31'
sentences_seen = []

criteria = {"lang": "en", "created_at": {'$regex': date},
            "text": {"$not": re.compile("RT")}}
f = open("sample.tsv", "w+")

f.write("ID\t TEXT\t HUMOR\t MISINFORMATION\t DOWNPLAY\t CONCERN\t GENERAL INFORMATION \n")
cursor = coll.find(criteria, {"text": 1}).limit(1000)
for document in cursor:
    text = ' '.join(document["text"].encode("utf-8").split())
    tokens = text.split()

    for token in tokens:
        if "htt" in token:
            tokens.remove(token)
    parsed = " ".join(tokens)

    if parsed not in sentences_seen:
        sentences_seen.append(parsed)
        f.write(str(document["_id"]) + "\t" + text.replace("\t", " ").replace("\n", " ") +
                "\t \t \t \t \t \n")

