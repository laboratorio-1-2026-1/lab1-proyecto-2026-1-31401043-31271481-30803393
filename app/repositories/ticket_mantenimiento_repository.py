from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.maquina import Maquina, TipoEstadoMaquina
from app.models.ticket_mantenimiento import TicketMantenimiento, TipoEstado
from app.repositories.base_repository import BaseRepository


class TicketMantenimientoRepository(BaseRepository[TicketMantenimiento]):
    def __init__(self, db: AsyncSession):
        super().__init__(TicketMantenimiento, db)

    async def get_ticket_abierto_por_maquina(self, maquina_id: int) -> TicketMantenimiento | None:
        #Devuelve el ticket Abierto activo de una máquina, si existe
        result = await self.db.execute(
            select(TicketMantenimiento).where(
                TicketMantenimiento.maquina_id == maquina_id,
                TicketMantenimiento.estado_ticket == TipoEstado.abierto
            )
        )
        return result.scalars().first()

    async def create_ticket_y_poner_maquina_en_mantenimiento(
        self,
        maquina: Maquina,
        maquina_id: int,
        usuario_id: int,
        descripcion: str,
    ) -> TicketMantenimiento:
        """
        Operación atómica: crea el ticket y cambia el estado de la máquina
        a 'En Mantenimiento' dentro de la misma transacción.
        """
        # Crear el ticket
        ticket = TicketMantenimiento(
            maquina_id=maquina_id,
            usuario_id=usuario_id,
            descripcion=descripcion,
        )
        self.db.add(ticket)

        # Actualizar estado de la máquina en la misma transacción
        maquina.estado_operativo = TipoEstadoMaquina.en_mantenimiento
        self.db.add(maquina)

        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def cerrar_ticket_y_reactivar_maquina(
        self,
        ticket: TicketMantenimiento,
        maquina: Maquina,
        costo_reparacion: float,
    ) -> TicketMantenimiento:
        """
        Operación atómica: cierra el ticket (fecha_resolucion, costo, estado=Cerrado)
        y reactiva la máquina a 'Activa' dentro de la misma transacción.
        """
        # Cerrar el ticket
        ticket.fecha_resolucion = datetime.now(timezone.utc)
        ticket.costo_reparacion = costo_reparacion
        ticket.estado_ticket = TipoEstado.cerrado
        self.db.add(ticket)

        # Reactivar la máquina
        maquina.estado_operativo = TipoEstadoMaquina.activa
        self.db.add(maquina)

        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket
