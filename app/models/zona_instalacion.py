from sqlalchemy import Column,  Integer, String , Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class TipoEstado(enum.Enum):
    """Estados posibles de una zona de instalación."""
    activa = "Activa"
    inactiva = "Inactiva"
    mantenimiento = "Mantenimiento"
    cerrada = "Cerrada"


class ZonaInstalacion(Base):
    """Zona dentro de las instalaciones (ej. gimnasio, cancha, sala) que alberga máquinas o actividades."""
    __tablename__ = "zona_instalacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_zona = Column(String, nullable=False, unique=True)
    capacidad_maxima = Column(Integer, nullable=False)
    estado_zona = Column(
        Enum(TipoEstado, name="tipo_estado_zona_instalacion"),
        nullable=False,
        default=TipoEstado.activa,
    )

    # Relaciones
    maquina = relationship("Maquina", back_populates="zona")
    sesion_programada = relationship("SesionProgramada", back_populates="zona")