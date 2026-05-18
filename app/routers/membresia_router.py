from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.membresia import MembresiaFilterParams, MembresiaResponse
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.membresia_service import MembresiaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> MembresiaService:
    return MembresiaService(db)


@router.get("/me", response_model=StandardResponse[List[MembresiaResponse]],
            dependencies=[Depends(require_roles("Cliente"))])
async def get_mis_membresias(
    service: MembresiaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos cliente_id del token
):
    """
    Retorna las membresías del cliente autenticado con su estado actualizado.
    - El estado se recalcula dinámicamente: Activa, Por Vencer o Vencida.
    - 404 si el cliente no tiene membresías registradas.
    - Rol Requerido: Cliente.
    """
    res = await service.get_mis_membresias(usuario_id=current_user.id)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/", response_model=PaginatedResponse[List[MembresiaResponse]],
            dependencies=[Depends(require_roles("Administrador", "Finanzas"))])
async def list_membresias(
    skip: int = 0,
    limit: int = 100,
    filtros: MembresiaFilterParams = Depends(),
    service: MembresiaService = Depends(get_service),
):
    """
    Lista las membresías con estados actualizados dinámicamente.
    - Filtros opcionales: cliente_id, estado (Activa, Por Vencer, Vencida).
    - Rol Requerido: Administración / Finanzas.
    """
    total, res = await service.list_membresias(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
