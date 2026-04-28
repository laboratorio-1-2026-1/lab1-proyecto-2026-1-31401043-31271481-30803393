from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from app.database.session import Base


class BitacoraAcceso(Base):
    """Registro de accesos de clientes al gimnasio con control de entradas."""
    __tablename__ = "bitacora_acceso"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    fecha_hora_entrada = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    acceso_concedido = Column(Boolean, nullable=False)

    # Relación
    cliente = relationship("Cliente", back_populates="accesos")