from pymongo import MongoClient
import sys
import re

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
date = sys.argv[3]
sentences_seen = []
count = 0
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}


# Set search criteria
criteria = {"lang": "en", "created_at": {'$regex': date},
            "text": {"$not": re.compile("RT")}}
cursor = coll.find(criteria, {"text": 1}).limit(1000)

month_day = date.split()
month = month_day[0]
day = month_day[1]
fn = "sample_" + str(months[month]) + "_" + str(day) + ".tsv"
f = open(fn, "w+")


# Write sample to file
print ("Creating a sample from the " + arg2 + " collection in the " + arg1 + " database for the date " + date + "...")
f.write("ID\t TEXT\t HUMOR\t MISINFORMATION\t DOWNPLAY\t CONCERN\t GENERAL INFORMATION \n")
for document in cursor:
    text = ' '.join(document["text"].encode("utf-8").split())
    tokens = text.split()

    for token in tokens:
        if "htt" in token:
            tokens.remove(token)
    parsed = " ".join(tokens)

    if count >= 100:
        break
    if parsed not in sentences_seen:
        sentences_seen.append(parsed)
        f.write(str(document["_id"]) + "\t" + text.replace("\t", " ").replace("\n", " ") +
                "\t \t \t \t \t \n")
        count += 1

