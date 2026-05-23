from datetime import date, datetime , timezone, time
from typing import List, Optional, Tuple

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.sesion_programada import SesionProgramada, TipoEstado
from app.repositories.base_repository import BaseRepository


class SesionProgramadaRepository(BaseRepository[SesionProgramada]):
    def __init__(self, db: AsyncSession):
        super().__init__(SesionProgramada, db)

    async def get_by_id_with_relations(self, id: int) -> Optional[SesionProgramada]:
        result = await self.db.execute(
            select(SesionProgramada)
            .options(
                selectinload(SesionProgramada.disciplina),
                selectinload(SesionProgramada.entrenador),
                selectinload(SesionProgramada.zona)
            )
            .where(SesionProgramada.id == id)
        )
        return result.scalars().first()

    # Verificaciones de solapamiento

    async def existe_solapamiento_entrenador(
        self,
        entrenador_id: int,
        inicio: datetime,
        fin: datetime,
        excluir_id: Optional[int] = None,
    ) -> bool:
        """
        Verifica si el entrenador ya tiene una sesión activa (no cancelada)
        que se solape con el bloque horario dado.
        Solapamiento: inicio_existente < fin_nueva AND fin_existente > inicio_nueva
        """
        query = select(SesionProgramada).where(
            and_(
                SesionProgramada.entrenador_id == entrenador_id,
                SesionProgramada.estado_sesion != TipoEstado.cancelada,
                SesionProgramada.fecha_hora_inicio < fin,
                SesionProgramada.fecha_hora_fin > inicio,
            )
        )
        if excluir_id:
            query = query.where(SesionProgramada.id != excluir_id)
        result = await self.db.execute(query)
        return result.scalars().first() is not None
    
    #verficar si exiten sesiones programadas con un id de de zona en particuclar
    async def existe_sesion_programada_zona(self, zona_id: int) -> bool:
        query = select(SesionProgramada).where(SesionProgramada.zona_id == zona_id,
                                                SesionProgramada.estado_sesion == TipoEstado.programada)
        result = await self.db.execute(query)
        return result.scalars().first() is not None

    async def existe_solapamiento_zona(
        self,
        zona_id: int,
        inicio: datetime,
        fin: datetime,
        excluir_id: Optional[int] = None,
    ) -> bool:
        """
        Verifica si la zona ya tiene una sesión activa (no cancelada)
        que se solape con el bloque horario dado.
        """
        query = select(SesionProgramada).where(
            and_(
                SesionProgramada.zona_id == zona_id,
                SesionProgramada.estado_sesion != TipoEstado.cancelada,
                SesionProgramada.fecha_hora_inicio < fin,
                SesionProgramada.fecha_hora_fin > inicio,
            )
        )
        if excluir_id:
            query = query.where(SesionProgramada.id != excluir_id)
        result = await self.db.execute(query)
        return result.scalars().first() is not None

    # ─────────────────────────────────────────────
    # Listados con filtros avanzados
    # ─────────────────────────────────────────────

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        fecha: Optional[date] = None,
        disciplina_id: Optional[int] = None,
        entrenador_id: Optional[int] = None,
        estado_sesion: Optional[TipoEstado] = None,
    ) -> Tuple[int, List[SesionProgramada]]:
        #Listado general con filtros por fecha exacta, disciplina, entrenador y estado.
        query = select(SesionProgramada).options(
            selectinload(SesionProgramada.disciplina),
            selectinload(SesionProgramada.entrenador),
            selectinload(SesionProgramada.zona)
        )
        conditions = []

        if fecha:
            # Filtra todos los registros del día completo
            inicio_dia = datetime.combine(fecha, time.min, tzinfo=timezone.utc)
            fin_dia = datetime.combine(fecha, time.max, tzinfo=timezone.utc)
            conditions.append(SesionProgramada.fecha_hora_inicio >= inicio_dia)
            conditions.append(SesionProgramada.fecha_hora_inicio <= fin_dia)
        if disciplina_id is not None:
            conditions.append(SesionProgramada.disciplina_id == disciplina_id)
        if entrenador_id is not None:
            conditions.append(SesionProgramada.entrenador_id == entrenador_id)
        if estado_sesion is not None:
            conditions.append(SesionProgramada.estado_sesion == estado_sesion)

        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(SesionProgramada.fecha_hora_inicio).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())

    async def get_mis_sesiones(
        self,
        entrenador_id: int,
        skip: int = 0,
        limit: int = 100,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        estado_sesion: Optional[TipoEstado] = None,
    ) -> Tuple[int, List[SesionProgramada]]:
        """
        Sesiones del entrenador autenticado (/me).
        Filtra por rango de fechas y estado.
        """
        conditions = [SesionProgramada.entrenador_id == entrenador_id]

        if fecha_inicio:
            inicio = datetime.combine(fecha_inicio, time.min, tzinfo=timezone.utc)
            conditions.append(SesionProgramada.fecha_hora_inicio >= inicio)
        if fecha_fin:
            fin = datetime.combine(fecha_fin, time.max, tzinfo=timezone.utc)
            conditions.append(SesionProgramada.fecha_hora_inicio <= fin)
        if estado_sesion:
            conditions.append(SesionProgramada.estado_sesion == estado_sesion)

        query = select(SesionProgramada).options(
            selectinload(SesionProgramada.disciplina),
            selectinload(SesionProgramada.entrenador),
            selectinload(SesionProgramada.zona)
        ).where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(SesionProgramada.fecha_hora_inicio).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())
