import json
import cherrypy
import cherrypy_cors
import datetime
from dateutil.parser import parse
from jinja2 import Environment, FileSystemLoader
from pymongo import MongoClient
import pymongo


class server:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('../'))
        cherrypy_cors.install()

    @cherrypy.expose
    def index(self, data=None):
        view = self.env.get_template('app/index.html')
        return view.render(title="Contextualization Interface")

    @cherrypy.expose
    def getTweets(self, date, concept):
        # Parse date information for Mongo Query
        parsedDate = parse(date)
        year = parsedDate.year
        month = parsedDate.month
        day = parsedDate.day

        # Handle Mongo Query
        client = MongoClient()
        db = client.Twitter
        cursor = db.Zika.find({"lang": "en", concept: "true", "created_at": {"$gte": datetime.datetime(year, month, day),
                                                                             "$lt": datetime.datetime(year, month, day + 1)}}).limit(1)

        tweets = []
        for document in cursor:
            tweets.append(document["text"])

        if len(tweets) == 0:
            tweets = ["No tweets for this date"]

        return tweets[0]

    @cherrypy.expose
    def getCount(self, date, concept):
        # Parse date information for Mongo Query
        parsedDate = parse(date)
        year = parsedDate.year
        month = parsedDate.month
        day = parsedDate.day
        print concept
        print date

        # Handle Mongo Query
        client = MongoClient()
        db = client.Twitter

        if concept == "total":
            count = db.Zika.count({"lang": "en", "created_at": {"$gte": datetime.datetime(year, month, day),
                                                                "$lt": datetime.datetime(year, month, day + 1)}})
        else:
            count = db.Zika.count({"lang": "en", concept: "true", "created_at": {"$gte": datetime.datetime(year, month, day),
                                                                                 "$lt": datetime.datetime(year, month, day + 1)}})

        return str(count)




cherrypy.quickstart(server(), "", "server.cfg")
