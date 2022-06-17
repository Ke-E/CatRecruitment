# coding: UTF-8
import psycopg2
import datetime
import sys
sys.path.append('../')
from propeties import config
from util import datetime_util

# self についてちょっと調べる
# user_info の insert ファイル作成

class DbOperation:

    # コネクション
    cunn = None
    def __init__(self, conn):
        self.conn = conn


    def is_retweeted(self, tweet_id):

        path = config.ROOT_PATH + '/src/sql/ddl/read/is_retweeted.sql'
        with open(path, 'r') as f:
            query = f.read()
        try:
            cur = self.conn.cursor()
            cur.execute(query, {
                'tweet_id':tweet_id
            })
            res = cur.fetchone()

        finally:
            if(cur):
                cur.close()

        return res[0]


    ### 本メソッドから呼び出されるメソッドは全て動作未確認
    def insert_retweet_info(self, tweet, query_id):

        try:
            cur = self.conn.cursor()

            self.__insert_retweet_history(cur, tweet, query_id)
            self.__insert_tweet_info(cur, tweet)
            self.__insert_use_hashtag_history(cur, tweet)
            self.__insert_user_info()

            cur.commit()
        finally:
            cur.close()



    def __insert_retweet_history(cur, tweet, used_query_id):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_retweet_history.sql'
        with open(path, 'r') as f:
            query = f.read()

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'used_query_id':used_query_id,
            'retweet_tm':datetime.datetime.now(config.JST).strftime('%Y/%m/%d %H:%M:%S')
        })


    def __insert_tweet_info(self, cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_tweet_info.sql'
        with open(path, 'r')as f:
            query = f.read()

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'tweet_url':tweet['entities']['urls'][0]['url'],
            'text':tweet['text'],
            'media_url':tweet['entities']['media'][0]['media_url_https'],
            'user_id':tweet['user']['id'],
            'tweet_tm':self.__format_datetime(tweet['created_at'])
        })


    def __insert_use_hashtag_history(cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_use_hashtag_history.sql'
        with open(path, 'r')as f:
            query = f.read()
        for hashtag in tweet['entities']['hashtags']:
            cur.execute(query, {
                'tweet_id':tweet['id'],
                'hashtag':hashtag
        })


    def __insert_user_info(cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_user_info.sql'
        with open(path, 'r')as f:
            query = f.read()
        for user in tweet['user']:
            cur.execute(query, {
                'user_id':user['id'],
                'tweet_id':tweet['id'],
                'name':user['name'],
                'screen_name':user['screen_name'],
                'location':user['location'],
                'description':user['description'],
                'url':user['url'] or ''
            })


    def __format_datetime(dt):
        twitter_format = '%a %b %d %H:%M:%S %z %Y'
        local_format = '%Y/%m/%d %H:%M:%S'
        return datetime_util.convert_to_jst(dt, twitter_format, local_format)