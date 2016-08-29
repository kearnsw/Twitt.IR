import sys
import path
import os
import json
from pymongo import MongoClient

mongolab_uri = "mongodb://kearnsw:I2wbw4aml!@ds013192.mlab.com:13192/heroku_d5z084rp"

# Connect to Mongo
client = MongoClient(mongolab_uri)
db = client.get_default_database()

# Open file to store the data
directory = os.path.dirname(os.getcwd())
fn = "method_2_data.json"
f = open(directory + "/data/" + fn, "w")

#Create a list of objects that coincide with Annotweet data
tweet = dict()
tweet["data"] = dict()
data_cursor = db.data.find()

f.write("[")
for document in data_cursor:
    tweet["data"]["humor"] = document["humor"]
    tweet["data"]["mistrust"] = document["mistrust"]
    tweet["data"]["relief"] = document["relief"]
    tweet["data"]["concern"] = document["concern"]

    sample_cursor = db.samples.find({"id": document["id"]})
    for doc in sample_cursor:
        tweet["tweet"] = doc
        tweet["username"] = "enguyen"
    json.dump(tweet, f)
    f.write(",\n")
f.write("]")
