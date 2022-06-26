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
# ログを出したい

# TwitterAPI OAuth1認証情報取得
oauth = OAuth1Session(
        config.CONSUMER_KEY,
        config.CONSUMER_SECRET,
        config.ACCESS_TOKEN,
        config.ACCESS_SECRET
    )

constr = "host='localhost' port=5432 dbname=cat_recruitment"
# 本当は右記も入れるが、今はこれでいい 「user=yamada password='hoge1234'」

print('===== 処理開始 =====')
# コネクションの取得
with psycopg2.connect(constr) as conn:

    # 各種インスタンスの取得
    db_operation = DbOperation(conn)
    tweet_operation = TweetOperation(oauth)

    # 登録されているクエリ情報を取得
    for query_info in db_operation.get_queries():

        # 必要情報を取得しておく
        query_id = query_info[0]
        query = query_info[1]
        print('----- 【実行クエリ：' + query + '】 -----')

        # ツイート検索
        timeline = tweet_operation.search_tweet(query)

        for tmp_tweet in timeline['statuses']:
            # リツイート履歴がなければ処理対象
            if db_operation.is_retweeted(tmp_tweet['id']) == False:
                print('新規ツイート：' + str(tmp_tweet['id']))
                tweet = tmp_tweet
                break
            else:
                print('リツイート済み：' + str(tmp_tweet['id']))
        else:
            # 全件リツイート済みである場合は次のクエリへ
            print('全件リツイート済み')
            continue

        # ツイート情報の登録
        db_operation.insert_retweet_info(tweet, query_id)
        # リツイート
        response_code = tweet_operation.retweet(tweet['id'])
        if response_code == 200:
            conn.commit()
            break
        else:
            # リツイートに失敗した場合はロールバックし処理を終了
            print('リツイートに失敗しました。')
            conn.rollback()
            break
    else:
        print('処理対象なし')



print('===== 処理終了 =====')




#クエリ候補
#result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
#result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])
