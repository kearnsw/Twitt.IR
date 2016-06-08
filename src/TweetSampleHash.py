import sys
import path
import os
import json

directory = os.path.dirname(os.getcwd())
fn = sys.argv[1]
f = open(directory + "/data/" + fn, "r")
tweets = json.load(f)

for tweet in tweets:
        print str(tweet["id"])
