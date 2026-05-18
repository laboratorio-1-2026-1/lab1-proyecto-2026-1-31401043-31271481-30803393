from datetime import datetime, date
from typing import Optional, Annotated
from decimal import Decimal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from app.models.pago_membresia import MetodoPago

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

class PagoCreate(BaseModel):
    cliente_id: int
    plan_id: int
    monto_pagado: Decimal = Field(..., gt=0)
    metodo_pago: MetodoPagoTolerante = Field(..., description="Debe ser Efectivo, Tarjeta o Transferencia")

class PagoFilterParams:
    """Filtros para GET /pagos (vista admin/finanzas)."""
    def __init__(
        self,
        membresia_id: Optional[int] = Query(None, description="Filtrar por ID de membresía"),
        metodo_pago: Optional[MetodoPagoTolerante] = Query(None, description="Filtrar por método de pago"),
        fecha_inicio: Optional[date] = Query(None, description="Filtrar por fecha de pago inicial (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Filtrar por fecha de pago final (YYYY-MM-DD)"),
    ):
        self.membresia_id = membresia_id
        self.metodo_pago = metodo_pago
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

class PagoResponse(BaseModel):
    id: int
    membresia_id: int
    monto_pagado: Decimal
    fecha_pago: datetime
    metodo_pago: MetodoPagoTolerante

    model_config = ConfigDict(from_attributes=True)
