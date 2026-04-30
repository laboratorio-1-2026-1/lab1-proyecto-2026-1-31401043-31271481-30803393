from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from typing import  Annotated
from app.models.zona_instalacion import TipoEstado

def mapear_estado_zona(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        if v_lower == "en mantenimiento" or v_lower == "mantenimiento":
            return "Mantenimiento"
        if v_lower == "activa":
            return "Activa"
        if v_lower == "inactiva":
            return "Inactiva"
        if v_lower == "cerrada":
            return "Cerrada"
        return v.capitalize()
    return v

EstadoZonaTolerante = Annotated[TipoEstado, BeforeValidator(mapear_estado_zona)]

class ZonaBase(BaseModel):
    nombre_zona: str = Field(..., min_length=1, max_length=100, description="Nombre de la zona de instalación")
    capacidad_maxima: int = Field(..., gt=0, description="Capacidad máxima de personas en la zona")

class ZonaCreate(ZonaBase):
    pass

class ZonaUpdateEstado(BaseModel):
    estado_zona: EstadoZonaTolerante = Field(..., description="Estado operativo de la zona (Activa, Inactiva, Mantenimiento, Cerrada)")

class ZonaResponse(ZonaBase):
    id: int
    estado_zona: EstadoZonaTolerante

    model_config = ConfigDict(from_attributes=True)
