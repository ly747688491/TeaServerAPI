"""
@Project        ：tea_server_api
@File           ：schemas.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MachineSchema(BaseModel):
    """
    机器创建更新模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = None
    name: Optional[str]
    machine_code: Optional[str] = None
    status: Optional[int]
    sort: Optional[int]
    raspberry_ip: Optional[str] = None
    raspberry_mac: Optional[str] = None


class DeviceSchema(BaseModel):
    """
    设备创建更新模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = None
    name: Optional[str] = None
    machine_id: Optional[int]
    type: Optional[int]
    status: Optional[int]
    config: Optional[dict] = None
    matter_code: Optional[str]
    stock: Optional[int]
    sort: Optional[int] = None


class VerifyMachineSchema(BaseModel):
    id: str = None
    token: Optional[str] = None
    expireTime: Optional[int] = None  # 过期时间


class AuthMachine(BaseModel):
    id: Optional[str] = None
    unique_identifier: Optional[str] = None


class MachineDetailSchema(MachineSchema):
    """
    机器详情模型
    """

    devices: Optional[List[DeviceSchema]] = None
