from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.disciplina import Disciplina
from app.repositories.base_repository import BaseRepository


class DisciplinaRepository(BaseRepository[Disciplina]):
    def __init__(self, db: AsyncSession):
        super().__init__(Disciplina, db)

    async def get_by_nombre_disciplina(self, nombre: str) -> Disciplina | None:
        # Busca una disciplina por nombre exacto (insensible a mayúsculas) para validar unicidad
        result = await self.db.execute(
            select(self.model).where(self.model.nombre_disciplina.ilike(nombre))
        )
        return result.scalars().first()
