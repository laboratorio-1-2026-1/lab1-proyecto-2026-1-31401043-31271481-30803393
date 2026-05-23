from pydantic import BaseModel, ConfigDict, Field,  BeforeValidator
from typing import  Optional, Annotated
from fastapi import Query

from app.models.maquina import TipoEstadoMaquina

def capitalizar_estado(v: str) -> str:
    if isinstance(v, str):
        # Limpiamos espacios y pasamos todo a minúsculas
        v = v.strip().lower()
        
        # Capitalizamos como frase (Primera letra en mayúscula)
        v = v.capitalize()
        
        # Si es "En mantenimiento", arreglamos la 'm' de mantenimiento
        # Buscamos específicamente las palabras que sí quieres en mayúscula
        palabras_a_corregir = ["Mantenimiento", "Servicio"]
        
        for palabra in palabras_a_corregir:
            if palabra.lower() in v:
                v = v.replace(palabra.lower(), palabra)
        
        return v
    return v

EstadoTolerante = Annotated[TipoEstadoMaquina, BeforeValidator(capitalizar_estado)]

class MaquinaBase(BaseModel):
    categoria_id: int = Field(..., description="ID de la categoría de la máquina")
    zona_id: int = Field(..., description="ID de la zona de la máquina")
    identificador_interno: str = Field(..., min_length=1, max_length=50, description="Identificador interno único de la máquina")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la máquina")
    descripcion_tecnica: str = Field(..., min_length=5, max_length=255, description="Descripción tecnica de la máquina")

class MaquinaFilterParams:
    def __init__(
        self,
        categoria_id: Optional[int] = Query(None, description="Filtrar por ID de la categoría de la máquina"),
        estado_operativo: Optional[EstadoTolerante] = Query(None, description="Filtrar por estado operativo de la máquina (Activa, En Mantenimiento, Fuera de Servicio)"),
        zona_id: Optional[int] = Query(None, description="Filtrar por ID de la zona de la máquina"),

    ):
        self.categoria_id = categoria_id
        self.estado_operativo = estado_operativo
        self.zona_id = zona_id


class MaquinaCreate(MaquinaBase):
    pass

class EstadoUpdate(BaseModel):
    estado_operativo: EstadoTolerante = Field(
        ..., 
        description="Nuevo estado operativo de la máquina (Activa, En Mantenimiento, Fuera de Servicio)"
    )

class MaquinaResponse(MaquinaBase):
    id: int
    estado_operativo: EstadoTolerante
    nombre_categoria: Optional[str] = None
    nombre_zona: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)