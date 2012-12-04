from flask import Flask, render_template, flash, request
from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
import coolness
import ujson
import fileinput

app = Flask(__name__)

def read_tweets():
    count = 0
    for line in fileinput.input():
        if count == 1000:
            break 
        count += 1
        yield ujson.loads(line)

def setup():
    tweetIt = read_tweets()
    COOL_TWEETS = []
    for tweet in tweetIt:
        COOL_TWEETS.append(tweet)

    analyzer._tf_idf(COOL_TWEETS)
    flwravg = analyzer.find_cool_line(COOL_TWEETS)
    analyzer.filter_classes(COOL_TWEETS,flwravg)

    for userId in analyzer.users:
        #print userId
        analyzer.knn(analyzer.filtered, userId)
        
analyzer = coolness.CoolAnalyzer()

setup()

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/my-link/')
def my_link():
    print 'I got clicked!'
    
    return analyzer.knn(analyzer.filtered, 10)
    
@app.route('/rateUser', methods=['POST'])
def rate_user():
    user = request.form['user']
    
    for status, tweets in analyzer.filtered.iteritems():
        for tweet in tweets:
            if user == tweet['user']['screen_name']:
                userId = tweet['user']['id']
                #analyzer.knn(analyzer.filtered, userId)
                
                result = []
                num = analyzer.users[userId]['coolscore']
                num = str(num)
                result.append(num)
                status = analyzer.users[userId]['cool']
                result.append(status)
                closestUser = '@'
                closestUser += analyzer.users[analyzer.users[userId]['closeuser']]['screen_name']
                result.append(closestUser)
                
                return ' '.join(result)
                
    return 'User Not Found'

if __name__ == '__main__':
    app.run(debug=False)
