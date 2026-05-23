from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Numeric, func
import enum
from sqlalchemy.orm import relationship
from app.database.session import Base

class TipoEstado(enum.Enum):
    abierto = "Abierto"
    en_progreso = "En Progreso"
    cerrado = "Cerrado"

class TicketMantenimiento(Base):
    __tablename__ = "ticket_mantenimiento"

    id = Column(Integer, primary_key=True, index=True)
    maquina_id = Column(Integer, ForeignKey("maquina.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_falla = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_resolucion = Column(DateTime(timezone=True), nullable=True) 
    costo_reparacion = Column(Numeric(10, 2), nullable=True)
    estado_ticket = Column(
        Enum(TipoEstado, name="tipo_estado_ticket"), 
        nullable=False, 
        default=TipoEstado.abierto,
        ) 

    #Relaciones
    maquina = relationship("Maquina", back_populates="ticket_mantenimiento")
    usuario = relationship("Usuario", back_populates="ticket_mantenimiento")

    @property
    def nombre_maquina(self) -> str:
        return self.maquina.identificador_interno if self.maquina else ""