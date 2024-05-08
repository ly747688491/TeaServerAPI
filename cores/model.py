"""
@Project        ：tea_server_api 
@File           ：model.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:09 
@Description    ：
"""
from tortoise import Model, fields

from utils.common_utils import generate_id


class CoreModel(Model):
    """
    CoreModel 核心数据库模型
    """
    id = fields.CharField(pk=True, default=generate_id, max_length=15, nullable=False, description="主键")
    description = fields.CharField(max_length=255, nullable=True, default="", comment="描述")
    create_time = fields.DatetimeField(auto_now_add=True, describe="创建时间", source_field="create_time", null=True)
    updateTime = fields.DatetimeField(source_field="update_time", auto_now=True, null=True, describe="更新时间")
    is_deleted = fields.BooleanField(default=False, null=True, describe="是否删除")

    def to_dict(self):  # 这个方法自定义的时候使用
        data = {i: getattr(self, i) for i in self.__dict__ if not i.startswith('_')}
        return data

    class Meta:
        abstract = True