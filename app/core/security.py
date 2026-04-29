from datetime import datetime, timedelta, timezone

import jwt 
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #verifica si la contraseña sin hash coincide con la contraseña hash almacenada utilizando el contexto de PassLib.
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # genera un hash de la contraseña utilizando el contexto de Passlib.
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    #crea un token de acceso utilizando JWT. Con informacion de su experiacion y firma con la clave secreta definida en la configuración.
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
