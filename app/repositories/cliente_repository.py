from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Dict, Any, Tuple, List, Optional 

from app.models.membresia_cliente import MembresiaCliente
from app.models.cliente import Cliente
from app.repositories.base_repository import BaseRepository

class ClienteRepository(BaseRepository[Cliente]):
    def __init__(self, db: AsyncSession):
        super().__init__(Cliente, db)
    
    async def get_by_usuario_id(self, usuario_id: int) -> Cliente | None:
        result = await self.db.execute(
            select(Cliente).where(Cliente.usuario_id == usuario_id)
        )
        return result.scalars().first()
    async def get_by_cedula(self, cedula: str) -> Cliente | None:
        result = await self.db.execute(
            select(Cliente).where(Cliente.cedula == cedula)
        )
        return result.scalars().first()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[int, List[Cliente]]:
        # Separar filtros directos y el especial de membresía
        estado_membresia = None
        other_filters = {}
        if filters:
            for key, value in filters.items():
                if key == 'estado' or key == 'estado_membresia':
                    estado_membresia = value
                else:
                    other_filters[key] = value

        # Consulta base con DISTINCT por si un cliente tiene múltiples membresías
        query = select(Cliente).distinct()

        # Aplicar filtros directos (sobre columnas de Cliente)
        for key, value in other_filters.items():
            if value is not None and hasattr(Cliente, key):
                if isinstance(value, str):
                    query = query.where(getattr(Cliente, key).ilike(f"%{value}%"))
                else:
                    query = query.where(getattr(Cliente, key) == value)

        # Aplicar filtro por membresía SOLO si se proporciona
        if estado_membresia:
            # INNER JOIN explícito para asegurar que solo clientes CON membresía
            query = query.join(MembresiaCliente, Cliente.id == MembresiaCliente.cliente_id)
            query = query.where(MembresiaCliente.estado == estado_membresia)

        # Query de conteo (con los mismos joins y filtros)
        count_query = select(func.count(Cliente.id.distinct()))
        # Aplicar los mismos filtros directos al count
        for key, value in other_filters.items():
            if value is not None and hasattr(Cliente, key):
                if isinstance(value, str):
                    count_query = count_query.where(getattr(Cliente, key).ilike(f"%{value}%"))
                else:
                    count_query = count_query.where(getattr(Cliente, key) == value)
        if estado_membresia:
            count_query = count_query.join(MembresiaCliente, Cliente.id == MembresiaCliente.cliente_id)
            count_query = count_query.where(MembresiaCliente.estado == estado_membresia)

        total = await self.db.scalar(count_query)

        # Paginación
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return total, list(result.scalars().all())
    