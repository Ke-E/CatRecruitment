# coding: UTF-8
import re
import urllib
import json
import requests
import config
from db_operation import search_retweet_history

def search_id(conn, oauth, query):
    query = urllib.parse.quote(query)
    url = config.API_URL1 + "/search/tweets.json?q=" + query + "&result_type=recent&count=100"
    res = oauth.get(url)

    timeline = json.loads(res.text)

    with open(config.FILEPATH, 'w') as f:
        f.write(json.dumps(timeline, indent=2, ensure_ascii=False))
        f.close()

    for tweet in timeline["statuses"]:
        result = is_retweeted(conn, tweet["id"])
        if result == False:
            return tweet["id"]
    
    print("新規投稿無し")
    return None