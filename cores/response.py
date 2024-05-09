"""
@Project        ：tea_server_api
@File           ：response.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:59
@Description    ：
"""

from typing import Union

from starlette.responses import JSONResponse

from cores.schema import (
    CoreResponseSchema,
    DetailResponseSchema,
    PageResponseSchema,
    ResponseSchema,
)


class ResponseUtil:
    """
    Response utility class to standardize API responses.
    """

    @classmethod
    def success(
        cls,
        code: int = 200,
        msg: str = "操作成功",
        data: Union[DetailResponseSchema, PageResponseSchema, ResponseSchema] = None,
    ) -> JSONResponse:
        response = CoreResponseSchema(data=data)
        return JSONResponse(content=response.model_dump(), status_code=200)

    @classmethod
    def error(
        cls,
        data: ResponseSchema,
        code: int = 200,
        msg: str = "接口异常",
    ) -> JSONResponse:
        response = CoreResponseSchema(msg=msg, success=True, data=data)
        return JSONResponse(content=response.model_dump(), status_code=code)

    @classmethod
    def failure(cls, code: int = 200, msg: str = "操作失败", data: Union[ResponseSchema] = None) -> JSONResponse:
        response = CoreResponseSchema(msg=msg, data=data)
        return JSONResponse(content=response.model_dump(), status_code=code)

    @classmethod
    def unauthorized(cls, code: int = 401, msg: str = "认证失效，访问系统资源失败") -> JSONResponse:
        response = CoreResponseSchema(msg=msg, data=None)
        return JSONResponse(content=response.model_dump(), status_code=code)
