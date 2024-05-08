"""
@Project        ：tea_server_api 
@File           ：models.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:54 
@Description    ：
"""
from tortoise import fields

from cores.model import CoreModel


class Machine(CoreModel):
    unique_identifier = fields.CharField(max_length=32, null=False, default="", description="机器唯一标识")
    machine_name = fields.CharField(max_length=100, null=False, default="", description="机器名称")
    machine_address = fields.CharField(max_length=100, null=False, default="", description="机器地址")
    machine_type = fields.CharField(max_length=100, null=False, default="", description="机器类型")
    raspberry_ip = fields.CharField(max_length=100, null=False, default="", description="树莓派IP地址")
    raspberry_mac = fields.CharField(max_length=100, null=False, default="", description="树莓派MAC地址")
    machine_status = fields.CharField(max_length=100, null=False, default="", description="机器状态")

    class Meta:
        table = "machine_info"
        table_description = "机器信息表"


class Device(CoreModel):
    device_name = fields.CharField(max_length=100, null=False, default="", description="设备名称")
    machine = fields.ForeignKeyField('models.Machine', related_name='devices', null=True, on_delete=fields.SET_NULL,
                                     description="所属机器")
    device_type = fields.CharField(max_length=100, null=False, default="", description="设备类型（电机、机械臂、扫码器等）")
    gpio_pins = fields.JSONField(description="GPIO引脚配置")
    operational_status = fields.CharField(max_length=100, null=False, default="", description="设备运行状态")
    is_faulty = fields.BooleanField(default=False, description="是否故障")
    # 新增字段，用于关联当前物料
    current_material = fields.ForeignKeyField('models.Material', related_name='current_device', null=True,
                                              on_delete=fields.SET_NULL, description="当前关联的物料")

    class Meta:
        table = "machine_device"
        table_description = "设备信息表"


class Material(CoreModel):
    material_name = fields.CharField(max_length=100, null=False, default="", description="物料名称")
    material_quantity = fields.DecimalField(max_digits=10, decimal_places=2, null=False, default=0,
                                            description="物料数量")
    material_unit = fields.CharField(max_length=50, null=False, default="", description="物料单位（如升、克）")

    class Meta:
        table = "material_info"
        table_description = "物料信息表"


class DeviceMaterial(CoreModel):
    device = fields.ForeignKeyField('models.Device', related_name='material_links', on_delete=fields.CASCADE,
                                    description="关联设备")
    material = fields.ForeignKeyField('models.Material', related_name='device_links', on_delete=fields.CASCADE,
                                      description="关联物料")
    is_empty = fields.BooleanField(default=False, description="是否为空")

    class Meta:
        table = "device_material"
        table_description = "设备与物料关联关系表"
