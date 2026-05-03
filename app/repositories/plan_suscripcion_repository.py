from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan_suscripcion import PlanSuscripcion
from app.repositories.base_repository import BaseRepository


class PlanSuscripcionRepository(BaseRepository[PlanSuscripcion]):
    def __init__(self, db: AsyncSession):
        super().__init__(PlanSuscripcion, db)

    async def get_by_nombre_plan(self, nombre: str) -> PlanSuscripcion | None:
        #Busca un plan por nombre (insensible a mayúsculas) para validar unicidad
        result = await self.db.execute(
            select(self.model).where(self.model.nombre_plan.ilike(nombre))
        )
        return result.scalars().first()
