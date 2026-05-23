from datetime import date, datetime, timezone, time
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.bitacora_acceso import BitacoraAcceso
from app.repositories.base_repository import BaseRepository


class AccesoRepository(BaseRepository[BitacoraAcceso]):
    def __init__(self, db: AsyncSession):
        super().__init__(BitacoraAcceso, db)

    async def get_by_id_with_relations(self, id: int) -> Optional[BitacoraAcceso]:
        result = await self.db.execute(
            select(BitacoraAcceso)
            .options(selectinload(BitacoraAcceso.cliente))
            .where(BitacoraAcceso.id == id)
        )
        return result.scalars().first()

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        acceso_concedido: Optional[bool] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
    ) -> Tuple[int, List[BitacoraAcceso]]:
        """Bitácora histórica con filtros de fecha, cliente y resultado de acceso."""
        conditions = []

        if cliente_id is not None:
            conditions.append(BitacoraAcceso.cliente_id == cliente_id)
        if acceso_concedido is not None:
            conditions.append(BitacoraAcceso.acceso_concedido == acceso_concedido)
        if fecha_inicio is not None:
            # Combinamos fecha_inicio con el primer segundo del día y zona UTC
            inicio = datetime.combine(fecha_inicio, time.min, tzinfo=timezone.utc)
            conditions.append(BitacoraAcceso.fecha_hora_entrada >= inicio)
            
        if fecha_fin is not None:
            # Combinamos fecha_fin con el último microsegundo del día y zona UTC
            fin = datetime.combine(fecha_fin, time.max, tzinfo=timezone.utc)
            conditions.append(BitacoraAcceso.fecha_hora_entrada <= fin)

        query = select(BitacoraAcceso).options(selectinload(BitacoraAcceso.cliente))
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(BitacoraAcceso.fecha_hora_entrada.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())
