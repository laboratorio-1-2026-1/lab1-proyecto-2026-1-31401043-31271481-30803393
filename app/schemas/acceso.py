from datetime import date
from typing import Optional, Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator , AwareDatetime


def formatear_cedula(v: str) -> str:
    if isinstance(v, str):
        return v.strip().upper() # Convierte "v-314046" o " v-314046 " -> "V-314046"
    return v

CedulaFormato = Annotated[
    str, 
    BeforeValidator(formatear_cedula), 
    Field(pattern=r"^[VEJPG]-\d{5,9}$")
]
class AccesoEntradaCreate(BaseModel):
    cedula: CedulaFormato = Field(..., min_length=1, max_length=20, description="Documento de identidad del cliente (ej. V-12345678)")


class AccesoFilterParams:
    """Filtros para GET /accesos (vista admin — bitácora histórica)."""
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
        acceso_concedido: Optional[bool] = Query(None, description="Filtrar por acceso concedido (true/false)"),
        fecha_inicio: Optional[date] = Query(None, description="Desde esta fecha (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Hasta esta fecha (YYYY-MM-DD)"),
    ):
        self.cliente_id = cliente_id
        self.acceso_concedido = acceso_concedido
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class AccesoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_hora_entrada: AwareDatetime
    acceso_concedido: bool
    nombre_cliente: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
