from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.producto_tienda import EstadoProducto
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.venta_repository import VentaRepository
from app.schemas.venta import VentaCreate, VentaFilterParams


class VentaService:
    def __init__(self, db: AsyncSession):
        self.repo = VentaRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.producto_repo = ProductoRepository(db)

    async def create_venta(self, schema: VentaCreate):
        # 1. Verificar que el cliente exista
        cliente = await self.cliente_repo.get_by_id(schema.cliente_id)
        if not cliente:
            raise NotFoundException(detail="Cliente no encontrado", error_code="CLIENTE_NOT_FOUND")

        # 2. Validar cada producto: existencia, estado activo, stock suficiente
        productos_validados = []
        items_data = []

        for item in schema.items:
            producto = await self.producto_repo.get_by_id(item.producto_id)

            if not producto:
                raise NotFoundException(
                    detail=f"El producto con ID {item.producto_id} no fue encontrado",
                    error_code="PRODUCTO_NOT_FOUND"
                )

            if producto.estado_producto == EstadoProducto.descontinuado:
                raise AppException(
                    detail=f"El producto '{producto.nombre_producto}' está descontinuado y no puede venderse",
                    error_code="ERR_VENTA_PRODUCTO_DESCONTINUADO",
                    status_code=409
                )

            if producto.stock_disponible < item.cantidad:
                raise AppException(
                    detail=(
                        f"El producto '{producto.nombre_producto}' no cuenta con stock suficiente. "
                        f"Disponible: {producto.stock_disponible}, Solicitado: {item.cantidad}."
                    ),
                    error_code="ERR_VENTA_STOCK_INSUFICIENTE",
                    status_code=409
                )

            productos_validados.append(producto)
            items_data.append({
                "producto_id": producto.id,
                "cantidad": item.cantidad,
                "precio_unitario": producto.precio_actual,  # Precio histórico del momento
            })

        # 3. Operación atómica: cabecera + detalles + descuento de stock
        db_obj = await self.repo.crear_venta_completa(
            cliente_id=schema.cliente_id,
            metodo_pago=schema.metodo_pago,
            items=items_data,
            productos=productos_validados,
        )
        return await self.repo.get_by_id_with_relations(db_obj.id)

    async def get_venta_detallada(self, venta_id: int):
        venta = await self.repo.get_venta_con_detalles(venta_id)
        if not venta:
            raise NotFoundException(detail="Venta no encontrada", error_code="VENTA_NOT_FOUND")
        return venta

    async def list_ventas(self, filtros: VentaFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=filtros.cliente_id,
            metodo_pago=filtros.metodo_pago,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin,
        )