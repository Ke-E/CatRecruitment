import sys
import json
from logging import getLogger, config as logging_config
sys.path.append('../')
from propeties import config

class Logger:
    """
    """

    def get_logger():
        """
        """
        with open(config.ROOT_PATH + config.LOG_CONFIG_PATH, 'r') as f:
            log_conf = json.load(f)

        logging_config.dictConfig(log_conf)
        return getLogger('main')