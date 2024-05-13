"""
@Project        ：tea_server_api
@File           ：machine_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:34
@Description    ：
"""

from fastapi import APIRouter, Depends

from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, DetailResponseSchema, ResponseSchema
from modules.machine.service.machine_service import MachineService

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
