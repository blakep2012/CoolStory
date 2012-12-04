from flask import Flask, render_template, flash, request
from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
import coolness

app = Flask(__name__)

COOL_TWEETS = [
    dict(
        text="Caverlee is a pretty slick dude.",
        user=dict(
                id=1,
                follower_count=100,
                screen_name='Avid'
        )
    ),
    dict(
        text="Howdy! Computer Science is really awesome even though I am bad at it.",
        user=dict(
                id=2,
                follower_count=80,
                screen_name='Blake'
        )
    ),
    dict(
        text="Everybody really sucks because I am the best.",
        user=dict(
                id=3,
                follower_count=40,
                screen_name='Frank'
        )
    ),
    dict(
        text="This just in, Agriculture is the best major at Texas A&M.",
        user=dict(
                id=4,
                follower_count=20,
                screen_name='Billy'
        )
    ),
    dict(
        text="I feel sorry for Texas A&M because I'm a butthurt sip",
        user=dict(
                id=5,
                follower_count=5,
                screen_name='McCoy'
        )
    ),
    dict(
        text="A&M OVER BAMA #ROLLTEARSROLL",
        user=dict(
                id=6,
                follower_count=91,
                screen_name='redassAg2012'
        )
    ),
    dict(
        text="I don't think that Computer Science is as marketable as people think...it's not that important",
        user=dict(
                id=7,
                follower_count=18,
                screen_name='businessMajorDude'
        )
    ),
    dict(
        text="#johnnyheisman",
        user=dict(
                id=8,
                follower_count=78,
                screen_name='aggie2014'
        )
    ),
    dict(
        text="I love CHI; the work load is very reasonable for 3 hours",
        user=dict(
                id=9,
                follower_count=15,
                screen_name='saidNoOneEver'
        )
    ),
    dict(
        text="Blake and Avid are the best",
        user=dict(
                id=10,
                follower_count=120,
                screen_name='theRealCaverlee'
        )
    )
]

analyzer = coolness.CoolAnalyzer()
analyzer._tf_idf(COOL_TWEETS)
flwravg = analyzer.find_cool_line(COOL_TWEETS)
analyzer.filter_classes(COOL_TWEETS,flwravg)

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/my-link/')
def my_link():
    print 'I got clicked!'
    print analyzer.filtered
    
    return analyzer.knn(analyzer.filtered, 10)
    
@app.route('/rateUser', methods=['POST'])
def rate_user():
    user = request.form['user']
    
    for status, tweets in analyzer.filtered.iteritems():
        for tweet in tweets:
            if user == tweet['user']['screen_name']:
                userId = tweet['user']['id']
                return analyzer.knn(analyzer.filtered, userId)
                
    return 'User Not Found'

if __name__ == '__main__':
    app.run(debug=True)
