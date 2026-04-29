from pydantic import BaseModel, ConfigDict
from typing import  Optional
class RoleBase(BaseModel):
    nombre: str
    descripcion: str

class RoleFilterParams:
    pass
class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    descripcion: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)