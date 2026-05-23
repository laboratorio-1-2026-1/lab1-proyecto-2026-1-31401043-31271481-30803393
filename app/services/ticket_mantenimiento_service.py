from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.maquina import TipoEstadoMaquina
from app.models.ticket_mantenimiento import TicketMantenimiento
from app.repositories.maquina_repository import MaquinaRepository
from app.repositories.ticket_mantenimiento_repository import TicketMantenimientoRepository
from app.schemas.ticket_mantenimiento import TicketCreate, TicketResolucion


class TicketMantenimientoService:
    def __init__(self, db: AsyncSession):
        self.repo = TicketMantenimientoRepository(db)
        self.maquina_repo = MaquinaRepository(db)

    async def create_ticket(self, schema: TicketCreate, usuario_id: int) -> TicketMantenimiento:
        # Verificar que la máquina exista
        maquina = await self.maquina_repo.get_by_id(schema.maquina_id)
        if not maquina:
            raise NotFoundException(detail="Máquina no encontrada", error_code="MAQUINA_NOT_FOUND")

        # Verificar que la máquina no esté ya fuera de servicio
        if maquina.estado_operativo == TipoEstadoMaquina.fuera_de_servicio:
            raise BusinessRuleException(
                detail="No se puede abrir un ticket para una máquina fuera de servicio",
                error_code="MAQUINA_FUERA_DE_SERVICIO"
            )

        # Verificar que la máquina no tenga ya un ticket abierto
        ticket_existente = await self.repo.get_ticket_abierto_por_maquina(schema.maquina_id)
        if ticket_existente:
            raise AppException(
                detail="La máquina ya tiene un ticket de mantenimiento abierto",
                error_code="TICKET_YA_ABIERTO",
                status_code=409
            )

        # Operación atómica: crear ticket + poner máquina En Mantenimiento
        db_obj = await self.repo.create_ticket_y_poner_maquina_en_mantenimiento(
            maquina=maquina,
            maquina_id=schema.maquina_id,
            usuario_id=usuario_id,
            descripcion=schema.descripcion,
        )
        return await self.repo.get_by_id_with_relations(db_obj.id)

    async def cerrar_ticket(self, ticket_id: int, schema: TicketResolucion) -> TicketMantenimiento:
        # Verificar que el ticket exista
        ticket = await self.repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundException(detail="Ticket no encontrado", error_code="TICKET_NOT_FOUND")

        # Verificar que el ticket no esté ya cerrado
        from app.models.ticket_mantenimiento import TipoEstado
        if ticket.estado_ticket == TipoEstado.cerrado:
            raise BusinessRuleException(
                detail="El ticket ya se encuentra cerrado",
                error_code="TICKET_YA_CERRADO"
            )

        # Obtener la máquina vinculada
        maquina = await self.maquina_repo.get_by_id(ticket.maquina_id)
        if not maquina:
            raise NotFoundException(detail="Máquina vinculada al ticket no encontrada", error_code="MAQUINA_NOT_FOUND")

        # Operación atómica: cerrar ticket + reactivar máquina
        db_obj = await self.repo.cerrar_ticket_y_reactivar_maquina(
            ticket=ticket,
            maquina=maquina,
            costo_reparacion=schema.costo_reparacion,
        )
        return await self.repo.get_by_id_with_relations(db_obj.id)
    
    async def list_tickets(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)
