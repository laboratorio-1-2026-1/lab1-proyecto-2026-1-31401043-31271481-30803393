from typing import List, Tuple, Optional
from datetime import date
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pago_membresia import PagoMembresia, MetodoPago
from app.models.membresia_cliente import MembresiaCliente
from app.repositories.base_repository import BaseRepository

class PagoRepository(BaseRepository[PagoMembresia]):
    def __init__(self, db: AsyncSession):
        super().__init__(PagoMembresia, db)

    async def get_all_con_filtros(
        self,
        skip: int = 0,
        limit: int = 100,
        membresia_id: Optional[int] = None,
        metodo_pago: Optional[MetodoPago] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Tuple[int, List[PagoMembresia]]:
        conditions = []
        if membresia_id is not None:
            conditions.append(PagoMembresia.membresia_id == membresia_id)
        if metodo_pago is not None:
            conditions.append(PagoMembresia.metodo_pago == metodo_pago)
        if fecha_inicio is not None:
            # Cast datetime to date for comparison
            conditions.append(func.date(PagoMembresia.fecha_pago) >= fecha_inicio)
        if fecha_fin is not None:
            conditions.append(func.date(PagoMembresia.fecha_pago) <= fecha_fin)

        query = select(PagoMembresia)
        if conditions:
            query = query.where(and_(*conditions))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()

        query = query.order_by(PagoMembresia.fecha_pago.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        
        return total, list(result.scalars().all())

    async def get_by_cliente_id_paginado(
        self,
        cliente_id: int,
        skip: int = 0,
        limit: int = 100,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Tuple[int, List[PagoMembresia]]:
        
        # Unimos con MembresiaCliente para filtrar por cliente_id
        query = select(PagoMembresia).join(MembresiaCliente)
        
        conditions = [MembresiaCliente.cliente_id == cliente_id]
        if fecha_inicio is not None:
            conditions.append(func.date(PagoMembresia.fecha_pago) >= fecha_inicio)
        if fecha_fin is not None:
            conditions.append(func.date(PagoMembresia.fecha_pago) <= fecha_fin)
            
        query = query.where(and_(*conditions))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar_one()
        
        query = query.order_by(PagoMembresia.fecha_pago.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        
        return total, list(result.scalars().all())
