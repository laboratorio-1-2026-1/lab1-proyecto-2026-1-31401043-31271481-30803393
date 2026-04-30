from pydantic import BaseModel, Field
from datetime import date
from fastapi import Query
from typing import Annotated, Optional
from pydantic import BeforeValidator, ConfigDict

from app.models.membresia_cliente import EstadoMembresia

def formatear_cedula(v: str) -> str:
    if isinstance(v, str):
        return v.strip().upper() # Convierte "v-314046" o " v-314046 " -> "V-314046"
    return v

CedulaFormato = Annotated[
    str, 
    BeforeValidator(formatear_cedula), 
    Field(pattern=r"^[VEJPG]-\d{5,9}$")
]
def capitalizar_estado(v: str) -> str:
    if isinstance(v, str):
        return v.capitalize() # Pasa "activo" -> "Activo"
    return v

EstadoTolerante = Annotated[EstadoMembresia, BeforeValidator(capitalizar_estado)]

class ClienteBase(BaseModel):
    usuario_id: int = Field(..., ge=1, description="Cédula del cliente (Ej: V-314046)")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    cedula: CedulaFormato = Field(..., description="Cédula del cliente (Ej: V-314046)")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del cliente")
    telefono: str = Field(..., min_length=1, max_length=100, description="Teléfono del cliente")
    direccion: str = Field(..., min_length=1, max_length=100, description="Dirección del cliente")
    fecha_nacimiento: date = Field(..., gt=date(1900, 1, 1), lt=date(2023, 1, 1), description="Fecha de nacimiento del cliente")

class ClienteFilterParams:
    def __init__(
            self,
            cedula: Optional[CedulaFormato] = Query(None, description="Filtrar por cédula del cliente (Ej: V-314046)"),
            nombre: Optional[str] = Query(None, min_length=1, max_length=100,description="Filtrar por nombre del cliente"),
            apellido: Optional[str] = Query(None, min_length=1, max_length=100,description="Filtrar por apellido del cliente"),
            estado : Optional[EstadoTolerante] = Query(None,description="Filtrar por estado de la membresia"),
        ):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.estado = estado


class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    telefono: Optional[str] = Field(None, min_length=1, max_length=100, description="Nuevo teléfono del cliente")
    direccion: Optional[str] = Field(None, min_length=1, max_length=100, description="Nueva dirección del cliente")

class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)