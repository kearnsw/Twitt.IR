from pymongo import MongoClient
from config import MONGO_URI
import sys

# Import training data
client = MongoClient(MONGO_URI)
db = client.get_default_database()
cursor = db["submissions"].find({"username": "kearnsw"})

user1 = []
for document in cursor:
    user1.append(document)

user2 = []
cursor = db["submissions"].find({"username": "enguyen"})
for document in cursor:
    user2.append(document)

humor_agreement = 0
mistrust_agreement = 0
concern_agreement = 0
relief_agreement = 0
user1_humor = 0
user1_mistrust = 0
user1_concern = 0
user1_relief = 0

user2_humor = 0
user2_mistrust = 0
user2_concern = 0
user2_relief = 0

for i in range(len(user1)):
    if user1[i]["data"]["humor"] == "true":
        user1_humor += 1
    if user1[i]["data"]["concern"] == "true":
        user1_concern += 1
    if user1[i]["data"]["mistrust"] == "true":
        user1_mistrust += 1
    if user1[i]["data"]["relief"] == "true":
        user1_relief += 1

    for j in range(len(user2)):
        if user2[j]["tweet"]["id"] == user1[i]["tweet"]["id"]:
            # Count overall trues
            if user2[j]["data"]["humor"] == "true":
                user2_humor += 1
            if user2[j]["data"]["concern"] == "true":
                user2_concern += 1
            if user2[j]["data"]["mistrust"] == "true":
                user2_mistrust += 1
            if user2[j]["data"]["relief"] == "true":
                user2_relief += 1

            # Check user agreement
            if user2[j]["data"]["humor"] == user1[i]["data"]["humor"]:
                humor_agreement += 1
            else:
                print "Humor Disagreement"
                print user1[i]["tweet"]["text"]
                print user1[i]["data"]["humor"]
                print user2[j]["data"]["humor"]
                print "\n"

            if user2[j]["data"]["mistrust"] == user1[i]["data"]["mistrust"]:
                mistrust_agreement += 1
            else:
                print "Mistrust Disagreement"
                print user1[i]["tweet"]["text"]
                print user1[i]["data"]["mistrust"]
                print user2[j]["data"]["mistrust"]
                print "\n"

            if user2[j]["data"]["concern"] == user1[i]["data"]["concern"]:
                concern_agreement += 1
            else:
                print "Concern Disagreement"
                print user1[i]["tweet"]["text"]
                print user1[i]["data"]["concern"]
                print user2[j]["data"]["concern"]
                print "\n"

            if user2[j]["data"]["relief"] == user1[i]["data"]["relief"]:
                relief_agreement += 1
            else:
                print "Relief Disagreement"
                print user1[i]["tweet"]["text"]
                print user1[i]["data"]["relief"]
                print user2[j]["data"]["relief"]
                print "\n"

print len(user1)
print("Agreement")
print("===================")
print humor_agreement
print mistrust_agreement
print concern_agreement
print relief_agreement

print("User 1")
print("===================")
print user1_humor
print user1_mistrust
print user1_concern
print user1_relief

print("User 2")
print("===================")
print user2_humor
print user2_mistrust
print user2_concern
print user2_relief

total = len(user1)
p0 = float(humor_agreement)/total
random_yes_user1 = float(user1_humor)/(total - user1_humor)
random_yes_user2 = float(user2_humor)/(total - user2_humor)
random_no_user1 = 1 - random_yes_user1
random_no_user2 = 1 - random_yes_user2
random_yes = random_yes_user1 * random_yes_user2
random_no = random_no_user1 * random_no_user2
pe = random_yes + random_no
humor_cohens = float(p0 - pe)/(1-pe)

p0 = float(mistrust_agreement)/total
random_yes_user1 = float(user1_mistrust)/(total - user1_mistrust)
random_yes_user2 = float(user2_mistrust)/(total - user2_mistrust)
random_no_user1 = 1 - random_yes_user1
random_no_user2 = 1 - random_yes_user2
random_yes = random_yes_user1 * random_yes_user2
random_no = random_no_user1 * random_no_user2
pe = random_yes + random_no
mistrust_cohens = float(p0 - pe)/(1-pe)

p0 = float(concern_agreement)/total
random_yes_user1 = float(user1_concern)/(total - user1_concern)
random_yes_user2 = float(user2_concern)/(total - user2_concern)
random_no_user1 = 1 - random_yes_user1
random_no_user2 = 1 - random_yes_user2
random_yes = random_yes_user1 * random_yes_user2
random_no = random_no_user1 * random_no_user2
pe = random_yes + random_no
concern_cohens = float(p0 - pe)/(1-pe)

p0 = float(relief_agreement)/total
random_yes_user1 = float(user1_relief)/(total - user1_relief)
random_yes_user2 = float(user2_relief)/(total - user2_relief)
random_no_user1 = 1 - random_yes_user1
random_no_user2 = 1 - random_yes_user2
random_yes = random_yes_user1 * random_yes_user2
random_no = random_no_user1 * random_no_user2
pe = random_yes + random_no
relief_cohens = float(p0 - pe)/(1-pe)

print ("Cohens")
print("===================")
print humor_cohens
print mistrust_cohens
print concern_cohens
print relief_cohens

