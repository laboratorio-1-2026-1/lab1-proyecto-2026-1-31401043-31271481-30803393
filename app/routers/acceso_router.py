from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.acceso import (
    AccesoEntradaCreate, 
    AccesoFilterParams, 
    AccesoResponse
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.acceso_service import AccesoService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> AccesoService:
    return AccesoService(db)


@router.post("/entrada", response_model=StandardResponse[AccesoResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))]) 
async def registrar_entrada(entrada_in: AccesoEntradaCreate, service: AccesoService = Depends(get_service)):
    """
    Registra el paso por el torniquete o recepción.
    - Valida la membresía en tiempo real.
    - Siempre registra el intento (concedido o denegado).
    - 409 si la membresía está vencida o no existe.
    - 404 si la cédula no existe.
    - Rol Requerido: Administración / Sistema Automático.
    """
    res = await service.registrar_entrada(schema=entrada_in)
    return {"status": "success", "message": "Acceso concedido", "data": res}


@router.get("/", response_model=PaginatedResponse[List[AccesoResponse]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_accesos(
    skip: int = 0,
    limit: int = 100,
    filtros: AccesoFilterParams = Depends(),
    service: AccesoService = Depends(get_service),
):
    """
    Consulta la bitácora de entradas históricas.
    - Filtros opcionales: cliente_id, acceso_concedido, fecha_inicio, fecha_fin.
    - Rol Requerido: Administrador.
    """
    total, res = await service.list_accesos(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
