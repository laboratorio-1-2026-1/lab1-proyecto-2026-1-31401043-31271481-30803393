from sqlalchemy import Column,  Integer, String , ForeignKey , Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class TipoEstado(enum.Enum):
    """Estados posibles de un entrenador."""
    activo = "Activo"
    inactivo = "Inactivo"
    vacaciones = "Vacaciones"

class Entrenador(Base):
    """Representa a los entrenadores del gimnasio, con información personal, su especialidad y su estado laboral."""
    __tablename__ = "entrenador"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False, unique=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    estado_laboral = Column(
        Enum(TipoEstado, name="tipo_estado_entrenador"), 
        nullable=False,
        default=TipoEstado.activo
        )  
    
    #Relaciones
    usuario = relationship("Usuario", back_populates="entrenador")
    sesion_programada = relationship("SesionProgramada", back_populates="entrenador")
    evaluacion_biometrica = relationship("EvaluacionBiometrica", back_populates="entrenador")