import sys
import json
from logging import getLogger, config as logging_config
sys.path.append('../')
from propeties import config

class Logger:
    """Loggerを生成する操作を行う
    """

    def get_logger(self):
        """loggerを生成、返す

        Returns:
            Logger: 汎用的な出力を行うlogger

        """
        with open(config.ROOT_PATH + config.LOG_CONFIG_PATH, 'r') as f:
            log_conf = json.load(f)

        logging_config.dictConfig(log_conf)
        return getLogger('main')