from decimal import Decimal
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.models.plan_suscripcion import EstadoPlan


def mapear_estado_plan(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "activo": "Activo",
            "archivado": "Archivado",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoPlanTolerante = Annotated[EstadoPlan, BeforeValidator(mapear_estado_plan)]


class PlanBase(BaseModel):
    nombre_plan: str = Field(..., min_length=1, max_length=100, description="Nombre del plan de suscripción")
    costo_actual: Decimal = Field(..., gt=0, description="Costo actual del plan")
    duracion_dias: int = Field(..., gt=0, description="Duración del plan en días")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción del plan")


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    """Actualización parcial del plan (campos editables, excluyendo estado)."""
    nombre_plan: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del plan")
    costo_actual: Optional[Decimal] = Field(None, gt=0, description="Nuevo costo del plan")
    duracion_dias: Optional[int] = Field(None, gt=0, description="Nueva duración en días")
    descripcion: Optional[str] = Field(None, max_length=500, description="Nueva descripción")


class PlanUpdateEstado(BaseModel):
    estado_plan: EstadoPlanTolerante = Field(
        ..., description="Nuevo estado del plan (Activo, Archivado)"
    )


class PlanFilterParams:
    def __init__(
        self,
        estado_plan: Optional[EstadoPlanTolerante] = Query(None, description="Filtrar por estado (Activo, Archivado)"),
    ):
        self.estado_plan = estado_plan


class PlanResponse(PlanBase):
    id: int
    estado_plan: EstadoPlanTolerante

    model_config = ConfigDict(from_attributes=True)
