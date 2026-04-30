from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException
from app.models.categoria_maquina import CategoriaMaquina
from app.repositories.categoria_maquina_repositoy import CategoriaMaquinaRepository
from app.schemas.categoria_maquina import CategoriaMaquinaCreate

class CategoriaMaquinaService:
    def __init__(self, db: AsyncSession):
        self.repo = CategoriaMaquinaRepository(db)

    async def create_categoria_maquina(self, schema: CategoriaMaquinaCreate) -> CategoriaMaquina:
        # Verificar si el nombre de la categoria existe
        exiting_categoria = await self.repo.get_by_name(schema.nombre_categoria)
        if exiting_categoria:
            raise AppException(detail="El nombre de la categoría ya existe", error_code="CATEGORIA_NAME_EXISTS", status_code=409)
        
        
        categoria_data = schema.model_dump()
        return await self.repo.create(categoria_data)
    

    async def list_categoria_maquinas(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)