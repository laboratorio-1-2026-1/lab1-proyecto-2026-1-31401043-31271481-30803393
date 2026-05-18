from datetime import date, datetime, timezone, time
from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.detalle_venta import DetalleVenta
from app.models.venta_tienda import MetodoPago, VentaTienda
from app.repositories.base_repository import BaseRepository


class VentaRepository(BaseRepository[VentaTienda]):
    def __init__(self, db: AsyncSession):
        super().__init__(VentaTienda, db)

    async def crear_venta_completa(
        self,
        cliente_id: int,
        metodo_pago: MetodoPago,
        items: list,       # List[dict] con producto_id, cantidad, precio_unitario
        productos: list,   # List[ProductoTienda] ya validados
    ) -> VentaTienda:
        """
        Operación atómica: crea cabecera + detalles + descuenta stock.
        Toca 3 tablas en una misma transacción.
        """
        # Calcular el total de la venta
        total = Decimal("0")
        for item in items:
            total += item["precio_unitario"] * item["cantidad"]

        # Crear la cabecera de la venta
        venta = VentaTienda(
            cliente_id=cliente_id,
            fecha_venta=datetime.now(timezone.utc),
            total_venta=total,
            metodo_pago=metodo_pago,
        )
        self.db.add(venta)
        await self.db.flush()  # Obtener el venta.id generado

        # Insertar los detalles y descontar stock
        for item in items:
            detalle = DetalleVenta(
                venta_id=venta.id,
                producto_id=item["producto_id"],
                cantidad=item["cantidad"],
                precio_unitario_historico=item["precio_unitario"],
            )
            self.db.add(detalle)

        # Descontar stock de cada producto
        for producto in productos:
            # Buscar la cantidad solicitada para este producto
            cantidad = next(i["cantidad"] for i in items if i["producto_id"] == producto.id)
            producto.stock_disponible -= cantidad
            self.db.add(producto)

        await self.db.commit()
        await self.db.refresh(venta)
        return venta

    async def get_venta_con_detalles(self, venta_id: int) -> VentaTienda | None:
        #Retorna una venta con sus detalles cargados (eager loading).
        result = await self.db.execute(
            select(VentaTienda)
            .options(selectinload(VentaTienda.detalle_ventas))
            .where(VentaTienda.id == venta_id)
        )
        return result.scalars().first()

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        metodo_pago: Optional[MetodoPago] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ) -> Tuple[int, List[VentaTienda]]:
        """Historial de ventas con filtros."""
        conditions = []

        if cliente_id is not None:
            conditions.append(VentaTienda.cliente_id == cliente_id)
        if metodo_pago is not None:
            conditions.append(VentaTienda.metodo_pago == metodo_pago)
        if fecha_inicio is not None:
            inicio = datetime.combine(fecha_inicio, time.min, tzinfo=timezone.utc)
            conditions.append(VentaTienda.fecha_venta >= inicio)
        if fecha_fin is not None:
            fin = datetime.combine(fecha_fin, time.max, tzinfo=timezone.utc)
            conditions.append(VentaTienda.fecha_venta <= fin)

        query = select(VentaTienda)
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(VentaTienda.fecha_venta.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())