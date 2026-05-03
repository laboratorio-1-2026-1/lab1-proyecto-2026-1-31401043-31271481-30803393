from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import Annotated

from app.models.membresia_cliente import EstadoMembresia


def mapear_estado_membresia(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "activa": "Activa",
            "por vencer": "Por Vencer",
            "vencida": "Vencida",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoMembresiaTolerante = Annotated[EstadoMembresia, BeforeValidator(mapear_estado_membresia)]


class MembresiaFilterParams:
    """Filtros para GET /membresias (vista admin/finanzas)."""
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
        estado: Optional[EstadoMembresiaTolerante] = Query(None, description="Filtrar por estado (Activa, Por Vencer, Vencida)"),
    ):
        self.cliente_id = cliente_id
        self.estado = estado


class MembresiaResponse(BaseModel):
    id: int
    cliente_id: int
    plan_id: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoMembresiaTolerante

    model_config = ConfigDict(from_attributes=True)
