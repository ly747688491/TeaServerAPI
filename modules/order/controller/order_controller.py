"""
@Project        ：tea_server_api
@File           ：order_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午11:33
@Description    ：
"""

from fastapi import APIRouter, Depends

from cores.dao import BaseDao
from cores.rabbitmq import RabbitMQService
from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, OnlyIdSchema, ResponseSchema
from modules.machine.service.machine_service import get_machine_dao
from modules.order.entity.schemas import OrderSchema
from modules.order.service.order_service import OrderService

OrderRouter = APIRouter(prefix="/order", tags=["订单模块"])


@OrderRouter.post("/", response_model=CoreResponseSchema, summary="提交订单")
async def get_order(order_info: OrderSchema, order_service: OrderService = Depends()):
    # try:
    info = await order_service.submit_order(order_info)
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
