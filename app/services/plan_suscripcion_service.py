from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.plan_suscripcion import PlanSuscripcion
from app.repositories.plan_suscripcion_repository import PlanSuscripcionRepository
from app.schemas.plan_suscripcion import PlanCreate, PlanUpdate, PlanUpdateEstado


class PlanSuscripcionService:
    def __init__(self, db: AsyncSession):
        self.repo = PlanSuscripcionRepository(db)

    async def create_plan(self, schema: PlanCreate) -> PlanSuscripcion:
        # Verificar unicidad del nombre
        existente = await self.repo.get_by_nombre_plan(schema.nombre_plan)
        if existente:
            raise AppException(
                detail="El nombre del plan ya está registrado",
                error_code="PLAN_NAME_EXISTS",
                status_code=409
            )
        return await self.repo.create(schema.model_dump())

    async def update_plan(self, id: int, schema: PlanUpdate) -> PlanSuscripcion:
        plan = await self.repo.get_by_id(id)
        if not plan:
            raise NotFoundException(detail="Plan de suscripción no encontrado", error_code="PLAN_NOT_FOUND")

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return plan

        # Si se intenta cambiar el nombre, verificar unicidad contra otros planes
        if "nombre_plan" in update_data:
            existente = await self.repo.get_by_nombre_plan(update_data["nombre_plan"])
            if existente and existente.id != id:
                raise AppException(
                    detail="El nombre del plan ya está en uso por otro plan",
                    error_code="PLAN_NAME_EXISTS",
                    status_code=409
                )

        return await self.repo.update(db_obj=plan, obj_in_data=update_data)

    async def update_plan_estado(self, id: int, schema: PlanUpdateEstado) -> PlanSuscripcion:
        plan = await self.repo.get_by_id(id)
        if not plan:
            raise NotFoundException(detail="Plan de suscripción no encontrado", error_code="PLAN_NOT_FOUND")

        if plan.estado_plan == schema.estado_plan:
            return plan

        return await self.repo.update(db_obj=plan, obj_in_data=schema.model_dump(exclude_unset=True))

    async def list_planes(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)
