"""
@Project        ：tea_server_api 
@File           ：schema.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:09 
@Description    ：
"""
from datetime import datetime
from typing import Optional, List, TypeVar

from pydantic import BaseModel, ConfigDict, field_validator, Field
from pydantic.alias_generators import to_camel


class CoreSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[str] = None
    description: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    @classmethod
    @field_validator("createTime", "updateTime")
    def format_time(cls, value: datetime) -> str:
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")


class OnlyIdSchema(BaseModel):
    id: Optional[str] = None


class CorePageQuerySchema(BaseModel):
    page_num: int = 1
    page_size: int = 10
    begin_time: Optional[str] = None
    end_time: Optional[str] = None


class ResponseSchema(BaseModel):
    code: Optional[int] = 200
    msg: Optional[str] = "success"


dataT = TypeVar('dataT', bound=BaseModel)


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
