# coding: UTF-8
import propeties.config
from requests_oauthlib import OAuth1Session
from tweet.tweet_operation import retweet
from tweet.tweet_search import search_id
import psycopg2

# TwitterAPI OAuth1認証情報取得
oauth = OAuth1Session(
        config.CONSUMER_KEY, 
        config.CONSUMER_SECRET, 
        config.ACCESS_TOKEN, 
        config.ACCESS_SECRET
    )

constr = "host='localhost' port=5432 dbname=cat_recruitment"
# 本当は右記も入れるが、今はこれでいい 「user=yamada password='hoge1234'」
conn = psycopg2.connect(constr)


# 検索用のクエリ
query = "里親 猫 募集 (神奈川 OR 東京 OR 群馬 OR 千葉 OR 埼玉 OR 栃木 OR 茨城) -@ filter:twimg -filter:retweets"
#result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
#result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])

# ツイート検索
tweet_id = search_id(conn, oauth, query)
# リツイート
#result = retweet(oauth, tweet_id)
#print(result)

