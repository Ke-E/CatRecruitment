# coding: UTF-8
from requests_oauthlib import OAuth1Session

def get_oauth():
    #取得したレスポンスの格納先
    FILEPATH = "/Users/k.enomoto/Desktop/workspace/Twitter API/response.json"

    #取得した認証キーを設定
    CONSUMER_KEY = "m0fG9UYLZ0JwEC64dss995inM"
    CONSUMER_SECRET = "gFfa2SNmgEebXIauB7xiwqlNKU5YdF2feImQ7jv15UyKYb44rS"
    ACCESS_TOKEN = "1525295386151137280-vlckvY3O01uibZenuAzWC8TBJpOTs9"
    ACCESS_SECRET = "Zbqo38F1lemtt1kQRTk3TjvocHqiR5iIfkUOgpg0dzP41"

    return OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)