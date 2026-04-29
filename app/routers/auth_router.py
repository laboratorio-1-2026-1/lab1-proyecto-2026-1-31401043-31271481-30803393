from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from app.core.deps import get_current_user, get_db
from app.models.usuario import Usuario
from app.schemas.response import StandardResponse
from app.schemas.usuario import UsuarioOut
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()




def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    token = await service.authenticate_user(form_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=StandardResponse[UsuarioOut])
def get_me(current_user: Usuario = Depends(get_current_user)):
    return {"status": "success", "message": "Usuario actual obtenido con éxito", "data": current_user}
