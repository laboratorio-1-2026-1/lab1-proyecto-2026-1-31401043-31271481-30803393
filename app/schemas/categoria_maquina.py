from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoriaMaquinaBase(BaseModel):
    nombre_categoria: str = Field(..., min_length=1, max_length=100, description="Nombre de la categoría de la maquina")
    descripcion: Optional[str] = Field(None, max_length=255, description="Descripción de la categoría de la maquina")

class CategoriaMaquinaFilterParams:
    pass

class CategoriaMaquinaCreate(CategoriaMaquinaBase):
    pass

class CategoriaMaquinaResponse(CategoriaMaquinaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)