import threading
from tweepy import OAuthHandler, API, Cursor, StreamListener, Stream
import json
import datetime

from Config import *
from ddbb.DBManager import DBManager
from scraping.TwitterScrapThread import ScrapThread, StreamThread, CommentScragThread


class TwitterManager:
    __instance = None

    class __Manager:
        def __init__(self):
            self.authenticate = OAuthHandler(APIKEY, APISECRETKEY)
            self.authenticate.set_access_token(ACCESTOKEN, ACCESTOKENSECRET)
            self.api = API(self.authenticate)
            self.sourcesCounter = {}  # Creem un diccionari on guardarem les vegades que ha demanat per rebre tweets
            self.db_manager = DBManager()
            self.db_manager.setFactorySource("Mongo")

        def treat_tweet(self, tweet):
            newT = {}
            if 'retweeted_status' in tweet:
                newT['original_media_name'] = tweet['retweeted_status']['user']['name']
                newT['retweet_user'] = tweet['user']['name']
                newT["tweet"] = {}
                newT["tweet"]["tweet_id"] = tweet['retweeted_status']['id']
                newT["tweet"]["created_at"] = tweet['retweeted_status']['created_at']
                newT["tweet"]["text"] = tweet['retweeted_status']['text']
                newT["tweet"]["retweets"] = tweet['retweeted_status']['retweet_count']
                newT["tweet"]["favourites"] = tweet['retweeted_status']['favorite_count']
                if 'extended_tweet' in tweet:
                    if 'entitites' in tweet ['retweeted_status']:
                        if 'urls' in tweet['retweeted_status'] in tweet ['retweeted_status'] ['entities']:
                            if (len(tweet ['retweeted_status'] ['entities']['urls']) > 0):
                                newT["url"] = tweet ['retweeted_status'] ['entities']['urls'][0]['url']
            else:
                if tweet['in_reply_to_status_id'] is None:
                    newT["media_name"] = tweet['user']['name']
                    newT["tweet"] = {}
                    newT["tweet"]["tweet_id"] = tweet['id']
                    newT["tweet"]["created_at"] = tweet['created_at']
                    newT["tweet"]["text"] = tweet['text']
                    newT["tweet"]["retweets"] = tweet['retweet_count']
                    newT["tweet"]["favourites"] = tweet['favorite_count']
                    if 'entitites' in tweet:
                        if (len(tweet['entities']['urls']) > 0):
                            newT["url"] = tweet['entities']['urls'][0]['url']

                else:
                    newT["tweet"] = {}
                    newT["tweet_id"] = tweet['in_reply_to_status_id']
                    newT['commented_user'] = tweet['user']['name']
                    newT["comment"] = {}
                    newT["comment"]["text"] = tweet['text']
                    newT["comment"]["user"]= tweet['user']['name']
                    newT["comment"]["created_at"] = tweet['created_at']
                    original_tweet = self.api.get_status(tweet['in_reply_to_status_id'])._json
                    newT["tweet"]["text"] = original_tweet['text']
                    newT["media_name"] = original_tweet['user']['name']
            return newT

        def on_get_original_tweet(self, tweet):
            print()

        def read_comment(self, tweet_id):
            thread = CommentScragThread(self.api, tweet_id, self.on_get_original_tweet)
            thread.start()

        def on_read_tweets_response(self, tweets):
            for tweet in tweets:
                filteredTweet = self.treat_tweet(tweet)
                if filteredTweet:
                    self.db_manager.insert_item("media", filteredTweet)

        def read_tweets_from_source(self, media_name):
            if len(self.sourcesCounter) == 0:
                self.sourcesCounter[media_name] = 0
            counter = self.sourcesCounter[media_name]
            thread = ScrapThread(self.api, media_name, counter, self.on_read_tweets_response)
            thread.start()
            self.sourcesCounter[media_name] += 1

        def on_read_stream(self, item):
            tweet = self.treat_tweet(item)
            print(tweet)
            if tweet:
                self.db_manager.insert_item("media", tweet)

        def start_stream_from_source(self, media_name):
            listener = Listener(self.on_read_stream)
            stream = Stream(self.authenticate, listener)
            stream.filter(follow=["198829810", "7996082", "145992645", "26729931", "74453123", "14436030", "10012122"])

            thread = StreamThread(stream, self.on_read_tweets_response)
            thread.start()

    instance = None

    def __init__(self):
        if not TwitterManager.instance:
            TwitterManager.instance = TwitterManager.__Manager()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def getTweetsFromUnderHour(self, obj):
        # Nomes ens quedem amb els tweets de fa una hora
        # Normalment se fica a la data un +0000 l'eliminem per a que pugui comprovar rapidament la data
        obj_date = obj['created_at']
        obj_operator = obj['created_at'].find('+')
        new_operator = obj['created_at'].find('+') + 6
        popper = obj_date[:obj_operator] + obj_date[new_operator:]
        # Se guarda en una hora menos, per tant fem la resta
        date_time_obj = datetime.datetime.strptime(popper, '%a %b %d %H:%M:%S %Y')
        date_time_obj = date_time_obj + datetime.timedelta(hours=1)
        hols = datetime.datetime.now()

        # Aixi comprovem si la distancia es major de una hora
        date_time_obj = date_time_obj + datetime.timedelta(hours=1)
        return date_time_obj


class Listener(StreamListener):
    __comptador = 0
    __listTweets = []

    def __init__(self, callback):
        super(Listener, self).__init__()
        self.callback = callback

    def on_data(self, data):
        obj = json.loads(data)
        self.callback(obj)

    def on_error(self, status):
        print(status)

    def getTweets(self):
        return self.__listTweets
