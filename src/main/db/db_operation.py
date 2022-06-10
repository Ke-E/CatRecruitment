# coding: UTF-8
import psycopg2

def is_retweeted(conn, tweet_id):
    cur = conn.cursor()
    cur.execute('select * from hoge where id >= 10000')
    res = cur.fetchall()
    print(res)
    cur.close()
    conn.close()
    return #Boolean