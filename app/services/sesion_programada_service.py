from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, BusinessRuleException, NotFoundException
from app.models.disciplina import TipoEstado as EstadoDisciplina
from app.models.entrenador import TipoEstado as EstadoEntrenador
from app.models.sesion_programada import SesionProgramada, TipoEstado as EstadoSesion
from app.models.zona_instalacion import TipoEstado as EstadoZona
from app.repositories.disciplina_repository import DisciplinaRepository
from app.repositories.entrenador_repository import EntrenadorRepository
from app.repositories.sesion_programada_repository import SesionProgramadaRepository
from app.repositories.zona_instalacion import ZonaInstalacionRepository
from app.schemas.sesion_programada import (
    MisSesionesFilterParams,
    SesionCreate,
    SesionFilterParams,
    SesionUpdateEstado,
)


class SesionProgramadaService:
    def __init__(self, db: AsyncSession):
        self.repo = SesionProgramadaRepository(db)
        self.entrenador_repo = EntrenadorRepository(db)
        self.zona_repo = ZonaInstalacionRepository(db)
        self.disciplina_repo = DisciplinaRepository(db)

    async def create_sesion(self, schema: SesionCreate) -> SesionProgramada:
        # Verificar que la disciplina exista y esté activa
        disciplina = await self.disciplina_repo.get_by_id(schema.disciplina_id)
        if not disciplina:
            raise NotFoundException(detail="Disciplina no encontrada", error_code="DISCIPLINA_NOT_FOUND")
        if disciplina.estado_disciplina == EstadoDisciplina.inactiva:
            raise BusinessRuleException(
                detail="La disciplina seleccionada no está activa",
                error_code="DISCIPLINA_INACTIVA"
            )

        # Verificar que el entrenador exista y esté disponible
        entrenador = await self.entrenador_repo.get_by_id(schema.entrenador_id)
        if not entrenador:
            raise NotFoundException(detail="Entrenador no encontrado", error_code="ENTRENADOR_NOT_FOUND")
        if entrenador.estado_laboral != EstadoEntrenador.activo:
            raise BusinessRuleException(
                detail=f"El entrenador no está disponible (estado: {entrenador.estado_laboral.value})",
                error_code="ENTRENADOR_NO_DISPONIBLE"
            )

        # Verificar que la zona exista y esté activa
        zona = await self.zona_repo.get_by_id(schema.zona_id)
        if not zona:
            raise NotFoundException(detail="Zona de instalación no encontrada", error_code="ZONA_NOT_FOUND")
        if zona.estado_zona != EstadoZona.activa:
            raise BusinessRuleException(
                detail=f"La zona no está disponible (estado: {zona.estado_zona.value})",
                error_code="ZONA_NO_DISPONIBLE"
            )

        # Verificar que el cupo de la sesión no exceda la capacidad máxima de la zona
        if schema.cupo_maximo > zona.capacidad_maxima:
            raise BusinessRuleException(
                detail=f"El cupo máximo ({schema.cupo_maximo}) excede la capacidad de la zona '{zona.nombre_zona}' ({zona.capacidad_maxima} personas)",
                error_code="CUPO_EXCEDE_CAPACIDAD_ZONA"
            )

        # Verificar solapamiento de entrenador en ese bloque horario
        solapa_entrenador = await self.repo.existe_solapamiento_entrenador(
            entrenador_id=schema.entrenador_id,
            inicio=schema.fecha_hora_inicio,
            fin=schema.fecha_hora_fin,
        )
        if solapa_entrenador:
            raise AppException(
                detail="El entrenador ya tiene una sesión asignada en ese bloque horario",
                error_code="ENTRENADOR_SOLAPAMIENTO",
                status_code=409
            )

        # Verificar solapamiento de zona en ese bloque horario
        solapa_zona = await self.repo.existe_solapamiento_zona(
            zona_id=schema.zona_id,
            inicio=schema.fecha_hora_inicio,
            fin=schema.fecha_hora_fin,
        )
        if solapa_zona:
            raise AppException(
                detail="La zona ya está ocupada en ese bloque horario",
                error_code="ZONA_SOLAPAMIENTO",
                status_code=409
            )

        # Crear la sesión usando el base (una sola tabla, no requiere función especial)
        return await self.repo.create(schema.model_dump())

    async def update_sesion_estado(self, id: int, schema: SesionUpdateEstado) -> SesionProgramada:
        sesion = await self.repo.get_by_id(id)
        if not sesion:
            raise NotFoundException(detail="Sesión no encontrada", error_code="SESION_NOT_FOUND")

        # Validar transiciones de estado permitidas
        transiciones_validas = {
            EstadoSesion.programada: [EstadoSesion.en_curso, EstadoSesion.cancelada],
            EstadoSesion.en_curso: [EstadoSesion.finalizada, EstadoSesion.cancelada],
            EstadoSesion.finalizada: [],
            EstadoSesion.cancelada: [],
        }
        estado_actual = sesion.estado_sesion
        nuevo_estado = schema.estado_sesion
        if nuevo_estado not in transiciones_validas.get(estado_actual, []):
            raise BusinessRuleException(
                detail=f"No se puede cambiar el estado de '{estado_actual.value}' a '{nuevo_estado.value}'",
                error_code="TRANSICION_ESTADO_INVALIDA"
            )

        return await self.repo.update(db_obj=sesion, obj_in_data=schema.model_dump(exclude_unset=True))

    async def list_sesiones(self, filtros: SesionFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            fecha=filtros.fecha,
            disciplina_id=filtros.disciplina_id,
            entrenador_id=filtros.entrenador_id,
            estado_sesion=filtros.estado_sesion,
        )

    async def list_mis_sesiones(
        self, entrenador_id: int, filtros: MisSesionesFilterParams, skip: int, limit: int
    ):
        return await self.repo.get_mis_sesiones(
            entrenador_id=entrenador_id,
            skip=skip,
            limit=limit,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin,
            estado_sesion=filtros.estado_sesion,
        )
