from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from typing import Annotated, Optional
from fastapi import Query

from app.models.disciplina import TipoEstado


def mapear_estado_disciplina(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        if v_lower == "activa":
            return "Activa"
        if v_lower == "inactiva":
            return "Inactiva"
        return v.capitalize()
    return v


EstadoDisciplinaTolerante = Annotated[TipoEstado, BeforeValidator(mapear_estado_disciplina)]


class DisciplinaBase(BaseModel):
    nombre_disciplina: str = Field(..., min_length=1, max_length=100, description="Nombre de la disciplina")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción de la disciplina")


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaUpdate(BaseModel):
    """Actualización parcial de la disciplina (solo campos editables, excluyendo estado)."""
    descripcion: Optional[str] = Field(None, max_length=500, description="Nueva descripción de la disciplina")


class DisciplinaUpdateEstado(BaseModel):
    estado_disciplina: EstadoDisciplinaTolerante = Field(
        ..., description="Nuevo estado de la disciplina (Activa, Inactiva)"
    )


class DisciplinaFilterParams:
    def __init__(
        self,
        estado_disciplina: Optional[EstadoDisciplinaTolerante] = Query(
            None, description="Filtrar por estado de la disciplina (Activa, Inactiva)"
        ),
    ):
        self.estado_disciplina = estado_disciplina


class DisciplinaResponse(DisciplinaBase):
    id: int
    estado_disciplina: EstadoDisciplinaTolerante

    model_config = ConfigDict(from_attributes=True)
