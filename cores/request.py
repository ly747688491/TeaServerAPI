"""
@Project        ：tea_server_api 
@File           ：request.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:59 
@Description    ：
"""
from datetime import datetime
from typing import Tuple

import requests
import user_agents
from fastapi import Request
from setup.setup_logger import logger
from starlette.datastructures import URL


class RequestService:
    def __init__(self, request: Request):
        self.request: Request = request
        self.user_agent = user_agents.parse(self.request.headers["user-agent"])  # 解析成user_agent

    def get_browser(self) -> str:
        """获取浏览器"""
        return self.user_agent.browser.family  # 判断是什么浏览器

    def get_os(self) -> str:
        """获取操作系统"""
        return self.user_agent.os.family

    def get_device(self) -> str:
        """获取设备类型"""
        return self.user_agent.device.family

    def get_host(self) -> str:
        """获取主机IP"""
        return self.request.client.host

    def get_port(self) -> int:
        """获取端口"""
        return self.request.client.port

    def get_ip_addr(self) -> str:
        """获取ip字符串"""
        host = self.request.client.host
        port = self.request.client.port
        return host + ":" + str(port)

    def get_oper_param(self) -> str:
        if hasattr(self.request, "_body"):
            return str(self.request._body)
        else:
            return self.request.url.query

    def get_params_time(self) -> Tuple:
        """是否有时间相关的查询参数"""
        query_params = self.request.query_params.items()
        start = None
        end = None
        for params in query_params:
            if params[0] == "params[beginTime]":
                start = datetime.strptime(params[1], "%Y-%m-%d")
            if params[0] == "params[endTime]":
                end = datetime.strptime(params[1], "%Y-%m-%d")
        return start, end

    def get_ip_location(self) -> str:
        """获取ip所属地"""
        location_str = "未知省市"
        try:
            url = "http://ip.taobao.com/outGetIpInfo"
            data = {
                "ip": self.get_host(),
                "accessKey": "alibaba-inc",
            }
            res = requests.post(url=url, data=data)
            res_dict = res.json()
            if res_dict["code"] == 0:
                location_str = res_dict["data"]["country"] + res_dict["data"]["region"] + res_dict["data"]["city"]
        except Exception as e:
            logger.error(e)
        finally:
            return location_str.lstrip("XXXX")

    def get_method(self) -> str:
        """请求方法"""
        return self.request.method

    def get_route_name(self) -> str:
        route = self.request.scope.get("route", None)
        if route:
            return route.name
        else:
            return ""

    def get_url(self) -> URL:
        """http://127.0.0.1:8001/dev-api/system/user/authRole/1"""
        return self.request.url

    def get_url_path(self) -> str:
        """'/dev-api/system/user/authRole/1'"""
        return self.request.url.path
