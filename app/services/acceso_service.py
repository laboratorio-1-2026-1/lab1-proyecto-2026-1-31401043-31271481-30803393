from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppException, NotFoundException
from app.models.bitacora_acceso import BitacoraAcceso
from app.models.membresia_cliente import EstadoMembresia
from app.repositories.acceso_repository import AccesoRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.membresia_repository import MembresiaClienteRepository
from app.schemas.acceso import AccesoEntradaCreate, AccesoFilterParams


class AccesoService:
    def __init__(self, db: AsyncSession):
        self.repo = AccesoRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.membresia_repo = MembresiaClienteRepository(db)

    async def registrar_entrada(self, schema: AccesoEntradaCreate) -> BitacoraAcceso:
        # Buscar al cliente por cédula
        cliente = await self.cliente_repo.get_by_cedula(schema.cedula)
        if not cliente:
            raise NotFoundException(
                detail="La cédula no corresponde a ningún cliente registrado",
                error_code="CLIENTE_CEDULA_NOT_FOUND"
            )

        # Verificar membresía vigente
        membresias = await self.membresia_repo.get_by_cliente_id(cliente.id)
        # get_by_cliente_id ya sincroniza los estados con la fecha actual

        tiene_membresia_activa = False
        estado_membresia = None

        for m in membresias:
            if m.estado == EstadoMembresia.activa or m.estado == EstadoMembresia.por_vencer:
                tiene_membresia_activa = True
                break
            # Guardamos el estado de la última membresía (más reciente) para el mensaje de error
            if estado_membresia is None:
                estado_membresia = m.estado

        # Registrar el acceso siempre (concedido o no)
        db_obj = await self.repo.create({
            "cliente_id": cliente.id,
            "acceso_concedido": tiene_membresia_activa,
        })
        acceso = await self.repo.get_by_id_with_relations(db_obj.id)

        # 4Si no tiene membresía vigente, lanzar 409 DESPUÉS de registrar el intento
        if not tiene_membresia_activa:
            estado_texto = estado_membresia.value if estado_membresia else "sin membresía"
            raise AppException(
                detail=f"El acceso fue denegado. La membresía del cliente se encuentra {estado_texto}.",
                error_code="ERR_ACCESO_MEMBRESIA_VENCIDA",
                status_code=409
            )

        return acceso

    async def list_accesos(self, filtros: AccesoFilterParams, skip: int, limit: int):
        return await self.repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            cliente_id=filtros.cliente_id,
            acceso_concedido=filtros.acceso_concedido,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin,
        )
