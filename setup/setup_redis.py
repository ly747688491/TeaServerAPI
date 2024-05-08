"""
@Project        ：tea_server_api 
@File           ：setup_redis.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:51 
@Description    ：
"""
from fastapi import FastAPI

from config.setting import setting
from cores.redis import RedisService
from setup.setup_logger import logger


async def setup_redis(app: FastAPI):
    redis: RedisService = await init_redis_pool()  # redis
    app.state.redis = redis


# 参考: https://github.com/grillazz/fastapi-redis/tree/main/app
async def init_redis_pool() -> RedisService:
    """连接redis"""
    result = await RedisService.from_url(url=setting.REDIS_URL, encoding=setting.GLOBAL_ENCODING, decode_responses=True)
    logger.info("初始化redis成功")
    return result
