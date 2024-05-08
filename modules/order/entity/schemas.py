"""
@Project        ：tea_server_api 
@File           ：schemas.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:54 
@Description    ：
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from cores.schema import CoreSchema


class OrderStatus(str, Enum):
    pending = 'pending'
    processing = 'processing'
    queued = 'queued'
    completed = 'completed'
    cancelled = 'cancelled'


class OrderSchema(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.pending
    machine_id: Optional[int]
    material: Optional[str]


class OrderDetailsSchema(CoreSchema, OrderSchema):
    pass


class OrderPageQuerySchema(BaseModel):
    page_num: int = 1
    page_size: int = 10
    begin_time: Optional[str] = None
    end_time: Optional[str] = None
    id: Optional[str] = None
