from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.plan_suscripcion import (
    PlanCreate,
    PlanUpdate,
    PlanUpdateEstado,
    PlanFilterParams,
    PlanResponse,
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.plan_suscripcion_service import PlanSuscripcionService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> PlanSuscripcionService:
    return PlanSuscripcionService(db)


@router.post("/", response_model=StandardResponse[PlanResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador", "Finanzas"))])
async def create_plan(plan_in: PlanCreate, service: PlanSuscripcionService = Depends(get_service)):
    res = await service.create_plan(schema=plan_in)
    return {"status": "success", "message": "Plan de suscripción creado exitosamente", "data": res}


@router.get("/", response_model=PaginatedResponse[List[PlanResponse]])
async def list_planes(
    skip: int = 0,
    limit: int = 100,
    filtros: PlanFilterParams = Depends(),
    service: PlanSuscripcionService = Depends(get_service),
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_planes(skip=skip, limit=limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.patch("/{id}", response_model=StandardResponse[PlanResponse],
            dependencies=[Depends(require_roles("Administrador", "Finanzas"))])
async def update_plan(id: int, plan_in: PlanUpdate, service: PlanSuscripcionService = Depends(get_service)):
    res = await service.update_plan(id=id, schema=plan_in)
    return {"status": "success", "message": "Plan de suscripción actualizado exitosamente", "data": res}


@router.patch("/{id}/estado", response_model=StandardResponse[PlanResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_plan_estado(id: int, estado_in: PlanUpdateEstado, service: PlanSuscripcionService = Depends(get_service)):
    res = await service.update_plan_estado(id=id, schema=estado_in)
    return {"status": "success", "message": "Estado del plan actualizado exitosamente", "data": res}
