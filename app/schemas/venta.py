from decimal import Decimal
from typing import Annotated, List, Optional
from datetime import date
from fastapi import Query
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, AwareDatetime

from app.models.venta_tienda import MetodoPago


def mapear_metodo_pago(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "efectivo": "Efectivo",
            "tarjeta": "Tarjeta",
            "transferencia": "Transferencia",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


MetodoPagoTolerante = Annotated[MetodoPago, BeforeValidator(mapear_metodo_pago)]


# ─────────────────────────────────────────────
# Schemas de entrada
# ─────────────────────────────────────────────

class VentaItem(BaseModel):
    producto_id: int = Field(..., description="ID del producto")
    cantidad: int = Field(..., gt=0, description="Cantidad a comprar (mayor a 0)")


class VentaCreate(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente comprador")
    metodo_pago: MetodoPagoTolerante = Field(..., description="Método de pago (Efectivo, Tarjeta, Transferencia)")
    items: List[VentaItem] = Field(..., min_length=1, description="Lista de productos a comprar (mínimo 1)")


class VentaFilterParams:
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
        metodo_pago: Optional[MetodoPagoTolerante] = Query(None, description="Filtrar por método de pago"),
        fecha_inicio: Optional[date] = Query(None, description="Desde esta fecha (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Hasta esta fecha (YYYY-MM-DD)"),
    ):
        self.cliente_id = cliente_id
        self.metodo_pago = metodo_pago
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


# ─────────────────────────────────────────────
# Schemas de respuesta
# ─────────────────────────────────────────────

class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario_historico: Decimal

    model_config = ConfigDict(from_attributes=True)


class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_venta: AwareDatetime
    total_venta: Decimal
    metodo_pago: MetodoPagoTolerante
    nombre_cliente: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VentaDetalladaResponse(VentaResponse):
    """Venta con sus ítems incluidos (GET /ventas/{id})."""
    detalle_ventas: List[DetalleVentaResponse] = []