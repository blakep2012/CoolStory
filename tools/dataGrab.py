import ujson
import fileinput

def read_tweets():
    for line in fileinput.input():
        yield ujson.loads(line)

tweets = read_tweets()
f = open('./tweetsCounts.txt', 'w+')

for tweet in tweets:
    if 'user' not in tweet:
        continue
    print >> f, tweet['user']['followers_count']
    

