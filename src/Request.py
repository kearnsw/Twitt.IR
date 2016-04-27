from pymongo import MongoClient
import sys
from config import MONGO_AUTHENTICATION, MONGO_PASSWORD, MONGO_USERNAME

class Request:

    def __init__(self):

        if len(sys.argv) >= 2:
            self.database = sys.argv[1]
        else:
            self.database = "Virus"

        if len(sys.argv) >= 3:
            self.collection = sys.argv[2]
        else:
            self.collection = "Zika"

        if len(sys.argv) >= 5:
            self.num_of_docs = sys.argv[4]
        else:
            self.num_of_docs = 100

        if len(sys.argv) >= 4:
            self.date = sys.argv[3]
        else:
            self.date = "Mar 31"

    def connect(self):
        # Open connection to client
        client = MongoClient()
        if MONGO_AUTHENTICATION:
            client.admin.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
        db = client[self.database]
        self.collection = db[self.collection]

    def search(self, query, *args):
        if args:
            return self.collection.find(query, args[0])
        else:
            return self.collection.find(query)

    def aggregate(self, query):
        return self.collection.aggregate(query)

    def count(self, query):
        return self.collection.find(query).count()
