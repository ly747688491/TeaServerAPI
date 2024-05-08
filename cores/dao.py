"""
@Project        ：tea_server_api
@File           ：dao.py
@IDE            ：PyCharm
@Author         ：李延
@Date           ：2024/5/7 下午5:56
@Description    ：
"""

from typing import Generic, Type, TypeVar, Optional, List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tortoise import Model

from cores.schema import PageResponseSchema

# 数据库orm模型
ModelType = TypeVar("ModelType", bound=Model)
# 基础模型
SchemaType = TypeVar("SchemaType", bound=BaseModel)
# 新增模型
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 修改模型
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# 查询模型
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


class BaseDao(
    Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]
):
    def __init__(self, model: Type[ModelType], schema_model: Type[SchemaType]):
        """
        初始化基础CRUD类，用于实现增删改查的默认方法。
        :param model: Tortoise ORM模型类。
        :param schema_model: Pydantic模型类。
        """
        self.model = model
        self.schema_model = schema_model

    async def create(self, schema: CreateSchemaType) -> SchemaType:
        """
        根据Pydantic模型创建数据库记录。
        """
        obj_data = jsonable_encoder(schema, exclude_unset=True)
        obj = await self.model.create(**obj_data)
        return self.schema_model.model_validate_json(obj)

    async def delete(self, schema: FilterSchemaType) -> int:
        """
        根据Pydantic模型删除符合条件的记录。
        """
        filter_data = jsonable_encoder(schema, exclude_unset=True)
        updated_count = await self.model.filter(**filter_data).update(is_deleted=True)
        return updated_count

    async def update(self, obj_id: str, schema: UpdateSchemaType) -> SchemaType:
        """
        根据ID和Pydantic模型更新记录。
        """
        obj = await self.model.get(id=obj_id)
        update_data = jsonable_encoder(schema, exclude_unset=True)
        await obj.update_from_dict(update_data)
        await obj.save()
        return self.schema_model.model_validate_json(obj)

    async def get(self, schema: FilterSchemaType) -> Optional[SchemaType]:
        """
        根据Pydantic模型查询单个记录，并返回Pydantic模型。
        """
        filter_data = schema.model_dump(exclude_unset=True)
        obj = await self.model.get_or_none(**filter_data, is_deleted=False)
        if obj:
            return self.schema_model.model_validate_json(obj)
        return None

    async def list(
            self, schema: FilterSchemaType, skip: int = 1, limit: int = 10
    ) -> List[SchemaType]:
        """
        根据Pydantic模型分页查询记录，并返回Pydantic模型列表。
        """
        filter_data = schema.model_dump(exclude_unset=True)
        query_set = (
            self.model.filter(**filter_data, is_deleted=False).offset(skip).limit(limit)
        )
        objs = await query_set.all()
        return [self.schema_model.model_validate_json(obj) for obj in objs]

    async def count(self, schema: FilterSchemaType) -> int:
        """
        根据Pydantic模型统计符合条件的记录数量。
        """
        filter_data = schema.model_dump(exclude_unset=True)
        count = await self.model.filter(**filter_data, is_deleted=False).count()
        return count

    async def exists(self, schema: FilterSchemaType) -> bool:
        """
        根据Pydantic模型检查符合条件的记录是否存在。
        """
        filter_data = schema.model_dump(exclude_unset=True)
        return await self.model.filter(**filter_data, is_deleted=False).exists()

    async def filter(self, schema: FilterSchemaType):
        """
        根据Pydantic模型过滤记录，返回QuerySet。
        """
        filter_data = schema.model_dump(exclude_unset=True)
        return self.model.filter(**filter_data, is_deleted=False)

    async def bulk_create(self, schemas: List[CreateSchemaType]) -> List[SchemaType]:
        """
        根据Pydantic模型列表批量创建记录，并返回Pydantic模型列表。
        """
        obj_data_list = [
            jsonable_encoder(schema, exclude_unset=True) for schema in schemas
        ]
        objs = await self.model.bulk_create(
            [self.model(**obj_data) for obj_data in obj_data_list]
        )
        return [self.schema_model.model_validate_json(obj) for obj in objs]

    async def bulk_update(self, schemas: List[UpdateSchemaType]) -> List[SchemaType]:
        """
        根据Pydantic模型列表批量更新记录，并返回Pydantic模型列表。
        """
        objs = []
        update_fields = set()
        for schema in schemas:
            obj_id = schema.id
            update_data = schema.model_dump(exclude_unset=True)
            obj = await self.model.get(id=obj_id)
            await obj.update_from_dict(update_data)
            objs.append(obj)
            update_fields.update(update_data.keys())
        await self.model.bulk_update(objs, fields=list(update_fields))
        return [self.schema_model.model_validate_json(obj) for obj in objs]

    async def paginate(
            self, schema: FilterSchemaType, page_num: int = 1, page_size: int = 10
    ):
        """
        根据Pydantic模型分页查询记录，并返回分页信息和Pydantic模型列表。
        """
        total_count = await self.count(schema)
        skip = (page_num - 1) * page_size
        objs = await self.list(schema, skip=skip, limit=page_size)
        has_next = total_count > skip + len(objs)
        return PageResponseSchema(
            total=total_count,
            page_num=page_num,
            page_size=page_size,
            data=objs,
            has_next=has_next
        )


def create_dao(model: Type[ModelType], schema_model: Type[SchemaType]) -> BaseDao:
    return BaseDao(model, schema_model)
