"""
@Project        ：tea_server_api
@File           ：schemas.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OrderQuerySchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    id: Optional[int] = Field(None, alias="id")
    machine_id: Optional[int] = Field(None, alias="machineId")


class OrderListQuerySchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    order_list: Optional[List[OrderQuerySchema]] = Field(None)


# Define the Pydantic model
class OrderGoodsSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)
    id: int = Field(..., alias="id")
    machine_id: int = Field(None, alias="machineId")
    order_id: int = Field(None, alias="orderId")
    device_goods_id: int = Field(None, alias="deviceGoodsId")
    device_goods_option_id: int = Field(None, alias="deviceGoodsOptionId")
    goods_id: int = Field(None, alias="goodsId")
    goods_name: str = Field(None, alias="goodsName")
    goods_option_name: str = Field(None, alias="goodsOptionName")
    matter_codes: str = Field(None, alias="matterCodes")
    status: int = Field(None, alias="status")
