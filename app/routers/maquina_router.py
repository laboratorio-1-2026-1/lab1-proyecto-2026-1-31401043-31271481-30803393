from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.response import StandardResponse, PaginatedResponse
from app.schemas.maquina import (
    MaquinaCreate, 
    MaquinaResponse, 
    MaquinaFilterParams, 
    EstadoUpdate
    )
from app.services.maquina_service import MaquinaService

router = APIRouter() 

def get_service(db: Session = Depends(get_db)) -> MaquinaService:
    return MaquinaService(db)

@router.post("/", response_model=StandardResponse[MaquinaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_maquina(schema: MaquinaCreate, service: MaquinaService = Depends(get_service)):
    res = await service.create_maquina(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}

@router.get("/", response_model=PaginatedResponse[List[MaquinaResponse]])
async def list_maquinas(
    pagination: PaginationParams = Depends(),
    filtros: MaquinaFilterParams = Depends(),
    service: MaquinaService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_maquinas(skip=pagination.skip,
        limit=pagination.limit,
        filters=filters_dict,
        )
    return {
        "status": "success", 
        "message": "Operación completada con éxito", 
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }

@router.patch("/{id}/estado", response_model=StandardResponse[MaquinaResponse], dependencies=[Depends(require_roles("Administrador"))])
async def update_maquina_estado(
    id: int,
    schema: EstadoUpdate,
    service: MaquinaService = Depends(get_service)
):
    res = await service.update_maquina_estado(id, schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}
