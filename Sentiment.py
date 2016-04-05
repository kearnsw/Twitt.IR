from pymongo import MongoClient
from vaderSentiment.vaderSentiment import sentiment as vs
import os

# File for writing sentiment for storage and analysis
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
outputFile = "sentiment.json"
f = open(os.path.join(__location__, outputFile), 'w+')

# Open mongodb client, access the database collection, and find documents
# based on criteria
client = MongoClient()
db = client["Virus"]
coll = db["Zika"]
criteria = {"lang": "en"}
cursor = coll.find(criteria)

# Dictionary of months for date conversion and empty array for documents
months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5,
          "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
          "Nov": 11, "Dec": 12}
docs = []

for document in cursor:
    # Convert time from Tue Mar 29 04:04:22 +0000 2016 to 2016-3-29
    time = document["created_at"].split()
    month = months[time[1]]
    day = time[2]
    year = time[5]
    date = str(year) + "-" + str(month) + "-" + str(day)

    docs.append({"text": document["text"],
                 "date": '"' + date + '"'})

aggregate = {}
count = {}

for doc in docs:
    text = doc["text"].encode('utf-8')
    sentiment = vs(text)
    value = (sentiment['neg'] * -1) + (sentiment['pos'])
    if doc["date"] not in aggregate:
        aggregate[doc["date"]] = value
        count[doc["date"]] = 1
    else:
        aggregate[doc["date"]] += value
        count[doc["date"]] += 1

# normalize
f.write("[ \n")
for date in aggregate:
    aggregate[date] = aggregate[date]/count[date]

    f.write('{ \t "date": ' + str(date) +
            ',\n \t "value": ' + str(aggregate[date]) + "\n }")
    f.write(", \n")

f.close()