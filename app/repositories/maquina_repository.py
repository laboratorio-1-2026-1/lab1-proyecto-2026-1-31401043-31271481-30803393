from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.maquina import Maquina
from app.models.ticket_mantenimiento import TicketMantenimiento , TipoEstado
from app.repositories.base_repository import BaseRepository


class MaquinaRepository(BaseRepository[Maquina]):
    def __init__(self, db: AsyncSession):
        super().__init__(Maquina, db)

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