from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundException, BusinessRuleException
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.plan_suscripcion_repository import PlanSuscripcionRepository
from app.repositories.membresia_repository import MembresiaClienteRepository
from app.repositories.pago_repository import PagoRepository
from app.schemas.pago import PagoCreate, PagoFilterParams
from app.models.membresia_cliente import EstadoMembresia
from app.models.plan_suscripcion import EstadoPlan
class PagoService:
    def __init__(self, db: AsyncSession):
        self.pago_repo = PagoRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.plan_repo = PlanSuscripcionRepository(db)
        self.membresia_repo = MembresiaClienteRepository(db)

    async def create_pago(self, schema: PagoCreate):
        # Validar Cliente
        cliente = await self.cliente_repo.get_by_id(schema.cliente_id)
        if not cliente:
            raise NotFoundException(
                detail="El cliente especificado no existe",
                error_code="CLIENTE_NOT_FOUND"
            )

        # Validar Plan
        plan = await self.plan_repo.get_by_id(schema.plan_id)
        if not plan:
            raise NotFoundException(
                detail="El plan especificado no existe",
                error_code="PLAN_NOT_FOUND"
            )
        if not plan.estado_plan == EstadoPlan.activo:
            raise NotFoundException(
                detail="El plan especificado no está activo",
                error_code="PLAN_NOT_ACTIVE"
            )
            
        hoy = date.today()
        # Guardamos los dias en una variable para evitar múltiples accesos a la propiedad del plan durante la lógica de membresía
        if schema.monto_pagado < plan.costo_actual:
            raise BusinessRuleException(
                detail="El monto pagado es menor que el costo del plan",
                error_code="MONTO_INSUFICIENTE"
            )
        if schema.monto_pagado > plan.costo_actual:
            raise BusinessRuleException(
                detail="El monto pagado es mayor que el costo del plan",
                error_code="MONTO_EXCESIVO"
            )
        duracion_dias_plan = plan.duracion_dias
        # Lógica de Membresía
        membresias = await self.membresia_repo.get_by_cliente_id(schema.cliente_id)
        
        if not membresias:
            # Crear nueva membresía
            nueva_membresia = {
                "cliente_id": schema.cliente_id,
                "plan_id": schema.plan_id,
                "fecha_inicio": hoy,
                "fecha_fin": hoy + timedelta(days=duracion_dias_plan),
                "estado": EstadoMembresia.activa
            }
            membresia = await self.membresia_repo.create(nueva_membresia)
        else:
            # Tomar la más reciente
            membresia = membresias[0]
            # Estado ya está sincronizado por get_by_cliente_id
            
            if membresia.plan_id != schema.plan_id:
                # CAMBIO DE PLAN: Cerramos la anterior y creamos una nueva
                if membresia.estado in [EstadoMembresia.activa, EstadoMembresia.por_vencer]:
                    await self.membresia_repo.update(membresia, {"fecha_fin": hoy - timedelta(days=1)})
                    await self.membresia_repo.sincronizar_estado(membresia)
                
                # Crear el nuevo registro para el nuevo plan
                nueva_membresia = {
                    "cliente_id": schema.cliente_id,
                    "plan_id": schema.plan_id,
                    "fecha_inicio": hoy,
                    "fecha_fin": hoy + timedelta(days=duracion_dias_plan),
                    "estado": EstadoMembresia.activa
                }
                membresia = await self.membresia_repo.create(nueva_membresia)
            else:
                # MISMO PLAN (Renovación): Actualizamos el registro actual
                update_data = {}

                if membresia.estado == EstadoMembresia.vencida:
                    update_data["fecha_inicio"] = hoy
                    update_data["fecha_fin"] = hoy + timedelta(days=duracion_dias_plan)
                else:
                    # Activa o por vencer, sumar días a la fecha de fin actual
                    update_data["fecha_fin"] = membresia.fecha_fin + timedelta(days=duracion_dias_plan)

                membresia = await self.membresia_repo.update(membresia, update_data)
                # Volver a sincronizar el estado luego del update
                await self.membresia_repo.sincronizar_estado(membresia)

        # Registrar Pago
        nuevo_pago = {
            "membresia_id": membresia.id,
            "monto_pagado": schema.monto_pagado,
            "metodo_pago": schema.metodo_pago
        }
        pago_creado = await self.pago_repo.create(nuevo_pago)
        
        return pago_creado

    async def list_pagos(self, skip: int, limit: int, filtros: PagoFilterParams):
        return await self.pago_repo.get_all_con_filtros(
            skip=skip,
            limit=limit,
            membresia_id=filtros.membresia_id,
            metodo_pago=filtros.metodo_pago,
            fecha_inicio=filtros.fecha_inicio,
            fecha_fin=filtros.fecha_fin
        )

    async def get_mis_pagos(self, usuario_id: int, skip: int, limit: int, fecha_inicio: date = None, fecha_fin: date = None):
        # Resolver cliente desde el token
        cliente = await self.cliente_repo.get_by_usuario_id(usuario_id)
        if not cliente:
            raise NotFoundException(
                detail="No se encontró un cliente vinculado a este usuario",
                error_code="CLIENTE_NOT_FOUND"
            )

        return await self.pago_repo.get_by_cliente_id_paginado(
            cliente_id=cliente.id,
            skip=skip,
            limit=limit,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
