# coding: UTF-8
import psycopg2
from propeties import config
from requests_oauthlib import OAuth1Session
from tweet.tweet_operation import TweetOperation
from db.db_operation import DbOperation

# 全体のリファクタリング
# sqlファイルのインデント調整
# コメント付与
# search_query の id はインクリメントにしても良さそう

# TwitterAPI OAuth1認証情報取得
oauth = OAuth1Session(
        config.CONSUMER_KEY,
        config.CONSUMER_SECRET,
        config.ACCESS_TOKEN,
        config.ACCESS_SECRET
    )

constr = "host='localhost' port=5432 dbname=cat_recruitment"
# 本当は右記も入れるが、今はこれでいい 「user=yamada password='hoge1234'」

with psycopg2.connect(constr) as conn:

    # データベース操作を行うインスタンスの取得
    db_operation = DbOperation(conn)
    for query_info in db_operation.get_queries():

        query_id = query_info[0]
        query = query_info[1]
        print('実行クエリ：' + query)

        # ツイート検索
        tweet_operation = TweetOperation(oauth)
        timeline = tweet_operation.search_tweet(query)


        for tmp_tweet in timeline['statuses']:
            if db_operation.is_retweeted(tmp_tweet['id']) == False:
                print('新規ツイート：' + str(tmp_tweet['id']))
                tweet = tmp_tweet
                break
            else:
                print('リツイート済み：' + str(tmp_tweet['id']))
        else:
            print('全件リツイート済み')

        if tweet != None:
            db_operation.insert_retweet_info(tweet, query_id)
            # リツイート
            response_code = tweet_operation.retweet(tweet['id'])
            if response_code == 200:
                # query_id は一旦固定
                print('処理完了')
                break
    else:
        print('処理対象なし')


#クエリ候補
#result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
#result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])
