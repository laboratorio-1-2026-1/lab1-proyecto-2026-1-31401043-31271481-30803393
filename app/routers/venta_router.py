from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.venta import VentaCreate, VentaFilterParams, VentaResponse, VentaDetalladaResponse
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.venta_service import VentaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> VentaService:
    return VentaService(db)


@router.post("/", response_model=StandardResponse[VentaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Finanzas", "Administrador"))])
async def create_venta(venta_in: VentaCreate, service: VentaService = Depends(get_service)):
    """
    Procesa una nueva venta de productos.
    - Valida stock de cada ítem antes de procesar.
    - Captura el precio histórico del momento de la venta.
    - Descuenta automáticamente el stock del inventario.
    - Rol Requerido: Finanzas / Administración.
    """
    res = await service.create_venta(schema=venta_in)
    return {"status": "success", "message": "Venta procesada exitosamente", "data": res}


@router.get("/", response_model=PaginatedResponse[List[VentaResponse]],
            dependencies=[Depends(require_roles("Finanzas", "Administrador"))])
async def list_ventas(
    skip: int = 0,
    limit: int = 100,
    filtros: VentaFilterParams = Depends(),
    service: VentaService = Depends(get_service),
):
    """
    Historial de ventas para cuadre de caja.
    - Filtros: cliente_id, metodo_pago, fecha_inicio, fecha_fin.
    - Rol Requerido: Finanzas / Administración.
    """
    total, res = await service.list_ventas(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{id}", response_model=StandardResponse[VentaDetalladaResponse],
            dependencies=[Depends(require_roles("Finanzas", "Administrador"))])
async def get_venta(id: int, service: VentaService = Depends(get_service)):
    """
    Detalle completo de una venta con todos sus ítems.
    - Incluye precio_unitario_historico de cada producto al momento de la compra.
    - Rol Requerido: Finanzas / Administración.
    """
    res = await service.get_venta_detallada(venta_id=id)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}