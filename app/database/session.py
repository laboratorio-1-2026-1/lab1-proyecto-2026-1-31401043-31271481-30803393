from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# Configuración de la base de datos utilizando SQLAlchemy con soporte asíncrono. 
# Se crea un motor de base de datos asíncrono y una fábrica de sesiones para manejar las conexiones a la base de datos. 
engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# Dependencia para inyectar la BD en los endpoints
async def get_db():
    async with SessionLocal() as db:
        yield db
