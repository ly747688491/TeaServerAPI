"""
@Project        ：tea_server_api
@File           ：material_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:35
@Description    ：
"""

from fastapi import APIRouter


MaterialRouter = APIRouter(prefix="/material", tags=["物料模块"])
