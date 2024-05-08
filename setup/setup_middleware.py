"""
@Project        ：tea_server_api 
@File           ：setup_middleware.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:51 
@Description    ：
"""
import time
from typing import Callable

from fastapi import Depends, FastAPI, Request, Response

from modules.system.service.operation_service import OperationService
from setup.setup_logger import logger


def setup_middleware(app: FastAPI):
    """请求拦截与响应拦截 -- https://fastapi.tiangolo.com/tutorial/middleware/"""

    @app.middleware("http")
    async def logger_request(
            request: Request, call_next: Callable,
            operation_service: OperationService = Depends(OperationService)
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()
        logger.debug(
            f"{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}s"
        )

        # 将日志记录任务委托给 OperationService
        if response.media_type == "application/json":  # 检查响应类型
            await operation_service.log_oper(request, response)
            pass
        return response
