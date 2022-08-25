# coding: UTF-8
import sys
sys.path.append('../')
import psycopg2
import json
from logging import getLogger, config as logging_config
from propeties import config
from requests_oauthlib import OAuth1Session
from tweet.tweet_operation import TweetOperation


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
    tweet_operation = TweetOperation(oauth)

    with open(config.ROOT_PATH + config.REGULAR_TWEET_TEXT_PATH, 'r') as f:
        tweet_text = f.read()

    try:
        # ツイート検索
        status_code = tweet_operation.tweet(tweet_text)
    except AttributeError as e:
        # 想定される key が存在しない or ツイート取得に失敗した場合は処理を終了
        logger.error(e)
        sys.exit()


logger.info('▲▲▲▲▲ 処理終了 ▲▲▲▲▲')




#クエリ候補
#result = re.search('神奈川県|東京都|群馬県|千葉県|埼玉県|栃木県|茨城県', tweet["user"]["description"])
#result = re.search('神奈川|東京|群馬|千葉|埼玉|栃木|茨城', tweet["text"])
