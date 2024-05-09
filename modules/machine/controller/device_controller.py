"""
@Project        ：tea_server_api
@File           ：device_controller.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:34
@Description    ：
"""

from fastapi import APIRouter, Depends

from cores.dao import BaseDao
from cores.response import ResponseUtil
from cores.schema import CoreResponseSchema, DetailResponseSchema, OnlyIdSchema, ResponseSchema
from modules.machine.controller.material_controller import MaterialRouter
from modules.machine.entity.schemas import DevicePageQuerySchema, DeviceSchema
from modules.machine.service.device_service import get_device_dao
from setup.setup_logger import logger

DeviceRouter = APIRouter(prefix="/device", tags=["设备模块"])
DeviceRouter.include_router(MaterialRouter)


@DeviceRouter.get("/", response_model=CoreResponseSchema, summary="设备列表")
async def get_device_list(page_query: DevicePageQuerySchema, device_dao: BaseDao = Depends(get_device_dao)):
    """
    获取设备列表
    :param page_query:
    :param machine_dao:
    :return:
    """
    filter_params = DevicePageQuerySchema(
        **page_query.model_dump(exclude_unset=True, exclude={"page_size", "page_num"})
    )
    logger.info(f"获取设备列表，参数：{filter_params}")
    pagination = await device_dao.paginate(
        schema=filter_params, page_num=page_query.page_num, page_size=page_query.page_size
    )
    return ResponseUtil.success(pagination)


@DeviceRouter.get("/{device_id}", response_model=CoreResponseSchema, summary="获取单个设备信息")
async def get_machine_by_id(device_id: str, device_dao: BaseDao = Depends(get_device_dao)):
    """
    获取单个机器信息
    :param machine_id: 机器id
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    id_schema = OnlyIdSchema(id=device_id)
    try:
        device = await device_dao.get(id_schema)
        if device is None:
            no_exists_schema = DetailResponseSchema(msg="机器不存在", data=device, code=204)
            return ResponseUtil.failure(msg="机器不存在", data=no_exists_schema)
        device_schema = DetailResponseSchema(msg="获取机器成功", data=device, code=200)
        return ResponseUtil.success(data=device_schema)
    except Exception as e:
        logger.error(f"get machine by id error: {e}")
        error_data = ResponseSchema(code=500, msg=f"get machine by id error: {e}")
        return ResponseUtil.error(data=error_data)


@DeviceRouter.post("/", response_model=CoreResponseSchema, summary="创建设备")
async def create_machine(device_create: DeviceSchema, device_dao: BaseDao = Depends(get_device_dao)):
    try:
        device = await device_dao.create(device_create)
        result = DetailResponseSchema(data=device)
        return ResponseUtil.success(msg="创建机器成功", data=result)
    except Exception as e:
        logger.error(f"create machine error: {e}")
        error_data = ResponseSchema(code=500, msg=f"create machine error: {e}")
        return ResponseUtil.error(data=error_data)


@DeviceRouter.put("/{device_id}", response_model=CoreResponseSchema, summary="更新设备")
async def update_machine(device_id: str, device_update: DeviceSchema, device_dao: BaseDao = Depends(get_device_dao)):
    """
    更新机器信息
    :param machine_id: 机器id
    :param machine_update: 机器信息更新模型
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    device = await device_dao.update(device_id, device_update)
    if device is None:
        return ResponseUtil.failure(msg="机器不存在")
    result = DetailResponseSchema(data=device)
    return ResponseUtil.success(data=result)


@DeviceRouter.delete("/{machine_id}", response_model=CoreResponseSchema, summary="删除设备")
async def delete_machine(device_id: str, device_dao: BaseDao = Depends(get_device_dao)):
    """
    删除机器信息
    :param machine_id: 机器id
    :param machine_dao: 机器信息数据访问对象
    :return:
    """
    device_delete = OnlyIdSchema(id=device_id)
    device_count = await device_dao.delete(device_delete)
    if device_count == 0:
        return ResponseUtil.failure(msg="机器不存在")
    return ResponseUtil.success(msg="删除机器成功")
