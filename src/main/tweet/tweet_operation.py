# coding: UTF-8
import urllib
import json
import sys
sys.path.append('../')
from propeties import config

class TweetOperation:
    """Twitter API を利用する操作を行う

    Args:
        oauth (object): OAuth1認証情報

    Attribute:
        __oauth (object): OAuth1認証情報

    """
    __oauth = None
    def __init__(self, oauth):
        self.__oauth = oauth


    def tweet(self, tweet_text):
        """引数に渡されたテキストでツイートを行う

        Args:
            tweet_text (string): ツイート内容
        """
        api_url = config.API_URL1 + "/statuses/update.json"

        # リクエストボディ
        params = {
            "status": tweet_text
        }

        res = self.__oauth.post(url=api_url, data=params)
        return res.status_code


    def retweet(self, tweet_id):
        """引数のツイートIDであるツイートをリツイートする

        Args:
            tweet_id (int): リツイート対象とするツイートID

        """
        url = config.API_URL1 + "/statuses/retweet/" + str(tweet_id) + ".json"
        res = self.__oauth.post(url)
        return res.status_code


    def search_tweet(self, query):
        """引数のクエリを用いてツイート検索を行う

        クエリの内容に関わらず、並び順は最新、最大100件とする

        Args:
            query (string): ツイート検索に使用するクエリ

        """
        query = urllib.parse.quote(query)
        url = config.API_URL1 + "/search/tweets.json?q=" + query + "&result_type=recent&count=100"
        res = self.__oauth.get(url)
        timeline = json.loads(res.text)

        with open(config.FILEPATH, 'w') as f:
            f.write(json.dumps(timeline, indent=2, ensure_ascii=False))
            f.close()

        return timeline

