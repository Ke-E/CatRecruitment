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
    __cunn = None
    def __init__(self, conn):
        self.__conn = conn
    # sqlファイルのインデント統一

    def get_queries(self):

        path = config.ROOT_PATH + '/src/sql/ddl/read/get_queries.sql'
        with open(path, 'r') as f:
            query = f.read()

        with self.__conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()
        print(res)
        return res


    def is_retweeted(self, tweet_id):

        path = config.ROOT_PATH + '/src/sql/ddl/read/is_retweeted.sql'
        with open(path, 'r') as f:
            query = f.read()

        with self.__conn.cursor() as cur:
            cur.execute(query, {
                'tweet_id':tweet_id
            })
            res = cur.fetchone()

        return res[0]


    ### 本メソッドから呼び出されるメソッドは全て動作未確認
    def insert_retweet_info(self, tweet, query_id):

        with self.__conn.cursor() as cur:

            self.__insert_retweet_history(cur, tweet, query_id)
            self.__insert_tweet_info(cur, tweet)
            self.__insert_use_hashtag_history(cur, tweet)
            self.__insert_user_info(cur, tweet)


    def __insert_retweet_history(self, cur, tweet, used_query_id):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_retweet_history.sql'
        with open(path, 'r') as f:
            query = f.read()

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'used_query_id':used_query_id
        })


    def __insert_tweet_info(self, cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_tweet_info.sql'
        with open(path, 'r')as f:
            query = f.read()

        tmp = self.__format_datetime(tweet['created_at'])
        print(tmp)
        print(type(tmp))

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'text':tweet['text'],
            'tweet_tm':self.__format_datetime(tweet['created_at'])
        })


    def __insert_use_hashtag_history(self, cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_use_hashtag_history.sql'
        with open(path, 'r')as f:
            query = f.read()
        for hashtag in tweet['entities']['hashtags']:
            cur.execute(query, {
                'tweet_id':tweet['id'],
                'hashtag':hashtag['text']
        })


    def __insert_user_info(self, cur, tweet):

        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_user_info.sql'
        with open(path, 'r')as f:
            query = f.read()
        print(tweet['user'])
        #for user in tweet['user']:
        cur.execute(query, {
            'user_id':tweet['user']['id'],
            'tweet_id':tweet['id'],
            'name':tweet['user']['name'],
            'screen_name':tweet['user']['screen_name'],
            'location':tweet['user']['location'],
            'description':tweet['user']['description'],
            'url':tweet['user']['url'] or ''
        })


    def __format_datetime(self, dt):
        twitter_format = '%a %b %d %H:%M:%S %z %Y'
        local_format = '%Y/%m/%d %H:%M:%S'
        return datetime_util.convert_to_jst(dt, twitter_format, local_format)