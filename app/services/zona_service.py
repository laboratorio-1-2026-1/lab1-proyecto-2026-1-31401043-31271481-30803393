from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.zona_instalacion import ZonaInstalacion
from app.repositories.zona_instalacion import ZonaInstalacionRepository
from app.schemas.zona import ZonaCreate, ZonaUpdateEstado

class ZonaService:
    def __init__(self, db: AsyncSession):
        self.repo = ZonaInstalacionRepository(db)

    async def create_zona(self, schema: ZonaCreate) -> ZonaInstalacion:
        # Verificar si la zona ya existe por nombre
        zona_existente = await self.repo.get_by_nombre_zona(schema.nombre_zona)
        if zona_existente:
            raise AppException(
                detail="El nombre de la zona ya está registrado",
                error_code="ZONA_NAME_EXISTS",
                status_code=409
            )
        
        zona_data = schema.model_dump()
        return await self.repo.create(zona_data)
    
    async def update_zona_estado(self, id: int, schema: ZonaUpdateEstado) -> ZonaInstalacion:
        # Verificar si la zona existe
        zona = await self.repo.get_by_id(id)
        if not zona:
            raise NotFoundException(detail="Zona no encontrada", error_code="ZONA_NOT_FOUND")
        
        # Validar si el estado de la zona actual es igual al nuevo para evitar db call innecesario
        # o alguna otra validación de negocio específica aquí
        if zona.estado_zona == schema.estado_zona:
            return zona
            
        # Actualizar el estado de la zona
        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=zona, obj_in_data=update_data)

    async def list_zonas(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)
