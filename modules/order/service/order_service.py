"""
@Project        ：tea_server_api
@File           ：order_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午11:33
@Description    ：
"""

from cores.dao import BaseDao, create_dao
from cores.schema import OnlyIdSchema
from modules.machine.entity.models import Machine
from modules.machine.service.machine_service import get_machine_dao
from modules.order.entity.models import OrderDetails
from modules.order.entity.schemas import OrderSchema


def get_config_dao():
    return create_dao(model=OrderDetails, schema_model=OrderSchema)


class OrderService:
    def __init__(self):
        self.schema = OrderSchema

    async def submit_order(self, order_data: OrderSchema):
        """
        提交订单
        :param order_data:
        :param machine_dao:
        :return:
        """
        try:
            id_schema = OnlyIdSchema(id=order_data.machine_id)
            filter_data = id_schema.model_dump(exclude_unset=True)
            obj = await Machine.get_or_none(**filter_data, status=1)
            if obj is None:
                return None
            order_data.machine_id = obj.machine_code
            return order_data
        except Exception as e:
            print(e)
            return None
