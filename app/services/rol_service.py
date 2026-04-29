from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rol import Rol
from app.repositories.base_repository import BaseRepository
from app.repositories.rol_repository import RolRepository


class RolService(BaseRepository[Rol]):
    def __init__(self, db: AsyncSession):
        self.repo = RolRepository(db)
    async def list_all(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)
