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


class MachineSchema(BaseModel):
    """
    机器创建更新模型
    """
    unique_identifier: Optional[str]
    machine_name: Optional[str]
    machine_address: Optional[str]
    machine_type: Optional[str]
    raspberry_ip: Optional[str]
    raspberry_mac: Optional[str]
    machine_status: Optional[str]


class MachineDetailSchema(MachineSchema, CoreSchema):
    """
    机器详情模型
    """
    pass


class DeviceSchema(BaseModel):
    """
    设备创建更新模型
    """
    device_name: Optional[str]
    machine: Optional[str]
    device_type: Optional[str]
    operational_status: Optional[str]
    gpio_pins: Optional[str]
    current_material: Optional[str]
    is_faulty: Optional[bool]


class DeviceDetailSchema(DeviceSchema, CoreSchema):
    """
    设备详情模型
    """
    pass


class MaterialSchema(BaseModel):
    """
    物料基础模型
    """
    material_name: Optional[str]
    material_quantity: Optional[str]
    material_unit: Optional[str]


class MaterialDetailSchema(MaterialSchema, CoreSchema):
    """
    物料详情模型
    """
    pass


class DeviceMaterialSchema(BaseModel):
    """
    设备物料关联模型
    """
    device: Optional[str]
    material: Optional[str]
    is_empty: Optional[bool]


class DeviceMaterialDetailSchema(DeviceMaterialSchema, CoreSchema):
    """
    设备物料关联详情模型
    """
    pass
