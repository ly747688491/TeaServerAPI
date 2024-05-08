"""
@Project        ：tea_server_api 
@File           ：setup_cors.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:50 
@Description    ：
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.setting import setting


def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in setting.CORS_ORIGINS],  # 允许访问的源
        # allow_origins=["*"],  # 允许访问的源
        allow_credentials=True,  # 支持 cookie
        allow_methods=("GET", "POST", "PUT", "DELETE"),  # 允许使用的请求方法
        allow_headers=("*", "Authorization"),  # 允许携带的 Headers
    )
