from sqlalchemy import Column,  Integer, String , Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class TipoEstado(enum.Enum):
    """Estados posibles de una disciplina."""
    activa = "Activa"
    inactiva = "Inactiva"

class Disciplina(Base):
    """Representa las diferentes disciplinas que se ofrecen en el gimnasio."""
    __tablename__ = "disciplina"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_disciplina = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)
    estado_disciplina = Column(
        Enum(TipoEstado, name="tipo_estado_disciplina"), 
        nullable=False, 
        default=TipoEstado.activa
        )
    
    # Relaciones
    sesion_programada = relationship("SesionProgramada", back_populates="disciplina")
