from sqlalchemy import Column, Integer, String, Numeric , Enum
from sqlalchemy.orm import relationship

from app.database.session import Base
import enum
class EstadoPlan(enum.Enum):
    """Estados posibles de un plan de suscripción en el gimnasio."""
    activo = "Activo"
    archivado = "Archivado"

class PlanSuscripcion(Base):
    """Representa los planes de suscripción disponibles en el gimnasio, 
    con información sobre su costo, duración, descripción y estado de disponibilidad."""
    __tablename__ = "plan_suscripcion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_plan = Column(String, unique=True, nullable=False)
    costo_actual = Column(Numeric(10, 2), nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)
    estado_plan = Column(
        Enum(EstadoPlan, name="tipo_estado_plan"), 
        nullable=False, 
        default=EstadoPlan.activo
        )

    #Relaciones
    membresia_cliente = relationship("MembresiaCliente", back_populates="plan")
