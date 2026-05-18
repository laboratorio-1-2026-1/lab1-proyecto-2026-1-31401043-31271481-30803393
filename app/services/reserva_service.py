from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.reserva import Reserva, TipoEstado as EstadoReserva
from app.models.sesion_programada import TipoEstado as EstadoSesion
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.reserva_repository import ReservaRepository
from app.repositories.sesion_programada_repository import SesionProgramadaRepository
from app.schemas.reserva import MisReservasFilterParams, ReservaCreate, ReservaFilterParams, ReservaUpdateEstado


class ReservaService:
    def __init__(self, db: AsyncSession):
        self.repo = ReservaRepository(db)
        self.sesion_repo = SesionProgramadaRepository(db)
        self.cliente_repo = ClienteRepository(db)

    async def create_reserva(self, schema: ReservaCreate, usuario_id: int) -> Reserva:
        # Resolver el cliente vinculado al usuario del token
        cliente = await self.cliente_repo.get_by_usuario_id(usuario_id)
        if not cliente:
            raise NotFoundException(
                detail="No se encontró un cliente vinculado a este usuario",
                error_code="CLIENTE_NOT_FOUND"
            )

        # Verificar que la sesión exista
        sesion = await self.sesion_repo.get_by_id(schema.sesion_id)
        if not sesion:
            raise NotFoundException(detail="Sesión no encontrada", error_code="SESION_NOT_FOUND")

        #  Verificar que la sesión esté en estado 'Programada' (no cancelada, finalizada, en curso)
        if sesion.estado_sesion != EstadoSesion.programada:
            raise BusinessRuleException(
                detail=f"No se puede reservar una sesión con estado '{sesion.estado_sesion.value}'",
                error_code="SESION_NO_DISPONIBLE"
            )

        #  Verificar que el cliente no tenga ya una reserva confirmada en esta misma sesión
        reserva_existente = await self.repo.get_reserva_activa_cliente_sesion(
            cliente_id=cliente.id, sesion_id=schema.sesion_id
        )
        if reserva_existente:
            raise AppException(
                detail="Ya tienes una reserva confirmada para esta sesión",
                error_code="RESERVA_DUPLICADA",
                status_code=409
            )

        # 5. Control de cupo — verificar que no se exceda el cupo_maximo (sobreventa)
        reservas_activas = await self.repo.contar_reservas_confirmadas(schema.sesion_id)
        if reservas_activas >= sesion.cupo_maximo:
            raise AppException(
                detail="La sesión no tiene cupos disponibles",
                error_code="SIN_CUPO_DISPONIBLE",
                status_code=409
            )

        # Verificar solapamiento horario — el cliente no puede estar en dos sesiones al mismo tiempo
        solapa = await self.repo.existe_solapamiento_cliente(
            cliente_id=cliente.id,
            inicio=sesion.fecha_hora_inicio,
            fin=sesion.fecha_hora_fin,
        )
        if solapa:
            raise AppException(
                detail="Ya tienes una reserva confirmada en otro sesión que se solapa con este horario",
                error_code="SOLAPAMIENTO_HORARIO",
                status_code=409
            )

        # Crear la reserva (una sola tabla → se usa el base)
        return await self.repo.create({
            "sesion_id": schema.sesion_id,
            "cliente_id": cliente.id,
        })

    async def update_reserva_estado(
        self,
        reserva_id: int,
        schema: ReservaUpdateEstado,
        rol_usuario: str,
    ) -> Reserva:
        # Verificar que la reserva exista
        reserva = await self.repo.get_by_id(reserva_id)
        if not reserva:
            raise NotFoundException(detail="Reserva no encontrada", error_code="RESERVA_NOT_FOUND")

        # Verificar que la reserva no esté ya cancelada (estado terminal)
        if reserva.estado_reserva == EstadoReserva.cancelada:
            raise BusinessRuleException(
                detail="La reserva ya está cancelada",
                error_code="RESERVA_YA_CANCELADA"
            )

        # Verificar que la reserva no esté ya en estado Asistio (estado terminal)
        if reserva.estado_reserva == EstadoReserva.asistio:
            raise BusinessRuleException(
                detail="La reserva ya fue marcada como asistida y no puede modificarse",
                error_code="RESERVA_YA_ASISTIDA"
            )

        # 4. Control de permisos por rol:
        #    - El cliente solo puede CANCELAR su reserva, nunca marcar 'Asistio'
        #    - Solo Administración / Entrenador pueden marcar 'Asistio'
        nuevo_estado = schema.estado_reserva
        rol_upper = rol_usuario.upper() if rol_usuario else ""
        es_cliente = "CLIENTE" in rol_upper

        if es_cliente and nuevo_estado == EstadoReserva.asistio:
            raise BusinessRuleException(
                detail="Los clientes no pueden marcar su propia asistencia",
                error_code="ACCION_NO_PERMITIDA_PARA_CLIENTE"
            )

        return await self.repo.update(
            db_obj=reserva,
            obj_in_data=schema.model_dump(exclude_unset=True)
        )

    async def list_reservas(self, filtros: ReservaFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=filtros.cliente_id,
            sesion_id=filtros.sesion_id,
            estado_reserva=filtros.estado_reserva,
        )

    async def list_mis_reservas(
        self, usuario_id: int, filtros: MisReservasFilterParams, skip: int, limit: int
    ):
        cliente = await self.cliente_repo.get_by_usuario_id(usuario_id)
        if not cliente:
            raise NotFoundException(
                detail="No se encontró un cliente vinculado a este usuario",
                error_code="CLIENTE_NOT_FOUND"
            )
        return await self.repo.get_mis_reservas(
            cliente_id=cliente.id,
            skip=skip,
            limit=limit,
            estado_reserva=filtros.estado_reserva,
        )
