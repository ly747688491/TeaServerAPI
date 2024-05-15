"""
@Project        ：tea_server_api
@File           ：models.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:54
@Description    ：
"""

from tortoise import Model, fields


class OrderGoods(Model):
    id = fields.IntField(pk=True)
    machine_id = fields.IntField(null=True, source_field="machineId")
    order_id = fields.IntField(null=True, source_field="orderId")
    device_goods_id = fields.IntField(null=True, source_field="deviceGoodsId")
    device_goods_option_id = fields.IntField(null=True, source_field="deviceGoodsOptionId")
    goods_id = fields.IntField(null=True, source_field="goodsId")
    goods_name = fields.CharField(max_length=100, null=True, source_field="goodsName")
    goods_option_name = fields.CharField(max_length=255, null=True, source_field="goodsOptionName")
    matter_codes = fields.CharField(max_length=255, null=True, source_field="matterCodes")
    status = fields.IntField(null=True)

    class Meta:
        table = "db_order_goods"
        table_description = "订单信息表"
