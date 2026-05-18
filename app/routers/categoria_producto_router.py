from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.categoria_producto import (
    CategoriaProductoCreate, 
    CategoriaProductoUpdate, 
    CategoriaProductoResponse
    )
from app.schemas.response import StandardResponse
from app.services.categoria_producto_service import CategoriaProductoService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> CategoriaProductoService:
    return CategoriaProductoService(db)


@router.post("/", response_model=StandardResponse[CategoriaProductoResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_categoria_producto(schema: CategoriaProductoCreate, service: CategoriaProductoService = Depends(get_service)):
    res = await service.create_categoria(schema=schema)
    return {"status": "success", "message": "Categoría de producto creada exitosamente", "data": res}


@router.get("/", response_model=StandardResponse[List[CategoriaProductoResponse]])
async def list_categorias_producto(
    skip: int = 0,
    limit: int = 100,
    service: CategoriaProductoService = Depends(get_service),
):
    total, res = await service.list_categorias(skip=skip, limit=limit)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.patch("/{id}", response_model=StandardResponse[CategoriaProductoResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_categoria_producto(id: int, schema: CategoriaProductoUpdate, service: CategoriaProductoService = Depends(get_service)):
    res = await service.update_categoria(id=id, schema=schema)
    return {"status": "success", "message": "Categoría de producto actualizada exitosamente", "data": res}