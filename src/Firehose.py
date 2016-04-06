import sys
import os
import twitter
import json
from datetime import datetime
from pymongo import MongoClient


def oauth_login(directory):
    fc = open(os.path.join(directory, "config"), 'r')
    configuration = fc.read()
    configuration = configuration.split()

    CONSUMER_KEY = configuration[2]
    CONSUMER_SECRET = configuration[5]
    OAUTH_TOKEN = configuration[8]
    OAUTH_TOKEN_SECRET = configuration[11]
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def save_to_mongo(data, database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return coll.insert(data)

# Checks whether the script was called from .sh or src
if os.path.basename(os.getcwd()) == "src":
    directory = os.path.dirname(os.getcwd())
else:
    directory = os.getcwd()

# Define configuration based off input from terminal
date = datetime.now().strftime('%Y-%m-%d')
query = sys.argv[1]     # Search terms should be separated by commas
outFile = sys.argv[2].split(".")
outputFile = outFile[0] + date + "." + outFile[1]
print date
if len(sys.argv) >= 4:
    db = sys.argv[3]
else:
    db = "Virus"

# Query Twitter Streaming API
print ("Searching Twitter stream for mentions of " + query + "...")
twitter_api = oauth_login(directory)

twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=query)

data_location = directory + "/data"

# Write to DB and file
print ("Streaming data into " + db + " database" + "...")
f.write('[')
for tweet in stream:
    json.dump(tweet, f, indent=1)
    f.write(',\n')
    save_to_mongo(tweet, db, query)

f.close()
