# Access the Instaparser API and return the body text of URLs
# Input: file of URLs separated by "\n"
# Output: file containing a dictionary of URLs with their body text

import requests
import time
import os
import sys
import json
from datetime import datetime


class Response:
    def __init__(self):
        self.status_code = 200
        self.url = "http://pandas.cc"
        self.text = {
            "site_name": "thejewishstar.com",
            "description": "Since Israel was founded in 1948, its numerous wars have taken a heavy toll on its small population. With mandatory conscription, most Israelis have lost someone on the battlefield \u2014 a relative, friend, community member, or someone they know more indirectly \u2014 and each sacrifice is highly personal. Last year has been even more taxing than usual, given the summer\u2019s war with Hamas in Gaza. During the Israel Defense Forces\u2019 Operation Protective Edge, 66 IDF soldiers were killed. The sobering cost of Israel\u2019s military reality is reflected annually on the Hebrew calendar date of the fourth of Iyar, which marks Yom Hazikaron (Israel Memorial Day). Established unofficially in 1948 and then officially in 1963, it is commemorated in conjunction with Yom Ha\u2019atzmaut (Israel Independence Day), which falls on the following day. This year, Yom Hazikaron and Yom Ha\u2019atzmaut come April 22\u201323. \u201cWe didn\u2019t think it would be easy when we decided to reclaim our right to national self-determination after 2,000 years,\u201d Paul Hirschson, an Israeli Foreign Ministry spokesman, told JNS.org. \u201cSince the establishment of Israel we have been forced to defend ourselves on too many an occasion,\u201d he said. \u201cSome of the finest of our children, friends, and colleagues had to pay with their lives to secure that elementary right to national self-determination. We grieve their loss deeply yet remain, always, resilient with a view to the future: building, innovating, creating, and confident that we will one day live in both peace and security.\u201d Using information compiled by the Foreign",
            "videos": [],
            "images": [
                "http://www.thejewishstar.com/images/js-nameplate.gif",
                "http://liherald.ads.communityq.com/www/delivery/avw.php?zoneid=206&cb=INSERT_RANDOM_NUMBER_HERE&n=a4480c92",
                "http://image.weather.com/web/common/wxicons/31/31.gif?12122006",
                "http://www.thejewishstar.com/images/thumbs/star.jpg",
                "http://liherald.ads.communityq.com/www/delivery/avw.php?zoneid=141&cb=INSERT_RANDOM_NUMBER_HERE&n=a4480c92",
                "http://liherald.ads.communityq.com/www/delivery/avw.php?zoneid=142&cb=INSERT_RANDOM_NUMBER_HERE&n=a4480c92"
            ],
            "words": 317,
            "date": "null",
            "title": "Gaza war adds new gravity to Yom Hazikaron",
            "url": "http://www.thejewishstar.com/stories/Gaza-war-adds-new-gravity-to-Yom-Hazikaron,5942",
            "is_rtl": "false",
            "author": "null",
            "html": "<div>\n\t<p>Since Israel was founded in 1948, its numerous wars have taken a heavy toll on its small population. With mandatory conscription, most Israelis have lost <em>someone</em> on the battlefield \u2014 a relative, friend, community member, or someone they know more indirectly \u2014 and each sacrifice is highly personal.</p>\n<p>Last year has been even more taxing than usual, given the summer\u2019s war with Hamas in Gaza. During the Israel Defense Forces\u2019 Operation Protective Edge, 66 IDF soldiers were killed.</p>\n<p>The sobering cost of Israel\u2019s military reality is reflected annually on the Hebrew calendar date of the fourth of Iyar, which marks Yom Hazikaron (Israel Memorial Day). Established unofficially in 1948 and then officially in 1963, it is commemorated in conjunction with Yom Ha\u2019atzmaut (Israel Independence Day), which falls on the following day. This year, Yom Hazikaron and Yom Ha\u2019atzmaut come April 22\u201323.</p>\n<p>\u201cWe didn\u2019t think it would be easy when we decided to reclaim our right to national self-determination after 2,000 years,\u201d Paul Hirschson, an Israeli Foreign Ministry spokesman, told JNS.org.</p>\n<p>\u201cSince the establishment of Israel we have been forced to defend ourselves on too many an occasion,\u201d he said. \u201cSome of the finest of our children, friends, and colleagues had to pay with their lives to secure that elementary right to national self-determination. We grieve their loss deeply yet remain, always, resilient with a view to the future: building, innovating, creating, and confident that we will one day live in both peace and security.\u201d</p>\n<p>Using information compiled by the Foreign Ministry, JNS.org remembers the Israeli soldiers who lost their lives in Operation Protective Edge and in other incidents since last Yom Hazikaron.</p>\n<p><strong>GAZA</strong></p>\n<p><span><strong>July 18, 2014: </strong></span>Just a day after Israel began its ground operation to dismantle Hamas\u2019s terror tunnels, the IDF experienced its first casualty of Operation Protective Edge\u2014Staff Sgt. Eitan Barak, 20, of Herzliya, who was killed in Beit Hannun in the northern Gaza Strip.</p>\n<p>\n\t</p></div>\n\n\t\n\t",
            "thumbnail": "http://jewishstar.static2.adqic.com/uploads/original/1429301694_0514.jpg"
        }


class InstaparserRequest:
    def __init__(self, api_key):
        self.API = 'https://www.instaparser.com/api/1/article'
        self.API_KEY = api_key
        self.URL = 'http://www.kearnsw.com'
        self.response = dict()

    def get_parameters(self):
        return {'api_key': self.API_KEY, 'url': self.URL}

    def set_url(self, new_url):
        self.URL = new_url
        return self.URL

    def get_request(self):
        return requests.get(self.API, self.get_parameters())

directory = os.path.dirname(os.getcwd())
fc = open(os.path.join(directory, "config"), 'r')
configuration = fc.read()
configuration = configuration.split()
API_KEY = configuration[14]

if len(sys.argv) >= 2:
    f_in = open(sys.argv[1], 'r')
else:
    f_in = open(directory + '/data/urls.json', 'r')

if len(sys.argv) >= 3:
    f_out = open(sys.argv[2], 'w+')
else:
    date = datetime.now().strftime('%m-%d-%H-%M')
    filename = "parsed" + date + ".json"
    f_out = open(directory + '/data/' + filename, 'w+')

f_out.write("[ ")
request = InstaparserRequest(API_KEY)
count = 1

urls = json.load(f_in)
for _id, url in urls.items():
    print "Parsing url #" + str(count) + "..."
    print _id
    request.set_url(url)
    response = request.get_request()
    if response.status_code == 200:
        if count != 1:
            f_out.write(", \n")
        f_out.write("{\"" + str(_id) + "\": ")
        body = json.loads(response.text)
        json.dump(body, f_out, indent=1)
        f_out.write("}")
    count += 1
    time.sleep(2)
f_out.write("]")
