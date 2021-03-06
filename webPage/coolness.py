from collections import Counter, defaultdict
import math
import operator
import heapq
import random
import time
import re
from stemming import porter2
from itertools import chain


class CoolAnalyzer(object):
    def __init__(self):
        self.users = {}
        self.term_idf = {}
        self.filtered = {}
        self.df = defaultdict(int)
        
    def _term_tf_idf(self, term, count):
        if count==0 or term not in self.term_idf:
            return 0
        return (1+math.log(count,2))*self.term_idf[term]

    def _normed_vect(self, tokens):
        #print tokens
        counts = defaultdict(int)
        for token in tokens:
            counts[token]+=1

        vect = {
            term:self._term_tf_idf(term,count)
            for term,count in counts.iteritems()
        }
        mag = math.sqrt(sum(x**2 for x in vect.itervalues()))
        return {term:weight/mag for term,weight in vect.iteritems()}

    def _tf_idf(self, tweets):
        index = 1
        for tweet in tweets:
            #print tweet
            tokens = re.findall("[\w']+", tweet['text'].lower())
            userid = tweet['user']['id']
            if userid in self.users:
                self.users[userid]['tokens'] = []
                for token in tokens:
                    if len(token) > 3:
                        self.users[userid]['tokens'].append(token)
                #print self.users[userid]['tokens']
            else:
                self.users[userid] = {}
                self.users[userid]['tokens'] = []
                for token in tokens:
                    if len(token) > 3:
                        self.users[userid]['tokens'].append(token)
                #print self.users[userid]['tokens']
                self.users[userid]['follower_count'] = tweet['user']['followers_count']
                self.users[userid]['index'] = index
                self.users[userid]['screen_name'] = tweet['user']['screen_name']
                index += 1
            


            for token in tokens:
                self.df[token]+=1.0
        
        #print "BEFORE"
        self.term_idf = {
            term:math.log(len(self.users)/count,2)
            for term,count in self.df.iteritems()
        }
        #print "AFTER"
        for k, v in self.users.iteritems():
            self.users[k]['vect'] = self._normed_vect(v['tokens'])
        
        #print self.users[-1]
        #print "# of users is: ", len(self.users)
        #print self.users[280825871]['vect']

    def find_cool_line(self, tweets):
        followercountavg = 0.0
        count = 0.0

        for tweet in tweets:
            followercountavg += tweet['user']['followers_count']
            count += 1.0

        followercountavg /= count

        return followercountavg

    def filter_classes(self,tweets, avg):
        self.filtered = {'cool': [], 'uncool': []}
        for tweet in tweets:
            if tweet['user']['followers_count'] >= avg:
                self.filtered['cool'].append(tweet)
            else:
                self.filtered['uncool'].append(tweet)
        return self.filtered

    def knn(self, filtered, userid):
        distances = {}
        counts = {'cool':0, 'uncool':0}

        userVect = self.users[userid]['vect']

        for status, tweets in filtered.iteritems():
            diffs = []
            seen = []
            for tweet in tweets:
                if tweet['user']['id'] == userid:
                    continue
                curId = tweet['user']['id']
                curVect = self.users[curId]['vect']
                for elem in userVect:
                    seen.append(elem)
                    if elem not in curVect:
                        diff = userVect[elem] * userVect[elem]
                        diffs.append(diff)
                        continue
                    diff = userVect[elem] - curVect[elem]
                    sq = diff * diff
                    diffs.append(sq)
                for elem in curVect:
                    seen.append(elem)
                    if elem not in seen:
                        diff = curVect[elem] * curVect[elem]
                        diffs.append(diff)

                sums = sum(diffs)
                sqrt = math.sqrt(sums)
                distances[sqrt] = {'status': status, 'userid': curId}

        counter = 0
        for key in sorted(distances.iterkeys()):
            if counter == 0:
                self.users[userid]['closeuser'] = self.users[distances[key]['userid']]['screen_name']
            if counter == 20:
                break
            if distances[key]['status'] == 'cool':
                counts['cool'] += 1.0
                #print distances[key]['userid']
                #print key
            else:
                counts['uncool'] += 1.0
                #print distances[key]['userid']
                #print key
            counter += 1

        self.users[userid]['coolscore'] = 100*(counts['cool'] / (counts['cool'] + counts['uncool']))
        #print "all keys have been printed"

        if self.users[userid]['coolscore'] >= 50.0:
            #print counts['cool']
            #print counts['uncool']
            self.users[userid]['cool'] = 'yes'
            return 'cool'
        else:
            #print counts['cool']
            #print counts['uncool']
            self.users[userid]['cool'] = 'no'
            return 'uncool'
