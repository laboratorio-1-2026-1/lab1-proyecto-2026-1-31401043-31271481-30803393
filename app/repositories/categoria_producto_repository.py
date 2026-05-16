from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categoria_producto import CategoriaProducto
from app.repositories.base_repository import BaseRepository


class CategoriaProductoRepository(BaseRepository[CategoriaProducto]):
    def __init__(self, db: AsyncSession):
        super().__init__(CategoriaProducto, db)

    async def get_by_nombre(self, nombre: str) -> CategoriaProducto | None:
        #Busca una categoría por nombre (insensible a mayúsculas) para validar unicidad
        result = await self.db.execute(
            select(self.model).where(self.model.nombre_categoria.ilike(nombre))
        )
        return result.scalars().first()