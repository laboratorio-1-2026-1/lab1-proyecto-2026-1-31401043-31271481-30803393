from sqlalchemy import Column,  Integer, ForeignKey , Enum , Date
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum
class EstadoMembresia(enum.Enum):
    """Estados posibles de una membresía de cliente."""
    activa = "Activa"
    por_vencer = "Por Vencer"
    vencida = "Vencida"

class MembresiaCliente(Base):
    """Representa la membresía de un cliente, con información sobre el plan de suscripción, 
    fechas de inicio y fin, estado de la membresía y sus relaciones con el cliente y los pagos realizados."""
    __tablename__ = "membresia_cliente"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plan_suscripcion.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(
        Enum(EstadoMembresia, name="tipo_estado_membresia"),
        nullable=False,
        default=EstadoMembresia.activa
        )

    # Relaciones
    cliente = relationship("Cliente", back_populates="membresia_cliente")
    plan = relationship("PlanSuscripcion", back_populates="membresia_cliente")
    pagos_membresia = relationship("PagoMembresia", back_populates="membresia")

    @property
    def nombre_cliente(self) -> str:
        return f"{self.cliente.nombre} {self.cliente.apellido}" if self.cliente else ""

    @property
    def nombre_plan(self) -> str:
        return self.plan.nombre if self.plan else ""
