from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.session import Base


class DetalleVenta(Base):
    """Línea individual de una venta, representando un producto con su precio en ese momento."""
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("venta_tienda.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("producto_tienda.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_historico = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    venta_tienda = relationship("VentaTienda", back_populates="detalle_ventas")
    producto_tienda = relationship("ProductoTienda", back_populates="detalle_ventas")