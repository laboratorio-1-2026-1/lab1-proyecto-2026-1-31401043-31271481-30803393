from typing import List, Optional, Tuple

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.reserva import Reserva, TipoEstado as EstadoReserva
from app.models.sesion_programada import SesionProgramada
from app.repositories.base_repository import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):
    def __init__(self, db: AsyncSession):
        super().__init__(Reserva, db)

    async def get_by_id_with_relations(self, id: int) -> Optional[Reserva]:
        result = await self.db.execute(
            select(Reserva)
            .options(
                selectinload(Reserva.cliente),
                selectinload(Reserva.sesion_programada)
            )
            .where(Reserva.id == id)
        )
        return result.scalars().first()

    async def get_reserva_activa_cliente_sesion(
        self, cliente_id: int, sesion_id: int
    ) -> Reserva | None:
        #Verifica si el cliente ya tiene una reserva confirmada para esta sesión exacta
        result = await self.db.execute(
            select(Reserva).where(
                Reserva.cliente_id == cliente_id,
                Reserva.sesion_id == sesion_id,
                Reserva.estado_reserva == EstadoReserva.confirmada,
            )
        )
        return result.scalars().first()

    async def contar_reservas_confirmadas(self, sesion_id: int) -> int:
        #Cuenta cuántas reservas confirmadas tiene una sesión (para control de cupo).
        result = await self.db.execute(
            select(func.count(Reserva.id)).where(
                Reserva.sesion_id == sesion_id,
                Reserva.estado_reserva == EstadoReserva.confirmada,
            )
        )
        return result.scalar_one()

    async def existe_solapamiento_cliente(
        self, cliente_id: int, inicio: object, fin: object
    ) -> bool:
        """
        Verifica si el cliente ya tiene una reserva CONFIRMADA en otra sesión
        que se solape con el bloque horario dado.
        Usa JOIN con SesionProgramada para comparar fechas.
        """
        result = await self.db.execute(
            select(Reserva).join(
                SesionProgramada, Reserva.sesion_id == SesionProgramada.id
            ).where(
                and_(
                    Reserva.cliente_id == cliente_id,
                    Reserva.estado_reserva == EstadoReserva.confirmada,
                    SesionProgramada.fecha_hora_inicio < fin,
                    SesionProgramada.fecha_hora_fin > inicio,
                )
            )
        )
        return result.scalars().first() is not None

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        sesion_id: Optional[int] = None,
        estado_reserva: Optional[EstadoReserva] = None,
    ) -> Tuple[int, List[Reserva]]:
        #Listado general con filtros para la vista de admin/entrenador
        conditions = []
        if cliente_id is not None:
            conditions.append(Reserva.cliente_id == cliente_id)
        if sesion_id is not None:
            conditions.append(Reserva.sesion_id == sesion_id)
        if estado_reserva is not None:
            conditions.append(Reserva.estado_reserva == estado_reserva)

        query = select(Reserva).options(
            selectinload(Reserva.cliente),
            selectinload(Reserva.sesion_programada)
        )
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(Reserva.fecha_registro.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())

    async def get_mis_reservas(
        self,
        cliente_id: int,
        skip: int = 0,
        limit: int = 100,
        estado_reserva: Optional[EstadoReserva] = None,
    ) -> Tuple[int, List[Reserva]]:
        #Reservas del cliente autenticado (/me)
        conditions = [Reserva.cliente_id == cliente_id]
        if estado_reserva is not None:
            conditions.append(Reserva.estado_reserva == estado_reserva)

        query = select(Reserva).options(
            selectinload(Reserva.cliente),
            selectinload(Reserva.sesion_programada)
        ).where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(Reserva.fecha_registro.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())
