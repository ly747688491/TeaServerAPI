"""
@Project        ：tea_server_api 
@File           ：redis.py
@IDE            ：PyCharm 
@Author         ：李延
@Date           ：2024/5/7 下午5:58 
@Description    ：
"""
from datetime import datetime

from aioredis import Redis

from schemas.machine import VerifyMachineSchema


def get_tokens_key(uuid: str) -> str:
    """# 检验机器 redis key"""
    return "machine_tokens:" + uuid


def get_command_codes_key(uuid: str) -> str:
    """# 参数管理 cache key"""
    return "command_codes:" + uuid


class RedisService(Redis):
    """继承Redis,并添加自己的方法"""

    def get_cmdstat_list(self, cmdstat_dict):
        cmdstat_list = []
        for key, value in cmdstat_dict.items():
            name = key.split("_")[-1]
            val = str(value["calls"])
            cmdstat_list.append({"name": name, "value": val})
        return cmdstat_list

    async def save_verify_tokens(self, id: str, token: str, expireTime: int):
        """# 保存机器验证token"""

        verify_machine_sh = VerifyMachineSchema(
            machine_id=id,
            token=token,
            expireTime=expireTime,
        )

        ex = expireTime - int(datetime.utcnow().timestamp())
        await self.set(get_tokens_key(id), verify_machine_sh.model_dump_json(exclude_none=True), ex=ex)
