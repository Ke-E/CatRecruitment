# coding: UTF-8
import urllib
import codecs
import json
import requests
from twitter_oauth import get_oauth
import config


##取得したレスポンスの格納先
FILEPATH = "/Users/****/Desktop/workspace/Twitter API/response.json"

twitter = get_oauth()

#API用のURLを設定（●にはデベロッパー管理画面のDev environment labelを入力）
#query = urllib.parse.quote_plus("猫 exclude:retweets")
query = urllib.parse.quote("from:MHLWitter -filter:retweets")
url = "https://api.twitter.com/1.1/search/tweets.json?q="+ query +"&result_type=recent&count=10"

#paramsに検索ワードや件数、日付などを入力
#params = {'query' : 'Twitter API', #検索したいワード
#         "maxResults" : "100"}　#取得件数

#上記で設定したパラメーターをget関数を使い指定URLから取得
res = twitter.get(url)

timeline = json.loads(res.text)
for tweet in timeline["statuses"]:
    print(json.dumps(tweet["text"], indent=2, ensure_ascii=False))

with open(FILEPATH, 'w') as f:
    f.write(json.dumps(timeline, indent=2, ensure_ascii=False))
    f.close()

