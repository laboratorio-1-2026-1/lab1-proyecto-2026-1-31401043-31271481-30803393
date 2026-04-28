from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum

class MetodoPago(enum.Enum):
    """Métodos de pago disponibles para el pago de membresías."""
    efectivo = "Efectivo"
    tarjeta = "Tarjeta"
    transferencia = "Transferencia"
class PagoMembresia(Base):
    """Representa los pagos realizados por los clientes para sus membresías, 
    con información sobre el monto pagado, fecha de pago y método de pago utilizado."""
    __tablename__ = "pago_membresia"

    id = Column(Integer, primary_key=True, index=True)
    membresia_id = Column(Integer, ForeignKey("membresia_cliente.id"), nullable=False)
    monto_pagado = Column(Numeric(10, 2), nullable=False)
    fecha_pago = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metodo_pago = Column(
        Enum(MetodoPago, name="tipo_metodo_pago"),  
        nullable=False
        )

    #Relaciones
    membresia = relationship("MembresiaCliente", back_populates="pagos_membresia")