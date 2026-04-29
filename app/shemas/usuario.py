from pydantic import BaseModel, Field, EmailStr, BeforeValidator, ConfigDict
from typing import  Optional, Annotated
from fastapi import Query
from app.models.usuario import TipoEstado

def capitalizar_estado(v: str) -> str:
    if isinstance(v, str):
        return v.capitalize() # Pasa "activo" -> "Activo"
    return v

EstadoTolerante = Annotated[TipoEstado, BeforeValidator(capitalizar_estado)]

class UsuarioBase(BaseModel):
    email : EmailStr = Field(..., min_length=1, max_length=100, description="Correo electrónico del usuario")
    rol_id : int = Field(..., ge=1, description="ID del rol asociado al usuario")
class UsuarioFilterParams:
    def __init__(
        self,
        rol_id: Optional[int] = Query(None, description="Filtrar por ID de rol"),
        estado_cuenta: Optional[EstadoTolerante] = Query(
            None,  
            description="Filtrar por estado de cuenta (Activo, Inactivo, Suspendido)"
        ),
        email: Optional[str] = Query(None, description="Filtrar por correo electrónico")
    ):
        self.rol_id = rol_id
        self.estado_cuenta = estado_cuenta
        self.email = email


class UsuarioCreate(UsuarioBase):
    password : str = Field(..., min_length=8, description="Contraseña del usuario, mínimo 8 caracteres")

class UsuarioUpdate(BaseModel):
    estado_cuenta: EstadoTolerante = Field(
        ..., 
        description="Nuevo estado de cuenta (Activo, Inactivo, Suspendido)"
    )

class UsuarioOut(UsuarioBase):
    id: int
    estado_cuenta: EstadoTolerante

    model_config = ConfigDict(from_attributes=True)