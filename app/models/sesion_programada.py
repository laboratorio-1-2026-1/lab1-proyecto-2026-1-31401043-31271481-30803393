from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class TipoEstado(enum.Enum):
    """Estados posibles de una sesión programada en el gimnasio."""
    programada = "Programada"
    en_curso = "En Curso"
    finalizada = "Finalizada"
    cancelada = "Cancelada"


class SesionProgramada(Base):
    """Sesión de entrenamiento grupal o personal agendada con fecha, hora y cupos limitados."""
    __tablename__ = "sesion_programada"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplina.id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenador.id"), nullable=False)
    zona_id = Column(Integer, ForeignKey("zona_instalacion.id"), nullable=False)
    fecha_hora_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_hora_fin = Column(DateTime(timezone=True), nullable=False)
    cupo_maximo = Column(Integer, nullable=False)
    estado_sesion = Column(
        Enum(TipoEstado, name="tipo_estado_sesion"),
        nullable=False,
        default=TipoEstado.programada,
        )

    # Relaciones
    disciplina = relationship("Disciplina", back_populates="sesion_programada")
    entrenador = relationship("Entrenador", back_populates="sesion_programada")
    zona = relationship("ZonaInstalacion", back_populates="sesion_programada")
    reserva = relationship("Reserva", back_populates="sesion_programada")
    
