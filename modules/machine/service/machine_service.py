"""
@Project        ：tea_server_api
@File           ：machine_service.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/8 下午1:28
@Description    ：
"""

from cores.dao import create_dao
from modules.machine.entity.models import Machine
from modules.machine.entity.schemas import DeviceSchema, MachineDetailSchema, MachineSchema


def get_machine_dao():
    return create_dao(model=Machine, schema_model=MachineSchema)


class MachineService:
    def __init__(self):
        self.machine_dao = get_machine_dao()
        self.machine_schema = MachineSchema
        self.machine_model = Machine

    async def get_machine_all_info(self, machine_id: str):
        """
        获取机器所有信息
        :param machine_id:
        :return:
        """
        try:
            if machine_info := await self.machine_model.get(machine_code=machine_id, status=1).prefetch_related(
                "devices"
            ):
                machine_data = MachineSchema.model_validate(machine_info.__dict__)
                devices_data = self._get_devices_for_machine(machine_info)
                machine_detail = MachineDetailSchema(**machine_data.model_dump(), devices=devices_data)
                return machine_detail
        except Exception as e:
            print(e)
            return None

    def _get_devices_for_machine(self, machine: Machine):
        devices = machine.devices
        return [DeviceSchema.model_validate(device.__dict__) for device in devices]
