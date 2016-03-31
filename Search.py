import twitter
import json


def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information
    # on Twitter's OAuth implementation.
    CONSUMER_KEY = 'X3MaTI14NpMnTyga8410PGCTm'
    CONSUMER_SECRET = 'YTHtm5MW7f2bC4idyzvIYZKlNJLnbiPVOrwlaw20i0BYuRrskv'
    OAUTH_TOKEN = '55862161-fURfClfU2L8HPE04lG4BDHfk1ERr3pTSXeQIgQ9MM'
    OAUTH_TOKEN_SECRET = 'YVsE20WflDEU19aYRlEWfvSQj1uwJkwO556Rvw2S9iHnk'
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api


def twitter_search(twitter_api, q, max_results=200, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
    # https://dev.twitter.com/docs/using-search for details on advanced
    # search criteria that may be useful for keyword arguments
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    for _ in range(10):  # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  # No more results when next_results doesn't exist
            break
            # Create a dictionary from next_results, which has the following form:
            # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=')
                       for kv in next_results[1:].split("&")])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses
# Sample usage
twitter_api = oauth_login()
q = "zika"
results = twitter_search(twitter_api, q, max_results=10)

# Show one sample search result by slicing the list...
f = open('/home/will/twitter/zika.json', "w")
print json.dump(results, f, indent=1)
f.close()
