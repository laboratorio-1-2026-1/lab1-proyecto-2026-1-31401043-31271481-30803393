from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.reserva import (
    ReservaCreate,
    ReservaUpdateEstado,
    ReservaFilterParams,
    MisReservasFilterParams,
    ReservaResponse,
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.reserva_service import ReservaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ReservaService:
    return ReservaService(db)


@router.post("/", response_model=StandardResponse[ReservaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Cliente"))])
async def create_reserva(
    reserva_in: ReservaCreate,
    service: ReservaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos cliente_id del token
):
    """
    Inscribe al cliente autenticado en una sesión.
    - cliente_id extraído automáticamente del token JWT.
    - Valida cupo disponible, sesión activa y solapamiento horario.
    - Rol Requerido: Cliente.
    """
    res = await service.create_reserva(schema=reserva_in, usuario_id=current_user.id)
    return {"status": "success", "message": "Reserva realizada exitosamente", "data": res}


@router.get("/me", response_model=PaginatedResponse[List[ReservaResponse]],
            dependencies=[Depends(require_roles("Cliente"))])
async def get_mis_reservas(
    skip: int = 0,
    limit: int = 100,
    filtros: MisReservasFilterParams = Depends(),
    service: ReservaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos cliente_id del token
):
    """
    Retorna la agenda personal del cliente autenticado.
    - Rol Requerido: Cliente.
    """
    total, res = await service.list_mis_reservas(
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


@router.get("/", response_model=PaginatedResponse[List[ReservaResponse]],
            dependencies=[Depends(require_roles("Administrador", "Entrenador"))])
async def list_reservas(
    skip: int = 0,
    limit: int = 100,
    filtros: ReservaFilterParams = Depends(),
    service: ReservaService = Depends(get_service),
):
    """
    Lista las reservas con filtros para admin/entrenador.
    - Útil para ver la lista de asistentes de una sesión.
    - Rol Requerido: Administración / Entrenador.
    """
    total, res = await service.list_reservas(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.patch("/{id}/estado", response_model=StandardResponse[ReservaResponse],
            dependencies=[Depends(require_roles("Cliente", "Entrenador", "Administrador"))])
async def update_reserva_estado(
    id: int,
    estado_in: ReservaUpdateEstado,
    service: ReservaService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos el rol para validar permisos
):
    """
    Modifica el estado de una reserva.
    - Cliente: solo puede Cancelar su reserva.
    - Entrenador / Administración: pueden marcar como 'Asistio' o Cancelar.
    - Rol Requerido: Cliente / Entrenador / Administración.
    """
    rol_usuario = current_user.rol.nombre if current_user.rol else ""
    res = await service.update_reserva_estado(
        reserva_id=id,
        schema=estado_in,
        rol_usuario=rol_usuario,
    )
    return {"status": "success", "message": "Estado de la reserva actualizado exitosamente", "data": res}
