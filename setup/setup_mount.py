"""
@Project        ：tea_server_api 
@File           ：setup_mount.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/8 上午10:51 
@Description    ：
"""
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config.setting import setting


def setup_mount(app: FastAPI):
    """挂载静态文件 -- https://fastapi.tiangolo.com/zh/tutorial/static-files/"""

    # 第一个参数为url路径参数, 第二参数为静态文件目录的路径, 第三个参数是FastAPI内部使用的名字
    app.mount(f"/{setting.STATIC_DIR}", StaticFiles(directory=setting.STATIC_DIR), name=setting.STATIC_DIR)
