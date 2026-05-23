from datetime import date, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.membresia_cliente import EstadoMembresia, MembresiaCliente
from app.repositories.base_repository import BaseRepository

# Umbral de días para considerar una membresía como "Por Vencer"
DIAS_POR_VENCER = 7


class MembresiaClienteRepository(BaseRepository[MembresiaCliente]):
    def __init__(self, db: AsyncSession):
        super().__init__(MembresiaCliente, db)

    async def get_by_id_with_relations(self, id: int) -> Optional[MembresiaCliente]:
        result = await self.db.execute(
            select(MembresiaCliente)
            .options(
                selectinload(MembresiaCliente.cliente),
                selectinload(MembresiaCliente.plan)
            )
            .where(MembresiaCliente.id == id)
        )
        return result.scalars().first()

    def calcular_estado(self, membresia: MembresiaCliente) -> EstadoMembresia:
        """
        Calcula el estado real de la membresía basado en las fechas.
        - Vencida: fecha_fin < hoy
        - Por Vencer: fecha_fin está dentro de los próximos DIAS_POR_VENCER días
        - Activa: aún le quedan más de DIAS_POR_VENCER días
        """
        hoy = date.today()
        if membresia.fecha_fin < hoy:
            return EstadoMembresia.vencida
        elif membresia.fecha_fin <= hoy + timedelta(days=DIAS_POR_VENCER):
            return EstadoMembresia.por_vencer
        return EstadoMembresia.activa

    async def sincronizar_estado(self, membresia: MembresiaCliente, auto_commit: bool = True) -> bool:
        """
        Recalcula el estado y lo persiste en la DB si cambió.
        De este modo el campo `estado` en la tabla siempre refleja la realidad.
        """
        estado_calculado = self.calcular_estado(membresia)
        if membresia.estado != estado_calculado:
            membresia.estado = estado_calculado
            self.db.add(membresia)
            # Solo hacemos commit si se pide explícitamente (para no romper los ciclos for)
            if auto_commit:
                await self.db.commit()
                await self.db.refresh(membresia)
            return True
        return False

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        cliente_id: Optional[int] = None,
        estado: Optional[EstadoMembresia] = None,
    ) -> Tuple[int, List[MembresiaCliente]]:
        """
        Lista membresías. Primero sincroniza los estados con la fecha actual,
        luego aplica los filtros incluyendo el de estado.
        """
        # Traer TODAS las membresías para recalcular estado (sin paginar aún)
        query_all = select(MembresiaCliente)
        if cliente_id is not None:
            query_all = query_all.where(MembresiaCliente.cliente_id == cliente_id)

        result_all = await self.db.execute(query_all)
        todas = list(result_all.scalars().all())

        # Sincronizar estado de cada una SIN hacer commit individual
        hubo_cambios = False
        for m in todas:
            cambio = await self.sincronizar_estado(m, auto_commit=False)
            if cambio:
                hubo_cambios = True
        # Hacemos un solo commit global si al menos una membresía cambió
        if hubo_cambios:
            await self.db.commit() 

        # Ahora construir la query final con filtros (incluido el estado actualizado)
        conditions = []
        if cliente_id is not None:
            conditions.append(MembresiaCliente.cliente_id == cliente_id)
        if estado is not None:
            conditions.append(MembresiaCliente.estado == estado)

        query = select(MembresiaCliente).options(
            selectinload(MembresiaCliente.cliente),
            selectinload(MembresiaCliente.plan)
        )
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(MembresiaCliente.fecha_fin.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())

    async def get_by_cliente_id(self, cliente_id: int) -> List[MembresiaCliente]:
        #Retorna todas las membresías de un cliente, sincronizando sus estados.
        result = await self.db.execute(
            select(MembresiaCliente)
            .options(
                selectinload(MembresiaCliente.cliente),
                selectinload(MembresiaCliente.plan)
            )
            .where(MembresiaCliente.cliente_id == cliente_id)
            .order_by(MembresiaCliente.fecha_fin.desc())
        )
        membresias = list(result.scalars().all())

        # Sincronizar estado SIN commit individual
        hubo_cambios = False
        for m in membresias:
            cambio = await self.sincronizar_estado(m, auto_commit=False)
            if cambio:
                hubo_cambios = True
        if hubo_cambios:
            await self.db.commit()

        return membresias
