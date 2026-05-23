from sqlalchemy import Column, Integer,  ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class TipoEstado(enum.Enum):
    confirmada = "Confirmada"
    cancelada = "Cancelada"
    asistio = "Asistio"


class Reserva(Base):
    __tablename__ = "reserva"

    id = Column(Integer, primary_key=True, index=True)
    sesion_id = Column(Integer, ForeignKey("sesion_programada.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    estado_reserva = Column(
        Enum(TipoEstado, name="tipo_estado_reserva"), 
        nullable=False, 
        default=TipoEstado.confirmada,
        )

    #Relaciones
    sesion_programada = relationship("SesionProgramada", back_populates="reserva")
    cliente = relationship("Cliente", back_populates="reserva")

    @property
    def nombre_cliente(self) -> str:
        return f"{self.cliente.nombre} {self.cliente.apellido}" if self.cliente else ""

    @property
    def nombre_sesion(self) -> str:
        return self.sesion_programada.nombre if self.sesion_programada else ""

