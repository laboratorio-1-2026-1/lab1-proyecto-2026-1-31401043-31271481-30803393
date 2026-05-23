from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.maquina import Maquina , TipoEstadoMaquina
from app.repositories.maquina_repository import MaquinaRepository 
from app.repositories.categoria_maquina_repositoy import CategoriaMaquinaRepository 
from app.repositories.zona_instalacion import ZonaInstalacionRepository
from app.schemas.maquina import EstadoUpdate, MaquinaCreate

class MaquinaService:
    def __init__(self, db: AsyncSession):
        self.repo = MaquinaRepository(db)
        self.zona_repo = ZonaInstalacionRepository(db)
        self.categoria_repo = CategoriaMaquinaRepository(db)

    async def create_maquina(self, schema: MaquinaCreate) -> Maquina:
        # Verificar que la categoría exista
        categoria = await self.categoria_repo.get_by_id(schema.categoria_id)
        if not categoria:
            raise NotFoundException(detail="Categoría de máquina no encontrada", error_code="CATEGORIA_NOT_FOUND")
        
        indentificador_existente = await self.repo.get_by_identificador_interno(schema.identificador_interno)
        if indentificador_existente:
            raise AppException(detail="El identificador interno ya está en uso", error_code="IDENTIFICADOR_INTERNO_EXISTS", status_code=409)
        
        # Verificar que la zona de instalación exista
            # Verificar que la zona de instalación exista
        zona = await self.zona_repo.get_by_id(schema.zona_id)
        if not zona:
            raise NotFoundException(detail="Zona de instalación no encontrada", error_code="ZONA_INSTALACION_NOT_FOUND")
            
        Maquina_data = schema.model_dump()
        # Crear la máquina
        db_obj = await self.repo.create(Maquina_data)
        return await self.repo.get_by_id_with_relations(db_obj.id)
    
    async def update_maquina_estado(self, id: int, schema: EstadoUpdate) -> Maquina:
        # Verificar si la máquina existe
        maquina = await self.repo.get_by_id(id)
        if not maquina:
            raise NotFoundException(detail="Máquina no encontrada", error_code="MAQUINA_NOT_FOUND")
        
        if maquina.estado_operativo == TipoEstadoMaquina.fuera_de_servicio:
            raise BusinessRuleException(detail="La máquina ya está fuera de servicio", error_code="MAQUINA_ALREADY_OUT_OF_SERVICE")
        
        # Verificar si la maquina esta activa y se quiere activar, si es así verificar que no tenga tickets abiertos
        if schema.estado_operativo == TipoEstadoMaquina.activa:
            if self.repo.activar_maquina(id):
                raise BusinessRuleException(detail="No se puede activar la máquina porque tiene un ticket de mantenimiento abierto", error_code="MAQUINA_TICKET_ABIERTO")
            
        if schema.estado_operativo == TipoEstadoMaquina.fuera_de_servicio:
            if self.repo.activar_maquina(id):
                raise BusinessRuleException(detail="No se puede dar de baja la máquina porque tiene el ticket de mantenimiento abierto", error_code="MAQUINA_TICKET_ABIERTO")
                                            
        if schema.estado_operativo == TipoEstadoMaquina.en_mantenimiento:
            # Solo la creacion del ticket de mantenimiento puede poner la máquina en mantenimiento, 
            # por lo que se valida que el nuevo estado sea diferente al actual para evitar db call innecesario
            raise BusinessRuleException(detail="Para cambiar el estado a mantenimiento, se debe crear un ticket de mantenimiento", error_code="MAQUINA_NO_TICKET_CREATE")
            
        # Actualizar el estado operativo de la máquina
        update_data = schema.model_dump(exclude_unset=True)
        db_obj = await self.repo.update(db_obj=maquina, obj_in_data=update_data)
        return await self.repo.get_by_id_with_relations(db_obj.id)

    async def list_maquinas(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)