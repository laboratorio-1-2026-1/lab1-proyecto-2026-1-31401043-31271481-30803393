import enum
from sqlalchemy import Column,  Integer, String , ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base


class TipoEstado(enum.Enum):
    """Estados posibles de una cuenta de usuario."""
    activo = "Activo"
    inactivo = "Inactivo"
    suspendido = "Suspendido"


class Usuario(Base):
    """Usuario del sistema con acceso mediante email y contraseña."""
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.id"), nullable=False)
    estado_cuenta = Column(
        Enum(TipoEstado, name="tipo_estado_usuario"),
        nullable=False,
        default=TipoEstado.activo,
        )

    # Relaciones
    rol = relationship("Rol", back_populates="usuario")
    cliente = relationship("Cliente", back_populates="usuario")
    entrenador = relationship("Entrenador", back_populates="usuario")
    ticket_mantenimiento = relationship("TicketMantenimiento", back_populates="usuario")