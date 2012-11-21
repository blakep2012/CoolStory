#!/usr/bin/env python
import requests
import os

# This reads tweets from Twitter's streaming API and writes them to a file.
# See Twitter's documentation here:
# https://dev.twitter.com/docs/api/1/post/statuses/filter
# You will need to change the SCREEN_NAME and PASSWORD below.
r = requests.post(
        'https://stream.twitter.com/1/statuses/filter.json',
        data={'locations': '-96.53,30.47, -96.15,30.79'},
        #data={'locations': '-96.33910,30.61865, -96.33844,30.61944'},
        auth=('BlakePavel', 's@bi@n1!')
        )

count = 0
output = open('tweets.%d.json'%os.getpid(),'w')

for line in r.iter_lines():
    if line: # filter out keep-alive new lines
        print>>output, line
        count +=1
        if count%100==0:
            print count
