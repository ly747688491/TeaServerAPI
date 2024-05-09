"""
@Project        ：tea_server_api
@File           ：machine_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:28
@Description    ：
"""

from cores.dao import create_dao
from modules.machine.entity.models import Machine
from modules.machine.entity.schemas import MachineSchema


def get_machine_dao():
    return create_dao(model=Machine, schema_model=MachineSchema)
