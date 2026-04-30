from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.entrenador import (
EntrenadorCreate, 
EntrenadorResponse, 
EntrenadorUpdate, 
EntrenadorFilterParams, 
EntrenadorUpdateEstado
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.entrenador_service import EntrenadorService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> EntrenadorService:
    return EntrenadorService(db)


@router.post("/", response_model=StandardResponse[EntrenadorResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_entrenador(schema: EntrenadorCreate, service: EntrenadorService = Depends(get_service)):
    res = await service.create_entrenador(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/", response_model=PaginatedResponse[List[EntrenadorResponse]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_entrenadores(
    pagination: PaginationParams = Depends(),
    filtros: EntrenadorFilterParams = Depends(),
    service: EntrenadorService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_entrenadores(skip=pagination.skip, limit=pagination.limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }


@router.patch("/{id}", response_model=StandardResponse[EntrenadorResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_entrenador(id: int, schema: EntrenadorUpdate, service: EntrenadorService = Depends(get_service)):
    res = await service.update_entrenador(id, schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.patch("/{id}/estado", response_model=StandardResponse[EntrenadorResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_entrenador_estado(id: int, schema: EntrenadorUpdateEstado, service: EntrenadorService = Depends(get_service)):
    res = await service.delete_soft_entrenador(id, schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}