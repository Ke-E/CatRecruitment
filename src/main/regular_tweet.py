# coding: UTF-8
import sys
sys.path.append('../')
import psycopg2
import json
from logging import getLogger, config as logging_config
from propeties import config
from util import datetime_util
from requests_oauthlib import OAuth1Session
from tweet.tweet_operation import TweetOperation
from db.db_operation import DbOperation


# レスポンスの異常検知
# 全体のリファクタリング

# loggerの設定
with open(config.ROOT_PATH + config.LOG_CONFIG_PATH, 'r') as f:
    log_conf = json.load(f)

logging_config.dictConfig(log_conf)
logger = getLogger('main')


# TwitterAPI OAuth1認証情報取得
oauth = OAuth1Session(
        config.CONSUMER_KEY,
        config.CONSUMER_SECRET,
        config.ACCESS_TOKEN,
        config.ACCESS_SECRET
    )

constr = "host='localhost' port=5432 dbname=cat_recruitment"
# 本当は右記も入れるが、今はこれでいい 「user=yamada password='hoge1234'」

logger.info('▽▽▽▽▽ 処理開始 ▽▽▽▽▽')
# コネクションの取得
with psycopg2.connect(constr) as conn:

    # 各種インスタンスの取得
    db_operation = DbOperation(conn)
    tweet_operation = TweetOperation(oauth)

    # 登録されているクエリ情報を取得
    for query_info in db_operation.get_queries():

        # 必要情報を取得しておく
        query_id = query_info[0]
        query = query_info[1] + datetime_util.create_query_format_datetime()
        logger.info('----- 【実行クエリ： {} 】 -----'.format(query))

        try:
            # ツイート検索
            timeline = tweet_operation.search_tweet(query)

            for tmp_tweet in timeline['statuses']:
                # リツイート履歴がなければ処理対象
                if not db_operation.is_retweeted(tmp_tweet['id']):
                    logger.info('処理対象ツイートID：{}'.format(str(tmp_tweet['id'])))
                    tweet = tmp_tweet
                    break

            else:
                # 全件リツイート済みである場合は次のクエリへ
                logger.info('全件リツイート済み')
                continue

        except AttributeError as e:
            # 想定される key が存在しない or ツイート取得に失敗した場合は処理を終了
            logger.error(e)
            sys.exit()

        # ツイート情報の登録
        db_operation.insert_retweet_info(tweet, query_id)
        # リツイート
        response_code = tweet_operation.retweet(tweet['id'])
        if response_code == 200:
            conn.commit()
            break
        else:
            # リツイートに失敗した場合はロールバックし、処理を終了
            logger.error('リツイートに失敗しました。')
            conn.rollback()
            break
    else:
        logger.info('処理対象なし')


logger.info('▲▲▲▲▲ 処理終了 ▲▲▲▲▲')




#クエリ候補
#result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
#result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])
