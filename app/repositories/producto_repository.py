from typing import List, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.producto_tienda import EstadoProducto, ProductoTienda
from app.repositories.base_repository import BaseRepository

UMBRAL_STOCK_BAJO = 5


class ProductoRepository(BaseRepository[ProductoTienda]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductoTienda, db)

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        categoria_producto_id: Optional[int] = None,
        estado_producto: Optional[EstadoProducto] = None,
        stock_bajo: bool = False,
    ) -> Tuple[int, List[ProductoTienda]]:
        #Listado con filtros de categoría, estado y alerta de stock bajo.
        conditions = []

        if categoria_producto_id is not None:
            conditions.append(ProductoTienda.categoria_producto_id == categoria_producto_id)
        if estado_producto is not None:
            conditions.append(ProductoTienda.estado_producto == estado_producto)
        if stock_bajo:
            conditions.append(ProductoTienda.stock_disponible < UMBRAL_STOCK_BAJO)

        query = select(ProductoTienda)
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(ProductoTienda.nombre_producto).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())