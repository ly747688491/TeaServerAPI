"""
@Project        ：tea_server_api 
@File           ：security.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:59 
@Description    ：
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from config.setting import setting

get_token = OAuth2PasswordBearer(tokenUrl=f"{setting.API_PREFIX}/auth")


def get_expires() -> datetime:
    """获取过期时间"""
    return datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict, expires: Optional[datetime] = None) -> str:
    """
    生成token
    :param expires: 过期时间
    :param data: 存储数据
    :return: 加密后的token
    """
    to_encode = data.copy()
    if not expires:
        expires = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
