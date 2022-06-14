# coding: UTF-8
import datetime
import sys
sys.path.append('../')
from propeties import config

# 文字列で送られてきたタイムゾーン[UTC]の日付を datetime 形式かつ JST に変換して返す
def convert_to_jst(utc, before_format, after_format):
    utc_dt = datetime.datetime.strptime(utc, before_format)
    jst_dt = utc_dt.astimezone(config.JST)
    return datetime.datetime(jst_dt, after_format)
