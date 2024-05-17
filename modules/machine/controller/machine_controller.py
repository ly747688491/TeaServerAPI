"""
@Project        ：tea_server_api
@File           ：machine_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:34
@Description    ：
"""


from fastapi import APIRouter, Depends

from cores.dao import BaseDao
from cores.rabbitmq import RabbitMQService
from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, DetailResponseSchema, OnlyIdSchema, ResponseSchema
from modules.machine.entity.schemas import MachineSchema
from modules.machine.service.machine_service import MachineService, get_machine_dao
from setup.setup_logger import logger

MachineRouter = APIRouter(prefix="/machine", tags=["机器模块"])


@MachineRouter.get("/all/{machine_id}", response_model=CoreResponseSchema, summary="获取机器详情")
async def get_machine_all_by_id(machine_id: str, machine_service: MachineService = Depends()):
    """
    根据机器id获取机器详情
    :param machine_id: 机器id
    :param machine_service: 机器服务
    :return:
    """
    machine = await machine_service.get_machine_all_info(machine_id)
    if machine is None:
        result = ResponseSchema(code=404, msg="机器不存在")
        return ResponseUtil.failure(msg="机器不存在", data=result)
    result = DetailResponseSchema(data=machine)
    return ResponseUtil.success(data=result)


@MachineRouter.get("/{machine_id}", response_model=CoreResponseSchema, summary="获取机器详情")
async def get_machine_by_id(machine_id: str, machine_dao: BaseDao = Depends(get_machine_dao)):
    """
    根据机器id获取机器详情
    :param machine_id: 机器id
    :param machine_dao: 机器dao
    :return:
    """
    try:
        machine_schema = MachineSchema(machine_code=machine_id)
        if machine := await machine_dao.get(machine_schema):
            result = DetailResponseSchema(data=machine)
            return ResponseUtil.success(data=result)
        else:
            result = DetailResponseSchema(data=None, code=404, msg="机器不存在")
            return ResponseUtil.failure(data=result)
    except Exception as e:
        result = ResponseSchema(code=500, msg=e.args[0])
        return ResponseUtil.error(data=result)


@MachineRouter.post("/clear/{machine_id}", response_model=CoreResponseSchema, summary="清洗机器")
async def clear_machine(machine_id: str, device_list: list[OnlyIdSchema], machine_service: MachineService = Depends()):
    """
    清洗机器
    :param machine_id: 机器id
    :param machine_service: 机器服务
    :return:
    """
    logger.info(f"清洗机器: {machine_id}")
    logger.info(f"清洗设备: {device_list}")
    result = await machine_service.get_device_list(machine_id, device_list)
    RabbitMQService.send_message(queue_name=machine_id, message=device_list)
    return ResponseUtil.success()
