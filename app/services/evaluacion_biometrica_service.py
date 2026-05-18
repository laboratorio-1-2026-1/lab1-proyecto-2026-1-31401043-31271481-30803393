from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundException
from app.models.evaluacion_biometrica import EvaluacionBiometrica
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.entrenador_repository import EntrenadorRepository
from app.repositories.evaluacion_biometrica_repository import EvaluacionBiometricaRepository
from app.schemas.evaluacion_biometrica import (
    EvaluacionCreate,
    EvaluacionFilterParams,
    EvaluacionUpdate,
    MisEvaluacionesFilterParams,
)


class EvaluacionBiometricaService:
    def __init__(self, db: AsyncSession):
        self.repo = EvaluacionBiometricaRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.entrenador_repo = EntrenadorRepository(db)

    async def create_evaluacion(self, schema: EvaluacionCreate, usuario_id: int) -> EvaluacionBiometrica:
        # Resolver el entrenador vinculado al usuario del token
        entrenador = await self.entrenador_repo.get_by_usuario_id(usuario_id)
        if not entrenador:
            raise NotFoundException(
                detail="No se encontró un entrenador vinculado a este usuario",
                error_code="ENTRENADOR_NOT_FOUND"
            )

        # 2. Verificar que el cliente exista
        cliente = await self.cliente_repo.get_by_id(schema.cliente_id)
        if not cliente:
            raise NotFoundException(
                detail="Cliente no encontrado",
                error_code="CLIENTE_NOT_FOUND"
            )

        # 3. Construir los datos combinando el payload con el entrenador_id resuelto
        evaluacion_data = schema.model_dump()
        evaluacion_data["entrenador_id"] = entrenador.id

        return await self.repo.create(evaluacion_data)

    async def update_evaluacion(self, id: int, schema: EvaluacionUpdate) -> EvaluacionBiometrica:
        evaluacion = await self.repo.get_by_id(id)
        if not evaluacion:
            raise NotFoundException(
                detail="Evaluación biométrica no encontrada",
                error_code="EVALUACION_NOT_FOUND"
            )

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return evaluacion

        return await self.repo.update(db_obj=evaluacion, obj_in_data=update_data)

    async def list_evaluaciones(self, filtros: EvaluacionFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=filtros.cliente_id,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin,
        )

    async def list_mis_evaluaciones(
        self, usuario_id: int, filtros: MisEvaluacionesFilterParams, skip: int, limit: int
    ):
        # Resolver cliente desde el usuario del token
        cliente = await self.cliente_repo.get_by_usuario_id(usuario_id)
        if not cliente:
            raise NotFoundException(
                detail="No se encontró un cliente vinculado a este usuario",
                error_code="CLIENTE_NOT_FOUND"
            )

        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=cliente.id,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin,
        )
