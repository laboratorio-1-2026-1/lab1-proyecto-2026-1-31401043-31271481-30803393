from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.disciplina import Disciplina
from app.repositories.disciplina_repository import DisciplinaRepository
from app.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate, DisciplinaUpdateEstado


class DisciplinaService:
    def __init__(self, db: AsyncSession):
        self.repo = DisciplinaRepository(db)

    async def create_disciplina(self, schema: DisciplinaCreate) -> Disciplina:
        # Verificar unicidad del nombre
        existente = await self.repo.get_by_nombre_disciplina(schema.nombre_disciplina)
        if existente:
            raise AppException(
                detail="El nombre de la disciplina ya está registrado",
                error_code="DISCIPLINA_NAME_EXISTS",
                status_code=409
            )

        return await self.repo.create(schema.model_dump())

    async def update_disciplina(self, id: int, schema: DisciplinaUpdate) -> Disciplina:
        # Verificar existencia
        disciplina = await self.repo.get_by_id(id)
        if not disciplina:
            raise NotFoundException(detail="Disciplina no encontrada", error_code="DISCIPLINA_NOT_FOUND")

        # Solo actualizamos los campos explícitamente enviados en el body
        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return disciplina

        return await self.repo.update(db_obj=disciplina, obj_in_data=update_data)

    async def update_disciplina_estado(self, id: int, schema: DisciplinaUpdateEstado) -> Disciplina:
        # Verificar existencia
        disciplina = await self.repo.get_by_id(id)
        if not disciplina:
            raise NotFoundException(detail="Disciplina no encontrada", error_code="DISCIPLINA_NOT_FOUND")

        # Idempotencia: si el estado ya es el mismo, no tocar la DB
        if disciplina.estado_disciplina == schema.estado_disciplina:
            return disciplina

        update_data = schema.model_dump(exclude_unset=True)
        return await self.repo.update(db_obj=disciplina, obj_in_data=update_data)

    async def list_disciplinas(self, skip: int = 0, limit: int = 100, filters: dict = None):
        return await self.repo.get_all(skip=skip, limit=limit, filters=filters)
