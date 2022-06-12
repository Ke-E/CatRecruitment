# coding: UTF-8
import psycopg2

def is_retweeted(conn, tweet_id):
    try:
        cur = conn.cursor()
        cur.execute('select count(tweet_id) from RETWEET_HISTORY where tweet_id = ' + str(tweet_id))
        res = cur.fetchone()

    finally:
        if(cur):
            cur.close()
    
    return res[0]