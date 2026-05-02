from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.evaluacion_biometrica import (
    EvaluacionCreate,
    EvaluacionUpdate,
    EvaluacionFilterParams,
    MisEvaluacionesFilterParams,
    EvaluacionResponse,
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.evaluacion_biometrica_service import EvaluacionBiometricaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> EvaluacionBiometricaService:
    return EvaluacionBiometricaService(db)


@router.post("/", response_model=StandardResponse[EvaluacionResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Entrenador"))])
async def create_evaluacion(
    evaluacion_in: EvaluacionCreate,
    service: EvaluacionBiometricaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos entrenador_id del token
):
    """
    Registra una nueva evaluación biométrica.
    - entrenador_id extraído automáticamente del token JWT.
    - Rol Requerido: Entrenador.
    """
    res = await service.create_evaluacion(schema=evaluacion_in, usuario_id=current_user.id)
    return {"status": "success", "message": "Evaluación biométrica registrada exitosamente", "data": res}


@router.get("/me", response_model=PaginatedResponse[List[EvaluacionResponse]],
            dependencies=[Depends(require_roles("Cliente"))])
async def get_mis_evaluaciones(
    skip: int = 0,
    limit: int = 100,
    filtros: MisEvaluacionesFilterParams = Depends(),
    service: EvaluacionBiometricaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos cliente_id del token
):
    """
    Historial biométrico del cliente autenticado, ordenado cronológicamente.
    - Rol Requerido: Cliente.
    """
    total, res = await service.list_mis_evaluaciones(
        usuario_id=current_user.id,
        filtros=filtros,
        skip=skip,
        limit=limit,
    )
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/", response_model=PaginatedResponse[List[EvaluacionResponse]],
            dependencies=[Depends(require_roles("Entrenador", "Administrador"))])
async def list_evaluaciones(
    skip: int = 0,
    limit: int = 100,
    filtros: EvaluacionFilterParams = Depends(),
    service: EvaluacionBiometricaService = Depends(get_service),
):
    """
    Historial biométrico general, ordenado cronológicamente.
    - Filtrar por cliente_id para ver el progreso de un cliente específico.
    - Rol Requerido: Entrenador / Administración.
    """
    total, res = await service.list_evaluaciones(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.patch("/{id}", response_model=StandardResponse[EvaluacionResponse],
            dependencies=[Depends(require_roles("Entrenador"))])
async def update_evaluacion(
    id: int,
    evaluacion_in: EvaluacionUpdate,
    service: EvaluacionBiometricaService = Depends(get_service),
):
    """
    Corrige métricas de una evaluación biométrica existente.
    - Solo corrige campos de métricas, no cambia el entrenador ni el cliente.
    - Rol Requerido: Entrenador.
    """
    res = await service.update_evaluacion(id=id, schema=evaluacion_in)
    return {"status": "success", "message": "Evaluación biométrica actualizada exitosamente", "data": res}
