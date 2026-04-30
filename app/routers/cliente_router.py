from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.cliente import (
    ClienteCreate, 
    ClienteResponse, 
    ClienteUpdate, 
    ClienteFilterParams
    )
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.cliente_service import ClienteService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ClienteService:
    return ClienteService(db)


@router.post("/", response_model=StandardResponse[ClienteResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_cliente(schema: ClienteCreate, service: ClienteService = Depends(get_service)):
    res = await service.create_cliente(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/", response_model=PaginatedResponse[List[ClienteResponse]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_clientes(
    pagination: PaginationParams = Depends(),
    filtros: ClienteFilterParams = Depends(),
    service: ClienteService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_clientes(skip=pagination.skip, limit=pagination.limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }


@router.patch("/{id}", response_model=StandardResponse[ClienteResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_cliente(id: int, schema: ClienteUpdate, service: ClienteService = Depends(get_service)):
    res = await service.update_cliente(id, schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}