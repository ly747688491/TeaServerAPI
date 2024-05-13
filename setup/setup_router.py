"""
@Project        ：tea_server_api
@File           ：setup_router.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 上午10:51
@Description    ：
"""

from fastapi import FastAPI

from modules.machine.controller.machine_controller import MachineRouter
from modules.order.controller.order_controller import OrderRouter

controller_list = [
    {"router": MachineRouter, "tag": "机器模块"},
    # {"router": OperRouter, "tag": "操作日志模块"},
    {"router": OrderRouter, "tag": "订单模块"},
    # {"router": AuthRouter, "tag": "认证模块"}
]


def setup_router(app: FastAPI):
    """注册路由"""
    for controller in controller_list:
        app.include_router(router=controller["router"], tags=controller.get("tags"))
