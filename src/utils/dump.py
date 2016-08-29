# Import training data
client = MongoClient(MONGO_URI)
db = client.get_default_database()
cursor = db["submissions"].find({})