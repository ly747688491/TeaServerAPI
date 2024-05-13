"""
@Project        ：tea_server_api
@File           ：schema.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午10:09
@Description    ：
"""

from datetime import datetime
from typing import List, Optional, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel


class OnlyIdSchema(BaseModel):
    id: Optional[str | int] = None


class CorePageQuerySchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, extra="forbid")
    page_num: int = 1
    page_size: int = 10


class ResponseSchema(BaseModel):
    code: Optional[int] = 200
    msg: Optional[str] = "success"


dataT = TypeVar("dataT", bound=BaseModel)


class PageResponseSchema(ResponseSchema):
    data: Optional[List[dataT]] = Field(None, description="数据列表")
    total: Optional[int] = Field(0, description="数据总数")
    page_num: Optional[int] = Field(1, description="当前页码")
    page_size: Optional[int] = Field(10, description="每页数据大小")
    has_next: Optional[bool] = Field(False, description="是否有下一页")


class DetailResponseSchema(ResponseSchema):
    data: Optional[dataT] = Field(None, description="数据详情")


class CoreResponseSchema(BaseModel):
    code: Optional[int] = 200
    msg: Optional[str] = "success"
    success: Optional[bool] = True
    data: Optional[PageResponseSchema | DetailResponseSchema | ResponseSchema] = None
