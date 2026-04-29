from typing import Any, Generic, List, Optional, Type, TypeVar, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], db: AsyncSession):
        self.model = model_class
        self.db = db

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[dict] = None) -> Tuple[int, List[ModelType]]:
        # Método genérico para obtener todos los registros con paginación y filtros dinámicos.
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    if isinstance(value, str):
                        query = query.where(getattr(self.model, key).ilike(f"%{value}%"))
                    else:
                        query = query.where(getattr(self.model, key) == value)

        # Count query
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        query = query.offset(skip).limit(limit)
        results = await self.db.execute(query)
        return total, list(results.scalars().all())

    async def create(self, obj_in_data: dict) -> ModelType:
        # Método genérico para crear un nuevo registro.
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in_data: dict) -> ModelType:
        # Método genérico para actualizar un registro existente.
        for field in obj_in_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, obj_in_data[field])
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> ModelType:
        # Método genérico para eliminar un registro existente, 
        # no se utiliza en este proyecto pero se deja si surge la necesidad de hacerlo.
        obj = await self.get_by_id(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj
