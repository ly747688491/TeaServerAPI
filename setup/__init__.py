"""
@Project        ：tea_server_api
@File           ：__init__.py.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:52
@Description    ：
"""

from .setup_cors import setup_cors
from .setup_database import setup_database
from .setup_exception import setup_exception
from .setup_logger import logger_init
from .setup_mount import setup_mount
from .setup_redis import setup_redis
from .setup_router import setup_router
