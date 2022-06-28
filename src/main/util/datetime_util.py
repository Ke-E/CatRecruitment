# coding: UTF-8
import datetime
import sys
sys.path.append('../')
from propeties import config

def convert_to_jst(dt, format):
    """文字列で送られてきた日時情報を datetime 形式かつ JST に変換して返す

    Args:
        dt (string): 文字列の日時情報
        format (string): 引数「datetime」のフォーマット情報

    """
    return datetime.datetime.strptime(dt, format).astimezone(config.JST)
