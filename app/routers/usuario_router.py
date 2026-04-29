from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate, UsuarioFilterParams
from app.schemas.response import StandardResponse, PaginatedResponse
from app.services.usuario_service import UsuarioService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> UsuarioService:
    return UsuarioService(db)


@router.post("/", response_model=StandardResponse[UsuarioOut], status_code=status.HTTP_201_CREATED,
            dependencies=[Depends(require_roles("Administrador"))])
async def create_usuario(schema: UsuarioCreate, service: UsuarioService = Depends(get_service)):
    res = await service.create_usuario(schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}


@router.get("/", response_model=PaginatedResponse[List[UsuarioOut]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_usuarios(
    pagination: PaginationParams = Depends(),
    filtros: UsuarioFilterParams = Depends(),
    service: UsuarioService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_usuarios(skip=pagination.skip, limit=pagination.limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }


@router.patch("/{id}/estado", response_model=StandardResponse[UsuarioOut],
            dependencies=[Depends(require_roles("Administrador"))])
async def update_usuario_estado(id: int, schema: UsuarioUpdate, service: UsuarioService = Depends(get_service)):
    res = await service.update_usuario(id, schema)
    return {"status": "success", "message": "Operación completada con éxito", "data": res}
