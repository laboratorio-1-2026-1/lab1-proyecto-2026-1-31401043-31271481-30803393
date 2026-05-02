from decimal import Decimal
from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class EvaluacionCreate(BaseModel):
    cliente_id: int = Field(..., description="ID del cliente evaluado")
    peso: Decimal = Field(..., gt=0, description="Peso en kg")
    estatura: Decimal = Field(..., gt=0, description="Estatura en metros")
    porcentaje_grasa: Decimal = Field(..., ge=0, le=100, description="Porcentaje de grasa corporal (0-100)")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones del entrenador")
    # entrenador_id se extrae del token JWT, no se expone en el payload


class EvaluacionUpdate(BaseModel):
    """Corrección parcial de métricas — solo campos editables post-registro."""
    peso: Optional[Decimal] = Field(None, gt=0, description="Peso en kg")
    estatura: Optional[Decimal] = Field(None, gt=0, description="Estatura en metros")
    porcentaje_grasa: Optional[Decimal] = Field(None, ge=0, le=100, description="Porcentaje de grasa corporal")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones corregidas")


class EvaluacionFilterParams:
    """Filtros para GET /evaluaciones (vista entrenador/admin — cliente_id recomendado)."""
    def __init__(
        self,
        cliente_id: Optional[int] = Query(None, description="ID del cliente a consultar"),
        fecha_inicio: Optional[date] = Query(None, description="Desde esta fecha (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Hasta esta fecha (YYYY-MM-DD)"),
    ):
        self.cliente_id = cliente_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class MisEvaluacionesFilterParams:
    """Filtros para GET /evaluaciones/me (vista del cliente autenticado)."""
    def __init__(
        self,
        fecha_inicio: Optional[date] = Query(None, description="Desde esta fecha (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Hasta esta fecha (YYYY-MM-DD)"),
    ):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class EvaluacionResponse(BaseModel):
    id: int
    cliente_id: int
    entrenador_id: int
    fecha_evaluacion: date
    peso: Decimal
    estatura: Decimal
    porcentaje_grasa: Decimal
    observaciones: Optional[str]

    model_config = ConfigDict(from_attributes=True)
