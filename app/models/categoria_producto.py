from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class CategoriaProducto(Base):
    """Categoría para clasificar los productos de la tienda (ej. Suplementos, Ropa, Accesorios)."""
    __tablename__ = "categoria_producto"

    id = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    # Relaciones
    producto = relationship("ProductoTienda", back_populates="categoria")
