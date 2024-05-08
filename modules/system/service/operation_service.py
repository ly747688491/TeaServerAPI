"""
@Project        ：tea_server_api 
@File           ：operation_service.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午11:11 
@Description    ：
"""
from fastapi import Request, Depends
from orjson import orjson
from starlette.responses import StreamingResponse

from cores.dao import BaseDao, create_dao
from modules.system.entity.models import OperationLog
from modules.system.entity.schemas import OperationLogSchema
from setup.setup_logger import logger


def get_oper_dao():
    return create_dao(model=OperationLog, schema_model=OperationLogSchema)


class OperationService():

    @classmethod
    async def log_oper(cls, request: Request, response: StreamingResponse, oper_dao: BaseDao = Depends(get_oper_dao)):
        oper_log_sch = request.scope.get("oper_log_json", None)
        if oper_log_sch:
            try:
                result = await response.body()
                result_dict = orjson.loads(result)
                oper_log_sch = OperationLogSchema(
                    request_modular=request.url.path,
                    request_path=str(request.url),
                    status="0" if response.status_code == 200 else "1",
                    errorMsg=result_dict.get("msg", "") if result_dict.get("code", 200) != 200 else "",
                    json_result=result,
                )
                await oper_dao.create(oper_log_sch)
            except Exception as e:
                logger.error(f"Failed to log operation: {e}")
        else:
            return response
