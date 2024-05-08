"""
@Project        ：tea_server_api 
@File           ：setup_database.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:50 
@Description    ：
"""
from types import ModuleType
from typing import Optional, Dict, Iterable, Union

from fastapi import FastAPI

from config.setting import setting
from setup.setup_logger import logger
from tortoise import Tortoise, connections




async def setup_database(app: FastAPI):
    await init_tortoise(db_url=setting.DB_URL,  # 数据库信息
                        modules={"models": setting.DB_MODELS},  # models列表
                        generate_schemas=False,  # 如果数据库为空，则自动生成对应表单,生产环境不要开)
                        )


async def init_tortoise(
        config: Optional[dict] = None,
        config_file: Optional[str] = None,
        db_url: Optional[str] = None,
        modules: Optional[Dict[str, Iterable[Union[str, ModuleType]]]] = None,
        generate_schemas: bool = False,
):
    await Tortoise.init(config=config, config_file=config_file, db_url=db_url, modules=modules)
    logger.info(f"Tortoise-ORM 初始化成功, {Tortoise.apps}")
    if generate_schemas:
        logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()


async def close_database():
    await connections.close_all()
    logger.info("Tortoise-ORM shutdown")