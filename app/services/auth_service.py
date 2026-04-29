from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.errors import UnauthorizedException
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import TipoEstado as EstadoCuenta

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UsuarioRepository(db)

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> str:
        user = await self.repo.get_by_email(form_data.username) 
        if not user or user.estado_cuenta is not EstadoCuenta.activo:
            raise UnauthorizedException("Incorrect email or inactive user", error_code="INVALID_CREDENTIALS")
        if not security.verify_password(form_data.password, user.password_hash):
            raise UnauthorizedException("Incorrect password", error_code="INVALID_CREDENTIALS")

        access_token = security.create_access_token(data={"sub": user.email})
        return access_token
