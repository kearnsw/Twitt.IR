import sys
import os
import twitter
import json
from datetime import datetime
from pymongo import MongoClient


def oauth_login():
    CONSUMER_KEY = 'X3MaTI14NpMnTyga8410PGCTm'
    CONSUMER_SECRET = 'YTHtm5MW7f2bC4idyzvIYZKlNJLnbiPVOrwlaw20i0BYuRrskv'
    OAUTH_TOKEN = '55862161-fURfClfU2L8HPE04lG4BDHfk1ERr3pTSXeQIgQ9MM'
    OAUTH_TOKEN_SECRET = 'YVsE20WflDEU19aYRlEWfvSQj1uwJkwO556Rvw2S9iHnk'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def save_to_mongo(data, database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return coll.insert(data)

# Define configuration based off input from terminal
time = datetime.now().strftime('%Y-%m-%d')
query = sys.argv[1]     # Search terms should be separated by commas
outFile = sys.argv[2].split(".")
outputFile = outFile[0] + time + "." + outFile[1]

print time
if len(sys.argv) >= 4:
    db = sys.argv[3]
else:
    db = "Virus"

data_location = os.getcwd() + "/data"
f = open(os.path.join(data_location, outputFile), 'w+')

print ("Searching Twitter stream for mentions of " + query + "...")
print ("Streaming data into " + db + " database" + "...")

twitter_api = oauth_login()
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

stream = twitter_stream.statuses.filter(track=query)

f.write('[')
for tweet in stream:
    json.dump(tweet, f, indent=1)
    f.write(',\n')
    print query
    save_to_mongo(tweet, db, query)

f.close()
