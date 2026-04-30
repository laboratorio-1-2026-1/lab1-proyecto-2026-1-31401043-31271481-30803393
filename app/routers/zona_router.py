from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.zona import ZonaCreate, ZonaResponse, ZonaUpdateEstado
from app.schemas.response import StandardResponse
from app.services.zona_service import ZonaService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ZonaService:
    return ZonaService(db)


@router.post("/", response_model=StandardResponse[ZonaResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_zona(zona_in: ZonaCreate, service: ZonaService = Depends(get_service)):
    res = await service.create_zona(schema=zona_in)
    return {"status": "success", "message": "Zona registrada exitosamente", "data": res}


@router.get("/", response_model=StandardResponse[List[ZonaResponse]])
async def list_zonas(skip: int = 0, limit: int = 100, service: ZonaService = Depends(get_service)):
    total, zonas = await service.list_zonas(skip=skip, limit=limit)
    return {"status": "success", "message": "Operación completada con éxito", "data": zonas}


@router.patch("/{id}/estado", response_model=StandardResponse[ZonaResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_estado_zona(id: int, estado_in: ZonaUpdateEstado, service: ZonaService = Depends(get_service)):
    res = await service.update_zona_estado(id=id, schema=estado_in)
    return {"status": "success", "message": "Estado de la zona actualizado exitosamente", "data": res}
