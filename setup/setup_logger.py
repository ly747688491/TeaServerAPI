"""
@Project        ：tea_server_api
@File           ：setup_logger.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午10:50
@Description    ：
"""

import logging
import os

from loguru import logger

from config.setting import setting
from utils.common_utils import create_dir


def logger_file() -> str:
    """创建日志文件名"""
    log_path = create_dir(setting.LOGGER_DIR)
    # 日志输出路径
    return os.path.join(log_path, setting.LOGGER_NAME)


# 将已写好的logging集成到loguru中
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# 日志配置
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
        },
    },
    "loggers": {
        "tortoise": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


def logger_init():
    """日志初始化"""
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    # 详见: https://loguru.readthedocs.io/en/stable/overview.html#features
    logger.add(
        logger_file(),  # 保存日志信息的文件路径
        encoding=setting.GLOBAL_ENCODING,  # 日志文件编码
        level=setting.LOGGER_LEVEL,  # 文件等级
        rotation=setting.LOGGER_ROTATION,  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
        retention=setting.LOGGER_RETENTION,  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]
        enqueue=True,  # 在多进程同时往日志文件写日志的时候使用队列达到异步功效
    )
    # 应用日志配置
    logging.config.dictConfig(logging_config)
