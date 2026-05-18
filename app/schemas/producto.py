from decimal import Decimal
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.models.producto_tienda import EstadoProducto


def mapear_estado_producto(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "activo": "Activo",
            "descontinuado": "Descontinuado",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoProductoTolerante = Annotated[EstadoProducto, BeforeValidator(mapear_estado_producto)]


class ProductoBase(BaseModel):
    categoria_producto_id: int = Field(..., description="ID de la categoría del producto")
    nombre_producto: str = Field(..., min_length=1, max_length=150, description="Nombre del producto")
    precio_actual: Decimal = Field(..., gt=0, description="Precio actual del producto")
    stock_disponible: int = Field(..., ge=0, description="Stock disponible")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    """Actualización parcial del producto."""
    nombre_producto: Optional[str] = Field(None, min_length=1, max_length=150, description="Nuevo nombre")
    precio_actual: Optional[Decimal] = Field(None, gt=0, description="Nuevo precio")
    stock_disponible: Optional[int] = Field(None, ge=0, description="Nuevo stock")


class ProductoUpdateEstado(BaseModel):
    estado_producto: EstadoProductoTolerante = Field(
        ..., description="Nuevo estado del producto (Activo, Descontinuado)"
    )


class ProductoFilterParams:
    def __init__(
        self,
        categoria_producto_id: Optional[int] = Query(None, description="Filtrar por categoría"),
        estado_producto: Optional[EstadoProductoTolerante] = Query(None, description="Filtrar por estado (Activo, Descontinuado)"),
        stock: Optional[str] = Query(None, description="Filtrar por stock: 'bajo' retorna productos con stock < 5"),
    ):
        self.categoria_producto_id = categoria_producto_id
        self.estado_producto = estado_producto
        self.stock = stock


class ProductoResponse(ProductoBase):
    id: int
    estado_producto: EstadoProductoTolerante

    model_config = ConfigDict(from_attributes=True)