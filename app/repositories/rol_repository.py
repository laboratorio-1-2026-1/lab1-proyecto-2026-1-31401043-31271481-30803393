from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rol import Rol
from app.repositories.base_repository import BaseRepository

class RolRepository(BaseRepository[Rol]):
    def __init__(self, db: AsyncSession):
        super().__init__(Rol, db)