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
from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, DetailResponseSchema, OnlyIdSchema, ResponseSchema
from modules.machine.controller.device_controller import DeviceRouter
from modules.machine.entity.schemas import MachinePageQuerySchema, MachineSchema
from modules.machine.service.machine_service import get_machine_dao
from setup.setup_logger import logger

MachineRouter = APIRouter(prefix="/machine", tags=["机器模块"])
MachineRouter.include_router(DeviceRouter)


@MachineRouter.get("/", response_model=CoreResponseSchema, summary="批量获取机器信息")
async def get_machine_page(page_query: MachinePageQuerySchema, machine_dao: BaseDao = Depends(get_machine_dao)):
    """
    批量获取机器信息
    :param page_query: 机器信息分页查询模型
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    filter_schema = MachinePageQuerySchema(
        **page_query.model_dump(
            exclude_unset=True,
            exclude={
                "page_size",
                "page_num",
            },
        )
    )
    logger.info(f"filter_schema: {filter_schema}")

    pagination = await machine_dao.paginate(
        schema=filter_schema,
        page_num=page_query.page_num,
        page_size=page_query.page_size,
    )
    return ResponseUtil.success(data=pagination)


@MachineRouter.get("/{machine_id}", response_model=CoreResponseSchema, summary="获取单个机器信息")
async def get_machine_by_id(machine_id: str, machine_dao: BaseDao = Depends(get_machine_dao)):
    """
    获取单个机器信息
    :param machine_id: 机器id
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    id_schema = OnlyIdSchema(id=machine_id)
    try:
        machine = await machine_dao.get(id_schema)
        if machine is None:
            no_exists_schema = DetailResponseSchema(msg="机器不存在", data=machine, code=204)
            return ResponseUtil.failure(msg="机器不存在", data=no_exists_schema)
        machine_schema = DetailResponseSchema(msg="获取机器成功", data=machine, code=200)
        return ResponseUtil.success(data=machine_schema)
    except Exception as e:
        logger.error(f"get machine by id error: {e}")
        error_data = ResponseSchema(code=500, msg=f"get machine by id error: {e}")
        return ResponseUtil.error(data=error_data)


@MachineRouter.post("/", response_model=CoreResponseSchema, summary="创建机器")
async def create_machine(machine_create: MachineSchema, machine_dao: BaseDao = Depends(get_machine_dao)):
    try:
        machine = await machine_dao.create(machine_create)
        result = DetailResponseSchema(data=machine)
        return ResponseUtil.success(msg="创建机器成功", data=result)
    except Exception as e:
        logger.error(f"create machine error: {e}")
        error_data = ResponseSchema(code=500, msg=f"create machine error: {e}")
        return ResponseUtil.error(data=error_data)


@MachineRouter.put("/{machine_id}", response_model=CoreResponseSchema, summary="更新机器")
async def update_machine(
    machine_id: str, machine_update: MachineSchema, machine_dao: BaseDao = Depends(get_machine_dao)
):
    """
    更新机器信息
    :param machine_id: 机器id
    :param machine_update: 机器信息更新模型
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    machine = await machine_dao.update(machine_id, machine)
    if machine is None:
        return ResponseUtil.failure(msg="机器不存在")
    result = DetailResponseSchema(data=machine)
    return ResponseUtil.success(data=result)


@MachineRouter.delete("/{machine_id}", response_model=CoreResponseSchema, summary="删除机器")
async def delete_machine(machine_id: str, machine_dao: BaseDao = Depends(get_machine_dao)):
    """
    删除机器信息
    :param machine_id: 机器id
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    machine_delete = OnlyIdSchema(id=machine_id)
    machine_count = await machine_dao.delete(machine_delete)
    if machine_count == 0:
        return ResponseUtil.failure(msg="机器不存在")
    return ResponseUtil.success(msg="删除机器成功")
