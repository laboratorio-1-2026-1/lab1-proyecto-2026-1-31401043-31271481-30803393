from pydantic import BaseModel, Field, BeforeValidator , ConfigDict
from fastapi import Query
from typing import Annotated, Optional

from app.models.entrenador import TipoEstado

def capitalizar_estado(v: str) -> str:
    if isinstance(v, str):
        return v.capitalize() # Pasa "activo" -> "Activo"
    return v

EstadoTolerante = Annotated[TipoEstado, BeforeValidator(capitalizar_estado)]

class EntrenadorBase(BaseModel):
    usuario_id: int = Field(..., ge=1, description="ID del usuario asociado al entrenador") 
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del entrenador")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido del entrenador")
    especialidad: str = Field(..., min_length=1, max_length=100, description="Especialidad del entrenador")
    telefono: str = Field(..., min_length=1, max_length=100, description="Teléfono del entrenador")

class EntrenadorFilterParams:
    def __init__(
            self,
            especialidad: Optional[str] = Query(None, min_length=1, max_length=100, description="Filtrar por especialidad del entrenador"),
            nombre: Optional[str] = Query(None, min_length=1, max_length=100, description="Filtrar por nombre del entrenador"),
            estado_laboral: Optional[EstadoTolerante] = Query(None,description="Filtrar por estado laboral del entrenador"),
        ):
        self.especialidad = especialidad
        self.nombre = nombre
        self.estado_laboral = estado_laboral


class EntrenadorCreate(EntrenadorBase):
    pass

class EntrenadorUpdate(BaseModel):
    especialidad: Optional[str] = Field(None, min_length=1, max_length=100, description="Nueva especialidad del entrenador")
    telefono: Optional[str] = Field(None, min_length=1, max_length=100, description="Nuevo teléfono del entrenador")

class EntrenadorUpdateEstado(BaseModel):
    estado_laboral: EstadoTolerante = Field(..., description="Nuevo estado laboral del entrenador (Activo,Inactivo, Vacaciones)")

class EntrenadorResponse(EntrenadorBase):
    id: int
    estado_laboral: EstadoTolerante

    model_config = ConfigDict(from_attributes=True)