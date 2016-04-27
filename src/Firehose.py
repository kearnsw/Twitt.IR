import sys
import os
import twitter
import json
from datetime import datetime
from pymongo import MongoClient
from config import MONGO_AUTHENTICATION, MONGO_PASSWORD, MONGO_USERNAME
from config import OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_SECRET, CONSUMER_KEY


def oauth_login():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def save_to_mongo(data, database, collection):
    client = MongoClient()
    if MONGO_AUTHENTICATION:
            client.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
    db = client[database]
    coll = db[collection]
    return coll.insert_one(data)

# Checks whether the script was called from .sh or src
if os.path.basename(os.getcwd()) == "src":
    directory = os.path.dirname(os.getcwd())
else:
    directory = os.getcwd()

# Define configuration based off input from terminal
date = datetime.now().strftime('%Y-%m-%d')
query = sys.argv[1]     # Search terms should be separated by commas
outputFile = sys.argv[2] + date + ".json"
print date
if len(sys.argv) >= 4:
    db = sys.argv[3]
else:
    db = "Virus"

# Query Twitter Streaming API
print ("Searching Twitter stream for mentions of " + query + "...")
twitter_api = oauth_login()

twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=query)

data_location = directory + "/data"
f = open(data_location + "/" + outputFile, "w+")
# Write to DB and file
print ("Streaming data into " + db + " database" + "...")
f.write('[')
for tweet in stream:
    json.dump(tweet, f, indent=1)
    f.write(',\n')
    save_to_mongo(tweet, db, query)
    print tweet["text"]

f.close()
