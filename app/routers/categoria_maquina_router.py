from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.categoria_maquina import (
    CategoriaMaquinaCreate, 
    CategoriaMaquinaResponse, 
    CategoriaMaquinaFilterParams
    )
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.categoria_maquina_service import CategoriaMaquinaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> CategoriaMaquinaService:
    return CategoriaMaquinaService(db)


@router.post("/", response_model=StandardResponse[CategoriaMaquinaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_categoria_maquina(schema: CategoriaMaquinaCreate, service: CategoriaMaquinaService = Depends(get_service)):
    res = await service.create_categoria_maquina(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/", response_model=PaginatedResponse[List[CategoriaMaquinaResponse]])
async def list_categoria_maquinas(
    pagination: PaginationParams = Depends(),
    filtros: CategoriaMaquinaFilterParams = Depends(),
    service: CategoriaMaquinaService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_categoria_maquinas(skip=pagination.skip, limit=pagination.limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }
