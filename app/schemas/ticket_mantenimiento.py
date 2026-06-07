from pydantic import BaseModel, ConfigDict, Field, BeforeValidator , AwareDatetime
from typing import Optional, Annotated
from decimal import Decimal

from fastapi import Query

from app.models.ticket_mantenimiento import TipoEstado

def mapear_estado_ticket(v: str) -> str:
    if isinstance(v, str):
        # Limpiamos espacios y pasamos a minúsculas
        v_lower = v.strip().lower()
        
        # Diccionario de equivalencias
        mapping = {
            "abierto": "Abierto",
            "Abierto": "Abierto",
            "cerrado": "Cerrado",
            "Cerrado": "Cerrado"     
        }
        
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoSesionTolerante = Annotated[TipoEstado, BeforeValidator(mapear_estado_ticket)]

class TicketCreate(BaseModel):
    maquina_id: int = Field(..., description="ID de la máquina que presenta la falla")
    descripcion: str = Field(..., min_length=5, max_length=500, description="Descripción de la falla reportada")

class TicketFilterParams:
    """Filtros para GET /sesiones (vista general)."""
    def __init__(
        self,
        maquina_id: Optional[int] = Query(None, description="Filtrar por ID de maquina"),
        estado_ticket: Optional[EstadoSesionTolerante] = Query(None, description="Filtrar por estado (Abierto, Cerrado)"),
    ):
        self.maquina_id = maquina_id
        self.estado_ticket = estado_ticket

class TicketResolucion(BaseModel):
    costo_reparacion: Decimal = Field(..., gt=0, description="Costo de la reparación (mayor a 0)")


class TicketResponse(BaseModel):
    id: int
    maquina_id: int
    usuario_id: int
    descripcion: str
    fecha_falla: AwareDatetime
    fecha_resolucion: Optional[AwareDatetime]
    costo_reparacion: Optional[Decimal]
    estado_ticket: TipoEstado
    nombre_maquina: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
