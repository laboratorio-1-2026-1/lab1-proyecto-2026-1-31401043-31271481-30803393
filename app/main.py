import app.models # Importar modelos para que SQLAlchemy los reconozca y cree las tablas correspondientes
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import setup_exception_handlers 
from app.middlewares.logging_middleware import LoggingMiddleware
#from app.seed import init_seed_data para cuando se tengan disponibles los datos semilla
from app.routers import (
    auth_router,
    rol_router,
    usuario_router,
    cliente_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creación de tablas de forma ASÍNCRONA 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    
    
    # Ejecutar lógica de datos semilla
    
    
    #await init_seed_data()
    
    yield

app = FastAPI(
    title="SmartGym API",
    description="API Restful implementando arquitectura de capas con FastAPI, SQLAlchemy y JWT",
    version="1.0.0",
    lifespan=lifespan,
)

# configurar Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)  # Loguea en consola la petición

# Setup Exception Handlers
setup_exception_handlers(app)

# Configurar Routers
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(rol_router.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(usuario_router.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(cliente_router.router, prefix="/api/v1/clientes", tags=["Clientes"])