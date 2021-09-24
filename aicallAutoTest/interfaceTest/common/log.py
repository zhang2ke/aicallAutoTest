import os
import logging
from logging.handlers import TimedRotatingFileHandler
from common.configInfo import ConfigInfo
import time

log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log")


class Logger(object):
    def __init__(self):
        self.log_info = ConfigInfo().get_log_info()
        self.log_file_name = self.log_info["name"]  # 日志文件的名称
        self.log_file_path = log_path  # 日志文件路径
        self.log_file_level = self.log_info["file_level"]  # 日志输出级别(输出到文件)
        self.log_console_level = self.log_info["console_level"]  # 日志输出级别(输出到控制台)
        self.log_file_bak_count = self.log_info["bak_count"]  # 最多存放日志的数量
        self.formatter = logging.Formatter('[%(asctime)s][%(funcName)s][%(levelname)s] %(message)s')  # 日志输出格式

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.log_console_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            self.log_file_name += time.strftime("%Y%m%d%H%M%S", time.localtime())
            file_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_file_path, self.log_file_name+".log"), when='D',
                                                    interval=1, backupCount=self.log_file_bak_count, delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.log_file_level)
            self.logger.addHandler(file_handler)
        return self.logger


if __name__ == "__main__":
    logger = Logger().get_logger()
    logger.warning("warning")
    logger.debug("debug")
    logger.error("error")
    logger.critical("critical")
    logger.info("info")
