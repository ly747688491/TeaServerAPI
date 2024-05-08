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


class OperationLog(CoreModel):
    """
    操作日志表模型
    """
    request_modular = fields.CharField(max_length=255, null=True, description="请求模块")
    request_path = fields.TextField(null=True, description="请求路径")
    request_title = fields.CharField(max_length=50, null=True, default="", description="请求标题")
    business_type = fields.IntField(null=False, default=0, description="业务类型")
    method = fields.CharField(max_length=100, null=True, default="", description="请求方法")
    request_method = fields.CharField(max_length=10, null=True, default="", description="请求方式")
    oper_device = fields.CharField(max_length=20, null=True, default="", description="操作设备")
    oper_url = fields.CharField(max_length=255, null=True, default="", description="请求URL")
    oper_ip = fields.CharField(max_length=128, null=True, default="", description="操作IP地址")
    oper_location = fields.CharField(max_length=255, null=True, default="", description="操作地点")
    oper_param = fields.TextField(null=True, default="", description="请求参数")
    json_result = fields.TextField(null=True, default="", description="返回参数")
    status = fields.IntField(null=False, default=0, description="操作状态")
    error_msg = fields.TextField(null=True, default="", description="错误消息")

    class Meta:
        table = "sys_oper_log"
        table_description = "操作日志表"
        indexes = [
            ("business_type",),
            ("status",),
            ("create_time",),
        ]
