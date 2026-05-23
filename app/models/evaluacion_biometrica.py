from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class EvaluacionBiometrica(Base):
    """Representa las evaluaciones biométricas realizadas a los clientes por parte de los entrenadores, 
    conteniendo con información sobre peso, estatura, porcentaje de grasa y observaciones."""
    __tablename__ = "evaluacion_biometrica"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenador.id"), nullable=False)
    fecha_evaluacion = Column(Date, server_default=func.current_date(), nullable=False)
    peso = Column(Numeric(10, 2), nullable=False)
    estatura = Column(Numeric(10, 2), nullable=False)
    porcentaje_grasa = Column(Numeric(10, 2), nullable=False)
    observaciones = Column(String, nullable=True)

    #Relaciones
    cliente = relationship("Cliente", back_populates="evaluacion_biometrica")
    entrenador = relationship("Entrenador", back_populates="evaluacion_biometrica")

    @property
    def nombre_cliente(self) -> str:
        return f"{self.cliente.nombre} {self.cliente.apellido}" if self.cliente else ""

    @property
    def nombre_entrenador(self) -> str:
        return f"{self.entrenador.nombre} {self.entrenador.apellido}" if self.entrenador else ""

