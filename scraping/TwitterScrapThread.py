import json
import threading

from tweepy import Cursor


class ScrapThread(threading.Thread):
    def __init__(self, api, media_name, counter, callbackFunc):
        threading.Thread.__init__(self, daemon=True)
        self.api = api
        self.media_name = media_name
        self.counter = counter
        self.callback = callbackFunc

    def run(self):
        tweets = []
        for tweet in Cursor(self.api.user_timeline, id=self.media_name, since=(25 * self.counter)).items(25):
            jstr = json.dumps(tweet._json)
            obj = json.loads(jstr)
            tweets.append(obj)
        self.callback(tweets)


class StreamThread(threading.Thread):
    def __init__(self, stream, callbackFunc):
        threading.Thread.__init__(self, daemon=True)
        self.stream = stream
        self.callback = callbackFunc

    def run(self):
        self.stream.filter(follow=["7996082"])
        #self.stream.filter(follow=["198829810", "7996082", "145992645", "26729931", "74453123", "14436030", "10012122"])


class CommentScragThread(threading.Thread):
    def __init__(self, api, tweet_id, callbackFunc):
        threading.Thread.__init__(self, daemon=True)
        self.api = api
        self.tweet_id = tweet_id
        self.callback = callbackFunc

    def run(self):
        tweet = self.api.get_status(self.tweet_id)
        self.callback(tweet)