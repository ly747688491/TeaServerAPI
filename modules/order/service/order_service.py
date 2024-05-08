"""
@Project        ：tea_server_api 
@File           ：order_service.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午11:33 
@Description    ：
"""
from cores.dao import create_dao
from modules.order.entity.models import OrderDetails
from modules.order.entity.schemas import OrderSchema


def get_config_dao():
    return create_dao(model=OrderDetails, schema_model=OrderSchema)
