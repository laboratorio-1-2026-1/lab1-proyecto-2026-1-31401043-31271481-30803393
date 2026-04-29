from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security
from app.core.config import settings
from app.database.session import get_db
from app.models.usuario import Usuario
from app.models.usuario import TipoEstado as EstadoCuenta

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TokenDep = Annotated[str, Depends(reusable_oauth2)]
SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(session: SessionDep, token: TokenDep) -> Usuario:
    # Importando aqui para evitar dependencia circular si es necesario
    from app.repositories.usuario_repository import UsuarioRepository

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    except (jwt.PyJWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e

    user = await UsuarioRepository(session).get_by_email_with_relations(email=token_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Chequeamos el estado de la cuenta. Si está inactiva o suspendida, no permitimos el acceso.
    if user.estado_cuenta is EstadoCuenta.inactivo or user.estado_cuenta is EstadoCuenta.suspendido:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


# Función para verificar roles. Permite especificar uno o más roles requeridos para acceder a una ruta.
def require_roles(*role_names: str):
    def role_dependency(current_user: Usuario = Depends(get_current_user)):
        role_name = current_user.rol.nombre if current_user.rol else None
        
        #if role_name == "SUPER_ADMIN": # Permitir acceso total a SUPER_ADMIN sin importar los roles requeridos se podria implementar esta logica aqui
            #return current_user
        
        if role_name not in role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The user doesn't have enough privileges. Requires one of: {', '.join(role_names)}",
            )
        return current_user

    return role_dependency
