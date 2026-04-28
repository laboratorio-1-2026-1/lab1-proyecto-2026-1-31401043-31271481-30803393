from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database.session import Base
import enum


class MetodoPago(enum.Enum):
    """Métodos de pago aceptados en la tienda."""
    efectivo = "Efectivo"
    tarjeta = "Tarjeta"
    transferencia = "Transferencia"


class VentaTienda(Base):
    """Transacción de venta en la tienda de productos y suplementos."""
    __tablename__ = "venta_tienda"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    fecha_venta = Column(DateTime(timezone=True), nullable=False)
    total_venta = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(
        Enum(MetodoPago, name="tipo_metodo_pago"), 
        nullable=False
        )

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas_tienda")
    detalle_ventas = relationship("DetalleVenta", back_populates="venta_tienda")
