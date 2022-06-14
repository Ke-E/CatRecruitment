# coding: UTF-8
import psycopg2
import datetime
import sys
sys.path.append('../')
from propeties import config

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
        # もしかしたら型違いでエラーの可能性
        'tweet_tm':tweet['created_at'],
        'ins_tm':datetime.datetime.now()
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

