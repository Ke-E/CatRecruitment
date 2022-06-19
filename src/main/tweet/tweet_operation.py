# coding: UTF-8
import urllib
import codecs
import json
import requests
import sys
sys.path.append('../')
from propeties import config

class TweetOperation:

    oauth = None
    def __init__(self, oauth):
        self.oauth = oauth


    def retweet(self, tweet_id):
        url = config.API_URL1 + "/statuses/retweet/" + str(tweet_id) + ".json"
        res = self.oauth.post(url)
        print(res.status_code)
        print(res.json())
        return res.status_code


    def search_tweet(self, query):
        query = urllib.parse.quote(query)
        url = config.API_URL1 + "/search/tweets.json?q=" + query + "&result_type=recent&count=100"
        res = self.oauth.get(url)

        timeline = json.loads(res.text)

        with open(config.FILEPATH, 'w') as f:
            f.write(json.dumps(timeline, indent=2, ensure_ascii=False))
            f.close()

        return timeline

