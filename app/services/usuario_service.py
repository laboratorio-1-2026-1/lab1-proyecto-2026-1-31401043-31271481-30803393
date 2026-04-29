from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.repositories.rol_repository import RolRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.repo = UsuarioRepository(db)
        self.rol_repo = RolRepository(db)

    async def create_usuario(self, schema: UsuarioCreate) -> Usuario:
        # Verificar si el correo ya existe
        existing_usuario = await self.repo.get_by_email(schema.email)
        if existing_usuario:
            raise AppException(detail="El correo ya está registrado", error_code="EMAIL_ALREADY_EXISTS", status_code=409)

        # Verificar si el rol existe
        rol = await self.rol_repo.get_by_id(schema.rol_id)
        if not rol:
            raise NotFoundException(detail="Rol no encontrado", error_code="ROL_NOT_FOUND")
        
        password_hash= get_password_hash(schema.password)
        user_data = schema.model_dump()
        user_data.pop("password")
        user_data["password_hash"] = password_hash
        # Crear el usuario
        return await self.repo.create(user_data)
    
    async def get_by_id(self, id: int) -> Usuario:
        user = await self.repo.get_by_id_with_relations(id)
        if not user:
            raise NotFoundException("User not found", "USER_NOT_FOUND")
        return user
    async def update_usuario(self, id: int, schema: UsuarioUpdate) -> Usuario:
        # Verificar si el usuario existe
        usuario = await self.repo.get_by_id(id)
        if not usuario:
            raise NotFoundException(detail="Usuario no encontrado", error_code="USER_NOT_FOUND")
        
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=usuario, obj_in_data=update_data)

    async def list_usuarios(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)