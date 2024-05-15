"""
@Project        ：tea_server_api
@File           ：order_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午11:33
@Description    ：
"""


# def get_config_dao():
#     return create_dao(model=OrderDetails, schema_model=OrderSchema)

from cores.schema import OnlyIdSchema
from modules.machine.entity.models import Machine
from modules.order.entity.models import OrderGoods
from modules.order.entity.schemas import OrderGoodsSchema, OrderListQuerySchema


class OrderGoodsService:
    def __init__(self):
        self.schema = OrderGoodsSchema
        self.model = OrderGoods

    async def get_order_goods(self, order_list: OrderListQuerySchema):
        """
        获取订单商品
        :param order_id:
        :return:
        """
        for order in order_list.order_list:
            order_data = await self.model.get_or_none(id=order.id)
            machine_data = await Machine.get_or_none(id=order.machine_id)
            if order_data and machine_data:
                pass
