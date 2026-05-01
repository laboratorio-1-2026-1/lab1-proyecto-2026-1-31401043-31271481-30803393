from pydantic import BaseModel, ConfigDict, Field, BeforeValidator, model_validator, AwareDatetime, field_validator
from typing import Annotated, Optional
from datetime import  date, datetime, timezone
from fastapi import Query

from app.models.sesion_programada import TipoEstado


def mapear_estado_sesion(v: str) -> str:
    if isinstance(v, str):
        v_lower = v.strip().lower()
        mapping = {
            "programada": "Programada",
            "en curso": "En Curso",
            "finalizada": "Finalizada",
            "cancelada": "Cancelada",
        }
        return mapping.get(v_lower, v.capitalize())
    return v


EstadoSesionTolerante = Annotated[TipoEstado, BeforeValidator(mapear_estado_sesion)]


class SesionCreate(BaseModel):
    disciplina_id: int = Field(..., description="ID de la disciplina")
    entrenador_id: int = Field(..., description="ID del entrenador")
    zona_id: int = Field(..., description="ID de la zona de instalación")
    fecha_hora_inicio: datetime= Field(..., description="Fecha y hora de inicio (YYYY-MM-DD HH:MM:SS)")
    fecha_hora_fin: datetime = Field(..., description="Fecha y hora de fin (YYYY-MM-DD HH:MM:SS)")
    cupo_maximo: int = Field(..., gt=0, description="Cupo máximo de participantes")

    @field_validator("fecha_hora_inicio", "fecha_hora_fin")
    @classmethod
    def asegurar_zona_horaria(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            # Si viene sin zona horaria, asumimos que es UTC
            return v.replace(tzinfo=timezone.utc)
        # Si ya trae su zona horaria (como la Z al final), la dejamos pasar normal
        return v
    
    @model_validator(mode="after")
    def validar_rango_horario(self) -> "SesionCreate":
        if self.fecha_hora_fin <= self.fecha_hora_inicio:
            raise ValueError("La fecha_hora_fin debe ser posterior a fecha_hora_inicio")
        return self


class SesionUpdateEstado(BaseModel):
    estado_sesion: EstadoSesionTolerante = Field(
        ..., description="Nuevo estado de la sesión (Programada, En Curso, Finalizada, Cancelada)"
    )


class SesionFilterParams:
    """Filtros para GET /sesiones (vista general)."""
    def __init__(
        self,
        fecha: Optional[date] = Query(None, description="Filtrar por fecha específica (YYYY-MM-DD)"),
        disciplina_id: Optional[int] = Query(None, description="Filtrar por ID de disciplina"),
        entrenador_id: Optional[int] = Query(None, description="Filtrar por ID de entrenador"),
        estado_sesion: Optional[EstadoSesionTolerante] = Query(None, description="Filtrar por estado"),
    ):
        self.fecha = fecha
        self.disciplina_id = disciplina_id
        self.entrenador_id = entrenador_id
        self.estado_sesion = estado_sesion


class MisSesionesFilterParams:
    """Filtros para GET /sesiones/me (vista del entrenador autenticado)."""
    def __init__(
        self,
        fecha_inicio: Optional[date] = Query(None, description="Filtrar desde esta fecha (YYYY-MM-DD)"),
        fecha_fin: Optional[date] = Query(None, description="Filtrar hasta esta fecha (YYYY-MM-DD)"),
        estado_sesion: Optional[EstadoSesionTolerante] = Query(None, description="Filtrar por estado"),
    ):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado_sesion = estado_sesion


class SesionResponse(BaseModel):
    id: int
    disciplina_id: int
    entrenador_id: int
    zona_id: int
    fecha_hora_inicio: AwareDatetime
    fecha_hora_fin: AwareDatetime
    cupo_maximo: int
    estado_sesion: EstadoSesionTolerante

    model_config = ConfigDict(from_attributes=True)
