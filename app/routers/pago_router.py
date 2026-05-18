from typing import List
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.pago import PagoCreate, PagoResponse, PagoFilterParams
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.pago_service import PagoService
from app.core.pagination import PaginationParams

router = APIRouter()

def get_service(db: AsyncSession = Depends(get_db)) -> PagoService:
    return PagoService(db)

@router.post("/", response_model=StandardResponse[PagoResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Finanzas", "Administración", "Administrador"))])
async def create_pago(schema: PagoCreate, service: PagoService = Depends(get_service)):
    """
    Registra la compra de un plan o su renovación.
    - Crea o actualiza la membresía del cliente basada en la duración del plan.
    - Registra de forma inmutable el monto, fecha y método de pago.
    - Rol Requerido: Finanzas / Administración.
    """
    res = await service.create_pago(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/me", response_model=PaginatedResponse[List[PagoResponse]],
            dependencies=[Depends(require_roles("Cliente"))])
async def get_mis_pagos(
    pagination: PaginationParams = Depends(),
    fecha_inicio: date = Query(None, description="Filtrar por fecha de pago inicial (YYYY-MM-DD)"),
    fecha_fin: date = Query(None, description="Filtrar por fecha de pago final (YYYY-MM-DD)"),
    service: PagoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Lista el historial de pagos y recibos realizados únicamente por el usuario autenticado.
    - Sirve para que el cliente pueda consultar su propia facturación desde su perfil.
    - Rol Requerido: Cliente.
    """
    total, res = await service.get_mis_pagos(
        usuario_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    return {
        "status": "success", 
        "message": "Operación completada con éxito", 
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }


@router.get("/", response_model=PaginatedResponse[List[PagoResponse]],
            dependencies=[Depends(require_roles("Finanzas", "Administración", "Administrador"))])
async def list_pagos(
    pagination: PaginationParams = Depends(),
    filtros: PagoFilterParams = Depends(),
    service: PagoService = Depends(get_service),
):
    """
    Lista el historial de pagos registrados en el sistema para auditoría.
    - Rol Requerido: Finanzas / Administración.
    """
    total, res = await service.list_pagos(
        skip=pagination.skip, 
        limit=pagination.limit, 
        filtros=filtros
    )
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }
