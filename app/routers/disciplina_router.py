from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.disciplina import (
    DisciplinaCreate,
    DisciplinaUpdate,
    DisciplinaUpdateEstado,
    DisciplinaFilterParams,
    DisciplinaResponse,
)
from app.schemas.response import StandardResponse
from app.services.disciplina_service import DisciplinaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> DisciplinaService:
    return DisciplinaService(db)


@router.post("/", response_model=StandardResponse[DisciplinaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_disciplina(disciplina_in: DisciplinaCreate, service: DisciplinaService = Depends(get_service)):
    res = await service.create_disciplina(schema=disciplina_in)
    return {"status": "success", "message": "Disciplina registrada exitosamente", "data": res}


@router.get("/", response_model=StandardResponse[List[DisciplinaResponse]])
async def list_disciplinas(
    skip: int = 0,
    limit: int = 100,
    filtros: DisciplinaFilterParams = Depends(),
    service: DisciplinaService = Depends(get_service),
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_disciplinas(skip=skip, limit=limit, filters=filters_dict)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.patch("/{id}", response_model=StandardResponse[DisciplinaResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_disciplina(id: int, disciplina_in: DisciplinaUpdate, service: DisciplinaService = Depends(get_service)):
    res = await service.update_disciplina(id=id, schema=disciplina_in)
    return {"status": "success", "message": "Disciplina actualizada exitosamente", "data": res}


@router.patch("/{id}/estado", response_model=StandardResponse[DisciplinaResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_disciplina_estado(id: int, estado_in: DisciplinaUpdateEstado, service: DisciplinaService = Depends(get_service)):
    res = await service.update_disciplina_estado(id=id, schema=estado_in)
    return {"status": "success", "message": "Estado de la disciplina actualizado exitosamente", "data": res}
