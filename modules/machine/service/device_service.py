"""
@Project        ：tea_server_api
@File           ：device_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:28
@Description    ：
"""

from cores.dao import create_dao
from modules.machine.entity.models import Device
from modules.machine.entity.schemas import DeviceSchema


def get_device_dao():  # -> BaseDao:
    return create_dao(model=Device, schema_model=DeviceSchema)
