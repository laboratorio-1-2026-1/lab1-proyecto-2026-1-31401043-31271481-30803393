from datetime import date
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluacion_biometrica import EvaluacionBiometrica
from app.repositories.base_repository import BaseRepository


class EvaluacionBiometricaRepository(BaseRepository[EvaluacionBiometrica]):
    def __init__(self, db: AsyncSession):
        super().__init__(EvaluacionBiometrica, db)

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ) -> Tuple[int, List[EvaluacionBiometrica]]:
        #Listado con filtros de fecha y cliente. Ordenado cronológicamente ASC.
        conditions = []

        if cliente_id is not None:
            conditions.append(EvaluacionBiometrica.cliente_id == cliente_id)
        if fecha_inicio is not None:
            conditions.append(EvaluacionBiometrica.fecha_evaluacion >= fecha_inicio)
        if fecha_fin is not None:
            conditions.append(EvaluacionBiometrica.fecha_evaluacion <= fecha_fin)

        query = select(EvaluacionBiometrica)
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(EvaluacionBiometrica.fecha_evaluacion.asc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())
