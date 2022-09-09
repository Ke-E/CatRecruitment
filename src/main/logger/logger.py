import sys
import json
from datetime import datetime
from logging import getLogger, config as logging_config
import logging.handlers
sys.path.append('../')
from propeties import config

class Logger:
    """Loggerを生成する操作を行う
    """

    # ログレベルを引数に設定し、予備元が好きなレベルのロガーを生成できるようにする
    def get_logger(self):
        """ログレベルがINFOなloggerを生成、返す

        Returns:
            Logger: 汎用的な出力を行うlogger

        """
        # loggerの生成
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # ログファイルハンドラーの設定
        log_name = config.LOG_PATH + config.LOG_NAME
        fh = logging.FileHandler(log_name.format(datetime.now()))
        fh.setLevel(logging.INFO)
        fh_formatter = logging.Formatter(fmt=config.LOG_OUTPUT_FMT, datefmt=config.LOG_DATE_FMT)
        fh.setFormatter(fh_formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter(fmt=config.LOG_OUTPUT_FMT, datefmt=config.LOG_DATE_FMT)
        ch.setFormatter(ch_formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger