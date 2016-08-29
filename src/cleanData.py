
def clean(tweet):
    # Remove @RT and @usernames
    for word in tweet:
        if "@" in word:
            tweet = tweet.replace(word, " ")

