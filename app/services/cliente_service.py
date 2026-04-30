from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteService:
    def __init__(self, db: AsyncSession):
        self.repo = ClienteRepository(db)
        self.usuario_repo = UsuarioRepository(db)

    async def create_cliente(self, schema: ClienteCreate) -> Cliente:
        # Verificar si el usuario existe
        existing_usuario = await self.usuario_repo.get_by_id(schema.usuario_id)
        if not existing_usuario:
            raise NotFoundException(detail="Usuario no encontrado", error_code="USER_NOT_FOUND")
        # Verificar si el cliente con ese usuario exite
        existing_cliente = await self.repo.get_by_usuario_id(schema.usuario_id)
        if existing_cliente:
            raise AppException(detail="El cliente ya existe", error_code="CLIENT_ALREADY_EXISTS", status_code=409)
        
        existing_cedula = await self.repo.get_by_cedula(schema.cedula)
        if existing_cedula:
            raise AppException(detail="La cédula ya está registrada", error_code="CEDULA_ALREADY_EXISTS", status_code=409)
        
        rol_usuario = await self.usuario_repo.get_nombre_rol_by_usuario_id(schema.usuario_id)
        rol_usuario = rol_usuario.upper() if rol_usuario else None
        if rol_usuario != "CLIENTE":
            raise BusinessRuleException(detail="El usuario no es un cliente", error_code="USER_NOT_CLIENT")
        
        cliente_data = schema.model_dump()
        # Crear el usuario
        return await self.repo.create(cliente_data)
    
    async def update_cliente(self, id: int, schema: ClienteUpdate) -> Cliente:
        # Verificar si el cliente existe
        cliente = await self.repo.get_by_id(id)
        if not cliente:
            raise NotFoundException(detail="Cliente no encontrado", error_code="CLIENT_NOT_FOUND")
        
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=cliente, obj_in_data=update_data)

    async def list_clientes(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)