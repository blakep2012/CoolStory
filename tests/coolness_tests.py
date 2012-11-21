import unittest
import math
import coolness

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

class TestCoolness(unittest.TestCase):

    def test_training(self):
        analyzer = coolness.CoolAnalyzer()
        analyzer._tf_idf(COOL_TWEETS)
        self.assertAlmostEqual(analyzer.users[1]['vect']['caverlee'], 0.48904356602098176)
        self.assertAlmostEqual(analyzer.users[2]['vect']['howdy'], 0.34052169288272116)
        self.assertAlmostEqual(analyzer.users[3]['vect']['sucks'], 0.500748258078816)
        self.assertAlmostEqual(analyzer.users[4]['vect']['texas'], 0.26679960741127956)
        self.assertAlmostEqual(analyzer.users[5]['vect']['texas'], 0.2606324134265765)

    def test_cool(self):
        analyzer = coolness.CoolAnalyzer()
        analyzer._tf_idf(COOL_TWEETS)
        flwravg = analyzer.find_cool_line(COOL_TWEETS)
        filtered = analyzer.filter_classes(COOL_TWEETS,flwravg)
        #analyzer.split_train_eval(filtered)
        self.assertEqual(analyzer.knn(filtered, 3), 'uncool')
        self.assertEqual(analyzer.knn(filtered, 4), 'uncool')
        self.assertEqual(analyzer.knn(filtered, 5), 'uncool')
        self.assertEqual(analyzer.knn(filtered, 8), 'cool')

if __name__ == '__main__':
    unittest.main()
