# coding: UTF-8
import psycopg2
from propeties import config
from requests_oauthlib import OAuth1Session
from tweet import tweet_operation, tweet_search


# TwitterAPI OAuth1認証情報取得
oauth = OAuth1Session(
        config.CONSUMER_KEY, 
        config.CONSUMER_SECRET, 
        config.ACCESS_TOKEN, 
        config.ACCESS_SECRET
    )
try:
    constr = "host='localhost' port=5432 dbname=cat_recruitment"
    # 本当は右記も入れるが、今はこれでいい 「user=yamada password='hoge1234'」
    conn = psycopg2.connect(constr)


    # 検索用のクエリ
    query = "里親 猫 募集 (神奈川 OR 東京 OR 群馬 OR 千葉 OR 埼玉 OR 栃木 OR 茨城) -@ filter:twimg -filter:retweets"
    #result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
    #result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])

    # query をリスト(タプル)で持つ
    # リストの数だけループし、ツイート検索の結果、リツイートしてOKだった場合はリツイートする
    # いずれも既にリツイート済み、もしくは対象がなかった場合はリツイートを行わず正常終了とする

    ### search_id 周りのリファクタリングがしたいなぁ
    ### tweet_operation の中に内包されていてもおかしくないし

    # ツイート検索
    tweet_id = tweet_search.search_id(conn, oauth, query)

    if tweet_id != None:
        # リツイート
        result = tweet_operation.retweet(oauth, tweet_id)
        #print(result)
finally:
    conn.close()
