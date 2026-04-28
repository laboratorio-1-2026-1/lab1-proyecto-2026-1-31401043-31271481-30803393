from sqlalchemy import Column,  Integer, String
from sqlalchemy.orm import relationship

from app.database.session import Base

class Rol(Base):
    """Representa los diferentes roles que pueden tener los usuarios del sistema, como administrador, entrenador o cliente"""
    __tablename__ = "rol"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="rol")
