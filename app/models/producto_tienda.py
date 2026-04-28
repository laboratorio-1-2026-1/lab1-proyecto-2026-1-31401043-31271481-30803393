from sqlalchemy import Column, Integer, String, ForeignKey, Numeric , Enum
from sqlalchemy.orm import relationship

from app.database.session import Base
import enum


class EstadoProducto(enum.Enum):
    """Estado de disponibilidad de un producto en la tienda."""
    activo = "Activo"
    descontinuado = "Descontinuado"


class ProductoTienda(Base):
    """Producto disponible para venta en la tienda de suplementos/accesorios."""
    __tablename__ = "producto_tienda"

    id = Column(Integer, primary_key=True, index=True)
    categoria_producto_id = Column(Integer, ForeignKey("categoria_producto.id"), nullable=False)
    nombre_producto = Column(String, nullable=False)
    precio_actual = Column(Numeric(10, 2), nullable=False)
    stock_disponible = Column(Integer, nullable=False)
    estado_producto = Column(
        Enum(EstadoProducto, name="tipo_estado_producto"),
        nullable=False,
        default=EstadoProducto.activo,
        )

    # Relaciones
    categoria = relationship("CategoriaProducto", back_populates="producto")
    detalle_ventas = relationship("DetalleVenta", back_populates="producto_tienda")
    