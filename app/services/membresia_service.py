from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundException
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.membresia_repository import MembresiaClienteRepository
from app.schemas.membresia import MembresiaFilterParams


class MembresiaService:
    def __init__(self, db: AsyncSession):
        self.repo = MembresiaClienteRepository(db)
        self.cliente_repo = ClienteRepository(db)

    async def list_membresias(self, filtros: MembresiaFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=filtros.cliente_id,
            estado=filtros.estado,
        )

    async def get_mis_membresias(self, usuario_id: int):
        # Resolver cliente desde el token
        cliente = await self.cliente_repo.get_by_usuario_id(usuario_id)
        if not cliente:
            raise NotFoundException(
                detail="No se encontró un cliente vinculado a este usuario",
                error_code="CLIENTE_NOT_FOUND"
            )

        membresias = await self.repo.get_by_cliente_id(cliente.id)
        if not membresias:
            raise NotFoundException(
                detail="No se encontraron membresías registradas para este cliente",
                error_code="MEMBRESIA_NOT_FOUND"
            )

        return membresias
