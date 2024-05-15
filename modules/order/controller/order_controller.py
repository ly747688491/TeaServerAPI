"""
@Project        ：tea_server_api
@File           ：order_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午11:33
@Description    ：
"""

from fastapi import APIRouter, Depends

from cores.rabbitmq import RabbitMQService
from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, ResponseSchema
from modules.order.entity.schemas import OrderListQuerySchema, OrderQuerySchema
from modules.order.service.order_service import OrderGoodsService

OrderRouter = APIRouter(prefix="/order", tags=["订单模块"])


@OrderRouter.post("/queued", response_model=CoreResponseSchema, summary="提交订单")
async def get_order(order_query: OrderListQuerySchema, order_service: OrderGoodsService = Depends()):
    # try:
    info = await order_service.get_order_goods(order_query)
    if info:
        RabbitMQService.send_message(queue_name=info.machine_id, message=info.material)
        # 返回正常响应
        result = ResponseSchema(code=200, msg="订单提交成功")
        return ResponseUtil.success(data=result)
    else:
        # 返回异常响应
        result = ResponseSchema(code=200, msg="订单提交失败")
        return ResponseUtil.error(data=result)

    # except Exception as e:
    #     # 返回异常响应
    #     result = ResponseSchema(code=200, msg=str(e))
    #     return ResponseUtil.error(data=result)
