"""
@Project        ：tea_server_api 
@File           ：schemas.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:54 
@Description    ：
"""
from typing import Optional

from pydantic import BaseModel

from cores.schema import CoreSchema


class OperationLogSchema(BaseModel):
    """
    操作日志表对应pydantic模型
    """
    request_modular: Optional[str]
    request_path: Optional[str]
    request_title: Optional[str]
    business_type: Optional[int]
    method: Optional[str]
    request_method: Optional[str]
    oper_device: Optional[str]
    oper_url: Optional[str]
    oper_ip: Optional[str]
    oper_location: Optional[str]
    oper_param: Optional[str]
    json_result: Optional[str]
    status: Optional[int]
    error_msg: Optional[str]


class OperPageQuerySchema(BaseModel):
    """
    操作日志表分页查询对应pydantic模型
    """
    page_num: int = 1
    page_size: int = 10
    begin_time: Optional[str] = None
    end_time: Optional[str] = None
    request_modular: Optional[str] = None
    method: Optional[str] = None
    request_method: Optional[str] = None
    status: Optional[int] = None


class OperDetailSchema(CoreSchema, OperationLogSchema):
    """
    操作日志表创建或更新对应pydantic模型
    """
    pass
