from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoUpdateEstado,
    ProductoFilterParams,
    ProductoResponse,
)
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.producto_service import ProductoService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> ProductoService:
    return ProductoService(db)


@router.post("/", response_model=StandardResponse[ProductoResponse], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_producto(schema: ProductoCreate, service: ProductoService = Depends(get_service)):
    res = await service.create_producto(schema=schema)
    return {"status": "success", "message": "Producto registrado exitosamente", "data": res}


@router.get("/", response_model=PaginatedResponse[List[ProductoResponse]])
async def list_productos(
    skip: int = 0,
    limit: int = 100,
    filtros: ProductoFilterParams = Depends(),
    service: ProductoService = Depends(get_service),
):
    total, res = await service.list_productos(filtros=filtros, skip=skip, limit=limit)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.patch("/{id}", response_model=StandardResponse[ProductoResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_producto(id: int, schema: ProductoUpdate, service: ProductoService = Depends(get_service)):
    res = await service.update_producto(id=id, schema=schema)
    return {"status": "success", "message": "Producto actualizado exitosamente", "data": res}


@router.patch("/{id}/estado", response_model=StandardResponse[ProductoResponse],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_producto_estado(id: int, estado_in: ProductoUpdateEstado, service: ProductoService = Depends(get_service)):
    res = await service.update_producto_estado(id=id, schema=estado_in)
    return {"status": "success", "message": "Estado del producto actualizado exitosamente", "data": res}