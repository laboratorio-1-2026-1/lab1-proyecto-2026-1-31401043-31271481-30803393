from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.repositories.entrenador_repository import EntrenadorRepository
from app.schemas.sesion_programada import (
    SesionCreate,
    SesionFilterParams,
    MisSesionesFilterParams,
    SesionUpdateEstado,
    SesionResponse,
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.sesion_programada_service import SesionProgramadaService
from app.core.errors import NotFoundException

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> SesionProgramadaService:
    return SesionProgramadaService(db)


@router.post("/", response_model=StandardResponse[SesionResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_sesion(sesion_in: SesionCreate, service: SesionProgramadaService = Depends(get_service)):
    """
    Crea una nueva sesión en el calendario.
    - Valida disponibilidad del entrenador, zona, disciplina y solapamientos.
    - Rol Requerido: Administrador.
    """
    res = await service.create_sesion(schema=sesion_in)
    return {"status": "success", "message": "Sesión programada exitosamente", "data": res}


@router.get("/me", response_model=PaginatedResponse[List[SesionResponse]])
async def get_mis_sesiones(
    skip: int = 0,
    limit: int = 100,
    filtros: MisSesionesFilterParams = Depends(),
    service: SesionProgramadaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos entrenador_id del token
    db: AsyncSession = Depends(get_db),
):
    """
    Devuelve las sesiones asignadas al entrenador autenticado.
    - El entrenador_id se obtiene automáticamente del token JWT.
    - Rol Requerido: Entrenador.
    """
    # Obtener el entrenador vinculado al usuario del token
    entrenador_repo = EntrenadorRepository(db)
    entrenador = await entrenador_repo.get_by_usuario_id(current_user.id)
    if not entrenador:
        raise NotFoundException(detail="No se encontró un entrenador vinculado a este usuario", error_code="ENTRENADOR_NOT_FOUND")

    total, res = await service.list_mis_sesiones(
        entrenador_id=entrenador.id,
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


@router.get("/", response_model=PaginatedResponse[List[SesionResponse]])
async def list_sesiones(
    skip: int = 0,
    limit: int = 100,
    filtros: SesionFilterParams = Depends(),
    service: SesionProgramadaService = Depends(get_service),
):
    """
    Lista las sesiones programadas con filtros opcionales.
    - Rol Requerido: Todos (sin restricción).
    """
    total, res = await service.list_sesiones(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.patch("/{id}/estado", response_model=StandardResponse[SesionResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_sesion_estado(id: int, estado_in: SesionUpdateEstado, service: SesionProgramadaService = Depends(get_service)):
    """
    Avanza el estado de una sesión (Programada → En Curso → Finalizada | Cancelada).
    - Solo permite transiciones de estado válidas.
    - Rol Requerido: Administrador.
    """
    res = await service.update_sesion_estado(id=id, schema=estado_in)
    return {"status": "success", "message": "Estado de la sesión actualizado exitosamente", "data": res}
