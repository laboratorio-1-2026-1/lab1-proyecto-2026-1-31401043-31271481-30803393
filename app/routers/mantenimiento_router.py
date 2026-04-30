from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.pagination import PaginationParams
from app.schemas.response import StandardResponse, PaginatedResponse
from app.core.deps import get_db, get_current_user, require_roles
from app.models.usuario import Usuario
from app.schemas.ticket_mantenimiento import (
    TicketCreate, 
    TicketResolucion, 
    TicketResponse,
    TicketFilterParams
    )
from app.services.ticket_mantenimiento_service import TicketMantenimientoService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> TicketMantenimientoService:
    return TicketMantenimientoService(db)


@router.post("/tickets", response_model=StandardResponse[TicketResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_ticket(
    ticket_in: TicketCreate,
    service: TicketMantenimientoService = Depends(get_service),
    current_user: Usuario = Depends(get_current_user),  # Necesario: extraemos el id del token
):
    """
    Abre un ticket de mantenimiento para una máquina.
    - El usuario_id se extrae automáticamente del Bearer Token.
    - Cambia el estado de la máquina a 'En Mantenimiento' de forma atómica.
    - 409 si la máquina ya tiene un ticket abierto.
    - 404 si la máquina no existe.
    """
    res = await service.create_ticket(schema=ticket_in, usuario_id=current_user.id)
    return {"status": "success", "message": "Ticket de mantenimiento creado exitosamente", "data": res}

@router.get("/", response_model=PaginatedResponse[List[TicketResponse]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_tickets(
    pagination: PaginationParams = Depends(),
    filtros: TicketFilterParams = Depends(),
    service: TicketMantenimientoService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_tickets(skip=pagination.skip,
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
@router.patch("/tickets/{id}/resolucion", response_model=StandardResponse[TicketResponse],
            dependencies=[Depends(require_roles("Administrador"))])

async def cerrar_ticket(
    id: int,
    resolucion_in: TicketResolucion,
    service: TicketMantenimientoService = Depends(get_service),
):
    """
    Cierra un ticket de mantenimiento.
    - Registra fecha_resolucion, costo_reparacion y cambia estado_ticket a 'Cerrado'.
    - Reactiva la máquina vinculada a 'Activa' de forma atómica.
    - 404 si el ticket no existe.
    """
    res = await service.cerrar_ticket(ticket_id=id, schema=resolucion_in)
    return {"status": "success", "message": "Ticket cerrado y máquina reactivada exitosamente", "data": res}
