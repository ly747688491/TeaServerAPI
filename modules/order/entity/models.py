"""
@Project        ：tea_server_api
@File           ：models.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from enum import Enum

from tortoise import fields

from cores.model import CoreModel


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    QUEUED = "queued"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderDetails(CoreModel):
    status = fields.CharEnumField(
        OrderStatus, default=OrderStatus.PENDING, null=False, index=True, description="订单状态"
    )
    machine = fields.ForeignKeyField(
        "models.Machine", related_name="orders", null=True, on_delete=fields.SET_NULL, description="关联机器"
    )
    material = fields.TextField(default="", null=False, description="所需材料")

    class Meta:
        table = "db_order"
        table_description = "订单信息表"
