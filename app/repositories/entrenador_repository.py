from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entrenador import Entrenador
from app.repositories.base_repository import BaseRepository

class EntrenadorRepository(BaseRepository[Entrenador]):
    def __init__(self, db: AsyncSession):
        super().__init__(Entrenador, db)
    
    async def get_by_usuario_id(self, usuario_id: int) -> Entrenador | None:
        result = await self.db.execute(
            select(Entrenador).where(Entrenador.usuario_id == usuario_id)
        )
        return result.scalars().first()

    