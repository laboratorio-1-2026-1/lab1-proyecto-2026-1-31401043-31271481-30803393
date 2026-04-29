from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_roles
from app.core.pagination import PaginationParams
from app.schemas.roles import RoleFilterParams, RoleOut
from app.schemas.response import  PaginatedResponse
from app.services.rol_service import RolService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> RolService:
    return RolService(db)


@router.get("/", response_model=PaginatedResponse[List[RoleOut]],
            dependencies=[Depends(require_roles("Administrador"))])
async def list_roles(
    pagination: PaginationParams = Depends(),
    filtros: RoleFilterParams = Depends(),
    service: RolService = Depends(get_service)
):
    filters_dict = {k: v for k, v in filtros.__dict__.items() if v is not None}
    total, res = await service.list_all(skip=pagination.skip, limit=pagination.limit, filters=filters_dict)
    return {
        "status": "success",
        "message": "Operación completada con éxito",
        "data": res,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit
    }
