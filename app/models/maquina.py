from sqlalchemy import Column,  Integer, String , ForeignKey , Enum
import enum
from sqlalchemy.orm import relationship
from app.database.session import Base

class TipoEstadoMaquina(enum.Enum):
    """Estados posibles de una máquina en el gimnasio."""
    activa = "Activa"
    en_mantenimiento = "En Mantenimiento"
    fuera_de_servicio = "Fuera de Servicio"

class Maquina(Base):
    """Representa las máquinas del gimnasio, con información sobre su categoría, 
    zona de instalación, estado operativo y detalles técnicos."""
    __tablename__ = "maquina"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categoria_maquina.id"), nullable=False)
    zona_id = Column(Integer, ForeignKey("zona_instalacion.id"), nullable=False)
    identificador_interno = Column(String, nullable=False, unique=True)
    nombre = Column(String, nullable=False)
    descripcion_tecnica = Column(String, nullable=False)
    estado_operativo = Column(
        Enum(TipoEstadoMaquina, name="tipo_estado_maquina"), 
        nullable=False, default=TipoEstadoMaquina.activa
        )

    #Relaciones
    categoria = relationship("CategoriaMaquina", back_populates="maquina")
    zona = relationship("ZonaInstalacion", back_populates="maquina")
    ticket_mantenimiento = relationship("TicketMantenimiento", back_populates="maquina")

    @property
    def nombre_categoria(self) -> str:
        return self.categoria.nombre_categoria if self.categoria else ""

    @property
    def nombre_zona(self) -> str:
        return self.zona.nombre_zona if self.zona else ""