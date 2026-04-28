from sqlalchemy import Column,  Integer, String , ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database.session import Base

class Cliente(Base):
    """Representa a los clientes del gimnasio, con información personal y sus relaciones con otras entidades como membresías, 
    evaluaciones biométricas, reservas, etc."""
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False, unique=True)
    cedula = Column(String, nullable=False, unique=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    
    #Relaciones
    usuario = relationship("Usuario", back_populates="cliente")
    membresia_cliente = relationship("MembresiaCliente", back_populates="cliente")
    evaluacion_biometrica = relationship("EvaluacionBiometrica", back_populates="cliente")
    accesos = relationship("BitacoraAcceso", back_populates="cliente")
    reserva = relationship("Reserva", back_populates="cliente")
    ventas_tienda = relationship("VentaTienda", back_populates="cliente")