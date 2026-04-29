from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rol import Rol
from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: AsyncSession):
        super().__init__(Usuario, db)

    async def get_by_email(self, email: str) -> Usuario:
        result = await self.db.execute(
            select(Usuario).where(Usuario.email == email)
        )
        return result.scalars().first()
    from sqlalchemy import select

    async def get_nombre_rol_by_usuario_id(self, usuario_id: int):
        result = await self.db.execute(
            select(Rol.nombre) # Queremos el nombre de la tabla Rol
            .join(Usuario, Usuario.rol_id == Rol.id) # Unimos las tablas
            .where(Usuario.id == usuario_id)
        )
        return result.scalars().first()
    
    async def get_by_email_with_relations(self, email: str) -> Usuario | None:
        result = await self.db.execute(
            select(Usuario)
            .options(
            selectinload(Usuario.rol),  
            selectinload(Usuario.cliente),  
            selectinload(Usuario.entrenador),
            )
            .filter(Usuario.email == email)
        )
        return result.scalars().first()
    