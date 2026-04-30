from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.zona_instalacion import ZonaInstalacion
from app.repositories.base_repository import BaseRepository

class ZonaInstalacionRepository(BaseRepository[ZonaInstalacion]):
    def __init__(self, db: AsyncSession):
        super().__init__(ZonaInstalacion, db)
        
    async def get_by_nombre_zona(self, nombre_zona: str) -> ZonaInstalacion | None:
        result = await self.db.execute(select(self.model).where(self.model.nombre_zona.ilike(nombre_zona)))
        return result.scalars().first()