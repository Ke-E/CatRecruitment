# coding: UTF-8
import urllib
import codecs
import json
import requests
import sys
sys.path.append('../')
from propeties import config

def retweet(oauth, retweet_id):
    url = config.API_URL1 + "/statuses/retweet/" + str(retweet_id) + ".json"
    res = oauth.post(url)
    print(res.status_code)
    print(res.json())
    return res.status_code




