from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.categoria_producto import CategoriaProducto
from app.repositories.categoria_producto_repository import CategoriaProductoRepository
from app.schemas.categoria_producto import CategoriaProductoCreate, CategoriaProductoUpdate


class CategoriaProductoService:
    def __init__(self, db: AsyncSession):
        self.repo = CategoriaProductoRepository(db)

    async def create_categoria(self, schema: CategoriaProductoCreate) -> CategoriaProducto:
        existente = await self.repo.get_by_nombre(schema.nombre_categoria)
        if existente:
            raise AppException(
                detail="El nombre de la categoría de producto ya está registrado",
                error_code="CATEGORIA_PRODUCTO_NAME_EXISTS",
                status_code=409
            )
        return await self.repo.create(schema.model_dump())

    async def update_categoria(self, id: int, schema: CategoriaProductoUpdate) -> CategoriaProducto:
        categoria = await self.repo.get_by_id(id)
        if not categoria:
            raise NotFoundException(detail="Categoría de producto no encontrada", error_code="CATEGORIA_PRODUCTO_NOT_FOUND")

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return categoria

        if "nombre_categoria" in update_data:
            existente = await self.repo.get_by_nombre(update_data["nombre_categoria"])
            if existente and existente.id != id:
                raise AppException(
                    detail="El nombre de la categoría ya está en uso por otra categoría",
                    error_code="CATEGORIA_PRODUCTO_NAME_EXISTS",
                    status_code=409
                )

        return await self.repo.update(db_obj=categoria, obj_in_data=update_data)

    async def list_categorias(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip=skip, limit=limit)