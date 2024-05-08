"""
@Project        ：tea_server_api 
@File           ：exceptions.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:56 
@Description    ：
"""


class LoginException(Exception):
    """
    自定义登录异常LoginException
    """

    def __init__(self, data: str = None, message: str = "用户名、密码、验证码错误或token失效"):
        self.data = data
        self.message = message


class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, data: str = None, message: str = "访问令牌失败"):
        self.data = data
        self.message = message


class PermissionException(Exception):
    """
    自定义权限异常PermissionException
    """

    def __init__(self, data: str = None, message: str = "权限不足,拒绝访问"):
        self.data = data
        self.message = message


class CommonException(Exception):
    """操作异常"""

    def __init__(self, message: str = "操作异常"):
        self.message = message


class DataNotExist(Exception):
    """存在异常"""

    def __init__(self, err_desc: str = "数据不存在"):
        self.message = err_desc
