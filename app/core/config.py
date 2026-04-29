import os
import sys
from dotenv import load_dotenv

load_dotenv()
# Debug: Imprime la URL de la base de datos para verificar que se ha cargado correctamente
print("=======================================")
print("DEBUG URL:", os.getenv("DATABASE_URL"))
print("=======================================")


# --------------------------------------

class Settings:
    # Intentamos obtener la clave
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Si es None, lanzamos un error crítico
    if not SECRET_KEY:
        print("RROR CRÍTICO: No se encontró la variable SECRET_KEY en el entorno.")
        # Detenemos la ejecución del servidor porque no es seguro continuar
        sys.exit(1) 

    # Lo mismo para la base de datos
    _raw_url = os.getenv("DATABASE_URL")
    if not _raw_url:
        print("ERROR CRÍTICO: DATABASE_URL no definida.")
        sys.exit(1)

    DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()

