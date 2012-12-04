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

    def _tf_idf(self, tweets):
        df = defaultdict(int)
        index = 1

        for tweet in tweets:
            #print tweet
            tokens = re.findall("[\w']+", tweet['text'].lower())
            if tweet['user']['id'] in self.users:
                self.users[tweet['user']['id']]['tokens'] += tokens
            else:
                self.users[tweet['user']['id']] = {}
                self.users[tweet['user']['id']]['tokens'] = tokens
                self.users[tweet['user']['id']]['follower_count'] = tweet['user']['followers_count']
                self.users[tweet['user']['id']]['index'] = index
                self.users[tweet['user']['id']]['screen_name'] = tweet['user']['screen_name']
                index += 1

            for token in tokens:
                df[token]+=1.0

        self.term_idf = {
            term:math.log(len(self.users)/count,2)
            for term,count in df.iteritems()
        }

        for k, v in self.users.iteritems():
            self.users[k]['vect'] = self._normed_vect(v['tokens'])

    def _term_tf_idf(self, term, count):
        if count==0 or term not in self.term_idf:
            return 0
        return (1+math.log(count,2))*self.term_idf[term]

    def _normed_vect(self, tokens):
        counts = defaultdict(int)
        for token in tokens:
            counts[token]+=1

        vect = {
            term:self._term_tf_idf(term,count)
            for term,count in counts.iteritems()
        }
        mag = math.sqrt(sum(x**2 for x in vect.itervalues()))
        return {term:weight/mag for term,weight in vect.iteritems()}

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

    def split_train_eval(self, filtered):
        smallest_class_size = min(len(tw) for tw in filtered.itervalues())
        cutoff = 2*smallest_class_size//3
        train_group, eval_group = {}, {}

        for clas,tweets in filtered.iteritems():
            # make the positive and negative classes the same size by throwing away
            # tweets from the larger class.
            picked = random.sample(tweets,smallest_class_size)
            train_group[clas] = picked[:cutoff]
            eval_group[clas] = picked[cutoff:]

        return train_group, eval_group

    def knn(self, filtered, userid):
        #For the given userid, check the distance between their text vector and all the others
        #The text vector is located in tweet['userid']['vect']
        #Check the distance between the given id vector and all others and choose the 3 smallest ones
        #You can tell whether they are cool or not because they will be located in 'cool' or 'uncool'
        #I put a call to this in coolnesstest.py for you but you can look at it and change it if you want
        #The goal of this is to append a key to the current tweet that has key 'cool' and value
        #true or false
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
                self.users[userid]['closeuser'] = distances[key]['userid']
            if counter == 5:
                break
            if distances[key]['status'] == 'cool':
                counts['cool'] += 1.0
            else:
                counts['uncool'] += 1.0
            counter += 1

        if counts['cool'] > counts['uncool']:
            self.users[userid]['coolscore'] = 100*(counts['cool'] / (counts['cool'] + counts['uncool'])) 
            self.users[userid]['cool'] = 'yes'
            #print self.users[userid]['coolscore']
            return 'cool'
        else:
            self.users[userid]['coolscore'] = 100*(counts['cool'] / (counts['cool'] + counts['uncool']))
            #print self.users[userid]['coolscore']
            self.users[userid]['cool'] = 'no'
            return 'uncool'
