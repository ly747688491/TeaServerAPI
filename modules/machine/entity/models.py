"""
@Project        ：tea_server_api
@File           ：models.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from tortoise import Model, fields

from cores.model import CoreModel


class Machine(Model):
    id = fields.IntField(pk=True, source_field="id")
    name = fields.CharField(max_length=255, source_field="name")
    sort = fields.IntField(null=True, source_field="sort")
    status = fields.IntField(null=True, source_field="status")
    machine_code = fields.CharField(max_length=50, source_field="machineCode")
    raspberry_ip = fields.CharField(max_length=100, null=True, source_field="raspberry_ip")
    raspberry_mac = fields.CharField(max_length=100, source_field="raspberry_mac")

    devices = fields.ReverseRelation["Device"]

    class Meta:
        table = "db_machine"
        table_description = "机器信息表"


class Device(Model):
    id = fields.IntField(pk=True, source_field="id")
    machine = fields.ForeignKeyField("models.Machine", related_name="devices", source_field="machineId")
    name = fields.CharField(max_length=50, null=True, source_field="name")
    matter_code = fields.CharField(max_length=255, source_field="matterCode")
    type = fields.IntField(null=True, source_field="type")
    config = fields.JSONField(null=True, source_field="config")
    stock = fields.IntField(source_field="stock")
    status = fields.IntField(null=True, source_field="status")
    sort = fields.IntField(null=True, source_field="sort")

    class Meta:
        table = "db_machine_device"
        table_description = "设备信息表"
