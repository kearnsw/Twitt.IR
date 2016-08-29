import sys
import os
import json

directory = os.path.dirname(os.getcwd())
fn = sys.argv[1]
f = open(directory + "/data/" + fn, "r")
fo = open(directory + "/data/urls", "w+")
tweets = json.load(f)
for tweet in tweets:
    query = "https://www.google.com/maps/place/"
    if "location" in tweet["user"]:
        if tweet["user"]["location"]:
            location = tweet["user"]["location"].split()
            for i in range(len(location)):
                if i == 0:
                    query += location[i]
                else:
                    query += "+" + location[i]
            fo.write(query.encode("UTF-8") + "\n")

        """
        if "location" in document["user"]:
            if document["user"]["location"]:
                location = document["user"]["location"].split()
                for i in range(len(location)):
                    if i == 0:
                        query += location[i]
                    else:
                        query += "+" + location[i]
                urls.write(str(document["_id"]) + "\t" + query.encode("UTF-8") + "\n")
                """