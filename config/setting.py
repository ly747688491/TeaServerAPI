"""
@Project        ：tea_server_api
@File           ：setting.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:55
@Description    ：
"""

import secrets
from typing import List, Optional

from pydantic_settings import BaseSettings

project_desc = """
物联网系统用于控制树莓派的后台
存储管理设备信息用于给树莓派传递关键数据
"""


class Setting(BaseSettings):
    DEBUG: bool = True  # 开发模式配置
    TITLE: str = "TeaServe API"  # 项目文档
    DESCRIPTION: str = project_desc  # 描述
    VERSION: str = "v1.0"  # 版本

    # Uvicorn
    UVICORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    API_PREFIX: str = "/dev-api"  # 接口前缀
    DOCS_URL: str = "/docs"  # 文档地址 默认为docs
    REDOC_URL: Optional[str] = "/redoc"  # redoc 文档
    OPENAPI_URL: str = "/openapi.json"  # 文档关联请求数据接口
    STATIC_DIR: str = "static"  # 静态文件目录
    GLOBAL_ENCODING: str = "utf-8"  # 全局编码
    # 跨域请求
    CORS_ORIGINS: List[str] = ["*"]

    # Token
    # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 3  # token过期时间: 60 m * 3 hour
    ALGORITHM: str = "HS512"  # 生成token的加密算法

    # ADMIN_USERNAME = "admin"
    # ADMIN_PASSWORD = "admin123"

    # loguru
    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = "{time:YYYY-MM-DD}.log"  # 日志文件名 (时间格式)
    LOGGER_LEVEL: str = "DEBUG"  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "500 MB"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    # Database
    DB_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "milktea"
    DB_PASSWORD: str = "eNR6zXXi24rYG6TY"
    DB_DATABASE: str = "milktea"
    DB_CHARSET: str = "utf8mb4"
    DB_URL: str = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8mb4"
    DB_MODELS: list = [
        "modules.machine.entity.models",
    ]

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "Openai**@2023%_"
    REDIS_DATABASE: int = 1
    REDIS_TIMEOUT: int = 10
    REDIS_URL: str = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}?encoding=utf-8"

    # RabbitMq
    RABBITMQ_HOST: str = "127.0.0.1"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USERNAME: str = "tea_serve"
    RABBITMQ_PASSWORD: str = "******"
    RABBITMQ_VHOST: str = "/teapi"
    RABBITMQ_EXCHANGE: str = "exchange"

    class Config:
        case_sensitive = True  # 区分大小写


setting = Setting()
