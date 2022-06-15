# coding: UTF-8
import psycopg2
import datetime
import sys
sys.path.append('../')
from propeties import config
from util import datetime_util

def is_retweeted(conn, tweet_id):
    try:
        cur = conn.cursor()
        cur.execute('select count(tweet_id) from RETWEET_HISTORY where tweet_id = ' + str(tweet_id))
        res = cur.fetchone()

    finally:
        if(cur):
            cur.close()

    return res[0]


### 本メソッドから呼び出されるメソッドは全て動作未確認
def insert_retweet_info(conn, tweet, query_id):
    try:
        cur = conn.cursor()
        insert_retweet_history(cur, tweet, query_id)
        insert_tweet_info(cur, tweet)
        insert_use_hashtag_history(cur, tweet)
        # 次を追加
        # ①insert_user_info()
        # ②class化

        cur.commit()
    finally:
        cur.close()



def insert_retweet_history(cur, tweet, used_query_id):

    insert_retweet_history = config.ROOT_PATH + '/src/sql/ddl/insert_retweet_history.sql'
    with open(insert_retweet_history, 'r') as f:
        query = f.read()

    cur.execute(query, {
        'tweet_id':tweet['id'],
        'used_query_id':used_query_id,
        'retweet_tm':datetime.datetime.now(config.JST).strftime('%Y/%m/%d %H:%M:%S')
    })


def insert_tweet_info(cur, tweet):

    insert_tweet_info = config.ROOT_PATH + '/src/sql/ddl/insert_tweet_info.sql'
    with open(insert_tweet_info, 'r')as f:
        query = f.read()

    cur.execute(query, {
        'tweet_id':tweet['id'],
        'tweet_url':tweet['entities']['urls'][0]['url'],
        'text':tweet['text'],
        'media_url':tweet['entities']['media'][0]['media_url_https'],
        'user_id':tweet['user']['id'],
        'tweet_tm':__format_datetime(tweet['created_at'])
    })


def insert_use_hashtag_history(cur, tweet):

    insert_use_hashtag_history = config.ROOT_PATH + '/src/sql/ddl/insert_use_hashtag_history.sql'
    with open(insert_use_hashtag_history, 'r')as f:
        query = f.read()
    for hashtag in tweet['entities']['hashtags']:
        cur.execute(query, {
            'tweet_id':tweet['id'],
            'hashtag':hashtag
        })


def __format_datetime(dt):
    twitter_format = '%a %b %d %H:%M:%S %z %Y'
    local_format = '%Y/%m/%d %H:%M:%S'
    return datetime_util.convert_to_jst(dt, twitter_format, local_format)