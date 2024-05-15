"""
@Project        ：tea_server_api
@File           ：schemas.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class MachineSchema(BaseModel):
    """
    机器创建更新模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(None, alias="id")
    name: Optional[str] = Field(None, alias="name")
    machine_code: Optional[str] = Field(None, alias="machine_code")
    status: Optional[int] = Field(None, alias="status")
    sort: Optional[int] = Field(None, alias="sort")
    raspberry_ip: Optional[str] = Field(None, alias="raspberry_ip")
    raspberry_mac: Optional[str] = Field(None, alias="raspberry_mac")


class DeviceSchema(BaseModel):
    """
    设备创建更新模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(None, alias="id")
    name: Optional[str] = Field(None, alias="name")
    machine_id: Optional[int] = Field(None, alias="machine_id")
    type: Optional[int] = Field(None, alias="type")
    status: Optional[int] = Field(None, alias="status")
    config: Optional[dict] = Field(None, alias="config")
    matter_code: Optional[str] = Field(None, alias="matter_code")
    stock: Optional[int] = Field(None, alias="stock")
    sort: Optional[int] = Field(None, alias="sort")


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
