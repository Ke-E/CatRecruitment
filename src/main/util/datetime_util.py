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

    Returns:
        datetime: JSTに変換した日付情報
    """
    return datetime.datetime.strptime(dt, format).astimezone(config.JST)


def create_query_format_datetime():
    """検索クエリ用の日付情報を文字列で生成、クエリ用にに作成した文字列を返す

    呼び出された日から2日前の日付情報を取得し、
    ツイート検索用にフォーマットを整え、keyを含めたクエリ文字列を返す

    Returns:
        String: サンプル:[ since:2022-8-10]
    """
    date = datetime.datetime.now(config.JST) - datetime.timedelta(days=2)
    return " since:" + date.strftime("%Y-%m-%d")