from pydantic import BaseModel, ConfigDict, BeforeValidator, Field , AwareDatetime
from typing import Annotated, Optional
from fastapi import Query

from app.models.reserva import TipoEstado


def mapear_estado_reserva(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "confirmada": "Confirmada",
            "cancelada": "Cancelada",
            "asistio": "Asistio",
            "asistió": "Asistio",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoReservaTolerante = Annotated[TipoEstado, BeforeValidator(mapear_estado_reserva)]


class ReservaCreate(BaseModel):
    sesion_id: int = Field(..., description="ID de la sesión a la que se desea inscribir")
    # cliente_id se extrae del token JWT, no se expone en el payload


class ReservaUpdateEstado(BaseModel):
    estado_reserva: EstadoReservaTolerante = Field(
        ..., description="Nuevo estado de la reserva (Confirmada, Cancelada, Asistio)"
    )


class ReservaFilterParams:
    """Filtros para GET /reservas (vista admin/entrenador)."""
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
        sesion_id: Optional[int] = Query(None, description="Filtrar por ID de sesión"),
        estado_reserva: Optional[EstadoReservaTolerante] = Query(None, description="Filtrar por estado"),
    ):
        self.cliente_id = cliente_id
        self.sesion_id = sesion_id
        self.estado_reserva = estado_reserva


class MisReservasFilterParams:
    """Filtros para GET /reservas/me (vista del cliente autenticado)."""
    def __init__(
        self,
        estado_reserva: Optional[EstadoReservaTolerante] = Query(None, description="Filtrar por estado"),
    ):
        self.estado_reserva = estado_reserva


class ReservaResponse(BaseModel):
    id: int
    sesion_id: int
    cliente_id: int
    fecha_registro: AwareDatetime
    estado_reserva: EstadoReservaTolerante

    model_config = ConfigDict(from_attributes=True)
