from typing import List, Optional, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.maquina import Maquina
from app.models.ticket_mantenimiento import TicketMantenimiento , TipoEstado
from app.repositories.base_repository import BaseRepository


class MaquinaRepository(BaseRepository[Maquina]):
    def __init__(self, db: AsyncSession):
        super().__init__(Maquina, db)

    async def get_by_id_with_relations(self, id: int) -> Optional[Maquina]:
        result = await self.db.execute(
            select(Maquina)
            .options(
                selectinload(Maquina.categoria),
                selectinload(Maquina.zona)
            )
            .where(Maquina.id == id)
        )
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[dict] = None) -> Tuple[int, List[Maquina]]:
        query = select(Maquina).options(
            selectinload(Maquina.categoria),
            selectinload(Maquina.zona)
        )
        if filters:
            for key, value in filters.items():
                if value is not None and hasattr(Maquina, key):
                    if isinstance(value, str):
                        query = query.where(getattr(Maquina, key).ilike(f"%{value}%"))
                    else:
                        query = query.where(getattr(Maquina, key) == value)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        query = query.offset(skip).limit(limit)
        results = await self.db.execute(query)
        return total, list(results.scalars().all())

    async def get_by_identificador_interno(self, identificador_interno: str) -> Maquina | None:
        # Buscar la máquina por su identificador interno
        result = await self.db.execute(
            select(Maquina).where(Maquina.identificador_interno == identificador_interno)
        )
        return result.scalars().first()
    
    async def activar_maquina(self, maquina_id: int):
    # Buscar tickets abiertos para esta máquina
        ticket_abierto = await self.db.execute(
            select(TicketMantenimiento).where(
                TicketMantenimiento.maquina_id == maquina_id,
                TicketMantenimiento.estado == TipoEstado.abierto
            )
        )
        return ticket_abierto.scalars().first()