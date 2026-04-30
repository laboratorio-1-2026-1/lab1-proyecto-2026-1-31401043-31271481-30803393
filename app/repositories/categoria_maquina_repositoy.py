from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categoria_maquina import CategoriaMaquina
from app.repositories.base_repository import BaseRepository

class CategoriaMaquinaRepository(BaseRepository[CategoriaMaquina]):
    def __init__(self, db: AsyncSession):
        super().__init__(CategoriaMaquina, db)
    async def get_by_name(self, nombre: str) -> CategoriaMaquina:
        # Busca una categoría por nombre (insensible a mayúsculas)
        result = await self.db.execute(
            select(CategoriaMaquina).where(func.lower(CategoriaMaquina.nombre_categoria) == nombre.lower())
        )
        return result.scalars().first()    