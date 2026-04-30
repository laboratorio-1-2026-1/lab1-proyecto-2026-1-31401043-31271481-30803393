from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.entrenador import Entrenador
from app.repositories.entrenador_repository import EntrenadorRepository
from app.repositories.usuario_repository import UsuarioRepository

from app.schemas.entrenador import EntrenadorCreate, EntrenadorUpdate, EntrenadorUpdateEstado

class EntrenadorService:
    def __init__(self, db: AsyncSession):
        self.repo = EntrenadorRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    async def create_entrenador(self, schema: EntrenadorCreate) -> Entrenador:
        # Verificar si el usuario existe
        existing_usuario = await self.usuario_repo.get_by_id(schema.usuario_id)
        if not existing_usuario:
            raise NotFoundException(detail="Usuario no encontrado", error_code="USER_NOT_FOUND")
        
        # Verificar si el entrenador con ese usuario exite
        existing_entrenador = await self.repo.get_by_usuario_id(schema.usuario_id)
        if existing_entrenador:
            raise AppException(detail="El entrenador ya existe", error_code="ENTRENADOR_ALREADY_EXISTS", status_code=409)
        
        rol_usuario = await self.usuario_repo.get_nombre_rol_by_usuario_id(schema.usuario_id)
        rol_usuario = rol_usuario.upper() if rol_usuario else None
        if rol_usuario != "ENTRENADOR":
            raise BusinessRuleException(detail="El usuario no es un entrenador", error_code="USER_NOT_ENTRENADOR")
        
        entrenador_data = schema.model_dump()
        # Crear el usuario
        return await self.repo.create(entrenador_data)
    
    async def update_entrenador(self, id: int, schema: EntrenadorUpdate) -> Entrenador:
        # Verificar si el entrenador existe
        entrenador = await self.repo.get_by_id(id)
        if not entrenador:
            raise NotFoundException(detail="Entrenador no encontrado", error_code="ENTRENADOR_NOT_FOUND")
        
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=entrenador, obj_in_data=update_data)
    
    async def delete_soft_entrenador(self, id: int, schema: EntrenadorUpdateEstado) -> Entrenador:
        # Verificar si el entrenador existe
        entrenador = await self.repo.get_by_id(id)
        if not entrenador:
            raise NotFoundException(detail="Entrenador no encontrado", error_code="ENTRENADOR_NOT_FOUND")
        
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=entrenador, obj_in_data=update_data)

    async def list_entrenadores(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)