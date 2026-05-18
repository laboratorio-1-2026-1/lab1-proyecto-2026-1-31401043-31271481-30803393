from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoriaProductoBase(BaseModel):
    nombre_categoria: str = Field(..., min_length=1, max_length=100, description="Nombre de la categoría de producto")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción de la categoría")


class CategoriaProductoCreate(CategoriaProductoBase):
    pass


class CategoriaProductoUpdate(BaseModel):
    """Actualización parcial de la categoría."""
    nombre_categoria: Optional[str] = Field(None, min_length=1, max_length=100, description="Nuevo nombre")
    descripcion: Optional[str] = Field(None, max_length=500, description="Nueva descripción")


class CategoriaProductoResponse(CategoriaProductoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)