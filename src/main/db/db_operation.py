# coding: UTF-8
import sys
sys.path.append('../')
from propeties import config
from util import datetime_util

# self についてちょっと調べる

class DbOperation:
    """DB操作を行うクラス

    DBの参照、登録、削除などはこのクラスを使用する。

    Args:
        conn (Connection): postgresql に接続するために使用するDBコネクション

    Attribute:
        __twitter_dt_format (string): Twitterの日時情報のフォーマット
        __conn (Connection): クラス内で使用するDBコネクション

    """

    __twitter_dt_format = '%a %b %d %H:%M:%S %z %Y'
    __cunn = None
    def __init__(self, conn):
        self.__conn = conn
        """DBコネクションを渡すコンストラクタ

        DB接続に使用するコネクションを引数で受け取り、格納する
        """

    def get_queries(self):
        """ツイート検索に使用するクエリ一覧を取得する

        削除フラグが false であるクエリを全て取得する。

        Returns:
            list: 取得した削除フラグが false のクエリ

        """
        path = config.ROOT_PATH + '/src/sql/ddl/read/get_queries.sql'
        with open(path, 'r') as f:
            query = f.read()

        with self.__conn.cursor() as cur:
            cur.execute(query)
            res = cur.fetchall()

        return res


    def is_retweeted(self, tweet_id):
        """引数のツイートIDが既にリツイート済みかを判定、結果を返却する

        テーブル「retweet_history」から、引数に指定されたツイートIDを検索し、
        既にリツイート済みなら True、リツイートがまだなら False を返す。

        Note:
            True か False かの判定は SQL で処理しているので注意

        Args:
            tweet_id (int): リツイート済みかを判定するツイートID

        """

        path = config.ROOT_PATH + '/src/sql/ddl/read/is_retweeted.sql'
        with open(path, 'r') as f:
            query = f.read()

        with self.__conn.cursor() as cur:
            cur.execute(query, {
                'tweet_id':tweet_id
            })
            res = cur.fetchone()

        return res[0]


    def insert_retweet_info(self, tweet, query_id):
        """リツイートを行うツイート情報を各種テーブルに格納する

        Args:
            tweet (object): ツイート情報
            query_id (int): ツイート取得に使用したクエリID

        """
        with self.__conn.cursor() as cur:

            self.__insert_retweet_history(cur, tweet, query_id)
            self.__insert_tweet_info(cur, tweet)
            self.__insert_use_hashtag_history(cur, tweet)
            self.__insert_user_info(cur, tweet)


    def __insert_retweet_history(self, cur, tweet, query_id):
        """テーブル「リツイート履歴」にデータを登録する

        Args:
            cur (object): DBへ接続するためのカーソル
            tweet (object): ツイート情報
            query_id (int): ツイート情報に使用したクエリID

        """
        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_retweet_history.sql'
        with open(path, 'r') as f:
            query = f.read()

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'used_query_id':query_id
        })


    def __insert_tweet_info(self, cur, tweet):
        """テーブル「ツイート情報」にデータを登録する

        Args:
            cur (object): DBへ接続するためのカーソル
            tweet (object): ツイート情報

        """
        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_tweet_info.sql'
        with open(path, 'r')as f:
            query = f.read()

        cur.execute(query, {
            'tweet_id':tweet['id'],
            'text':tweet['text'],
            'tweet_tm':datetime_util.convert_to_jst(tweet['created_at'], self.__twitter_dt_format)
        })


    def __insert_use_hashtag_history(self, cur, tweet):
        """テーブル「利用ハッシュタグ履歴」にデータを登録する

        複数ハッシュタグが使用されている場合は、その数分登録を行う

        Args:
            cur (object): DBへ接続するためのカーソル
            tweet (object): ツイート情報

        """
        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_use_hashtag_history.sql'
        with open(path, 'r')as f:
            query = f.read()

        for hashtag in tweet['entities']['hashtags']:
            cur.execute(query, {
                'tweet_id':tweet['id'],
                'hashtag':hashtag['text']
        })


    def __insert_user_info(self, cur, tweet):
        """テーブル「利用ユーザ情報」にデータを登録する

        Args:
            cur (object): DBへ接続するためのカーソル
            tweet (object): ツイート情報

        """
        path = config.ROOT_PATH + '/src/sql/ddl/create/insert_user_info.sql'
        with open(path, 'r')as f:
            query = f.read()

        cur.execute(query, {
            'user_id':tweet['user']['id'],
            'tweet_id':tweet['id'],
            'name':tweet['user']['name'],
            'screen_name':tweet['user']['screen_name'],
            'location':tweet['user']['location'],
            'description':tweet['user']['description'],
            'url':tweet['user']['url'] or ''
        })

