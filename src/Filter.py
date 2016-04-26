import alignment
import thread

class Filter:

    def __init__(self, threshold):
        self.stopwords = ['Zika', 'the', 'and', 'or']
        self.threshold = threshold
        self.match_len = 0

    def check_duplicates(self, tweet1, tweet2):
        tweet1 = tweet1.lower().split()
        tweet2 = tweet2.lower().split()
        self.match_len = alignment.water(tweet1, tweet2)
        if self.match_len >= self.threshold:
            return True
        else:
            return False
