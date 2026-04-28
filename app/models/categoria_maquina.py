from sqlalchemy import Column,  Integer, String
from sqlalchemy.orm import relationship

from app.database.session import Base

class CategoriaMaquina(Base):
    """Representa las diferentes categorías a las que pueden pertenecer las máquinas en el gimnasio."""
    __tablename__ = "categoria_maquina"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    # Relaciones
    maquina = relationship("Maquina", back_populates="categoria")