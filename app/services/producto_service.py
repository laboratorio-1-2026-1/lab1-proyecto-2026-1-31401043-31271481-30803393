from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import  NotFoundException
from app.models.producto_tienda import ProductoTienda
from app.repositories.categoria_producto_repository import CategoriaProductoRepository
from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoFilterParams, ProductoUpdate, ProductoUpdateEstado


class ProductoService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductoRepository(db)
        self.categoria_repo = CategoriaProductoRepository(db)

    async def create_producto(self, schema: ProductoCreate) -> ProductoTienda:
        # Verificar que la categoría exista
        categoria = await self.categoria_repo.get_by_id(schema.categoria_producto_id)
        if not categoria:
            raise NotFoundException(
                detail="Categoría de producto no encontrada",
                error_code="CATEGORIA_PRODUCTO_NOT_FOUND"
            )

        return await self.repo.create(schema.model_dump())

    async def update_producto(self, id: int, schema: ProductoUpdate) -> ProductoTienda:
        producto = await self.repo.get_by_id(id)
        if not producto:
            raise NotFoundException(detail="Producto no encontrado", error_code="PRODUCTO_NOT_FOUND")

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return producto

        return await self.repo.update(db_obj=producto, obj_in_data=update_data)

    async def update_producto_estado(self, id: int, schema: ProductoUpdateEstado) -> ProductoTienda:
        producto = await self.repo.get_by_id(id)
        if not producto:
            raise NotFoundException(detail="Producto no encontrado", error_code="PRODUCTO_NOT_FOUND")

        if producto.estado_producto == schema.estado_producto:
            return producto

        return await self.repo.update(db_obj=producto, obj_in_data=schema.model_dump(exclude_unset=True))

    async def list_productos(self, filtros: ProductoFilterParams, skip: int, limit: int):
        stock_bajo = filtros.stock is not None and filtros.stock.lower() == "bajo"
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            categoria_producto_id=filtros.categoria_producto_id,
            estado_producto=filtros.estado_producto,
            stock_bajo=stock_bajo,
        )