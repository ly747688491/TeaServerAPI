"""
@Project        ：tea_server_api
@File           ：material_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:28
@Description    ：
"""

from cores.dao import create_dao
from modules.machine.entity.models import Material
from modules.machine.entity.schemas import MaterialSchema


def get_oper_dao():
    return create_dao(model=Material, schema_model=MaterialSchema)
