# Much of this code is adopted from Matthew A. Russell book Mining the Social
# Web, 2nd Edition
import sys
import os
import twitter
import json
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


def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    # Connects to the MongoDB server running on
    # localhost:27017 by default
    client = MongoClient(**mongo_conn_kw)
    # Get a reference to a particular database
    db = client[mongo_db]
    # Reference a particular collection in the database
    coll = db[mongo_db_coll]
    # Perform a bulk insert and return the IDs
    return coll.insert(data)


def load_from_mongo(mongo_db, mongo_db_coll, return_cursor=False,
                    criteria=None, projection=None, **mongo_conn_kw):
    # Optionally, use criteria and projection to limit the data that is
    # returned as documented in
    # http://docs.mongodb.org/manual/reference/method/db.collection.find/
    # Consider leveraging MongoDB's aggregations framework for more
    # sophisticated queries.
    client = MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]

    if criteria is None:
        criteria = {}
    if projection is None:
        cursor = coll.find(criteria)
    else:
        cursor = coll.find(criteria, projection)

    # Returning a cursor is recommended for large amounts of data
    if return_cursor:
        return cursor
    else:
        return [item for item in cursor]

disease = sys.argv[1]
outputFile = sys.argv[2]

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, outputFile), 'w+')

query = disease  # Comma-separated list of search terms
print >> sys.stderr, 'Filtering the public timeline for track="%s"' % (query,)

twitter_api = oauth_login()
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

stream = twitter_stream.statuses.filter(track=query)

f.write('[')
for tweet in stream:
    json.dump(tweet, f, indent=1)
    f.write(',\n')
    save_to_mongo(tweet, 'Virus', disease)

f.close()
