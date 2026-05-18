# seed.py
from sqlalchemy.future import select
from sqlalchemy import func
from app.database.session import SessionLocal
from app.core.security import get_password_hash

# Importación de todos los modelos necesarios
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.categoria_maquina import CategoriaMaquina
from app.models.maquina import Maquina
from app.models.plan_suscripcion import PlanSuscripcion
from app.models.producto_tienda import ProductoTienda
from app.models.categoria_producto import CategoriaProducto
from app.models.zona_instalacion import ZonaInstalacion

async def init_seed_data():
    async with SessionLocal() as db:
        try:
            # Verificar si la base de datos ya tiene roles (indicador de DB inicializada)
            result = await db.execute(select(func.count(Rol.id)))
            count = result.scalar()

            if count > 0:
                print("La base de datos ya contiene datos. Omitiendo seed.")
                return

            print("Base de datos vacía. Iniciando carga de datos semilla...")

            # Crear Roles Fundamentales
            roles_nombres = ["Administrador", "Cliente", "Finanzas", "Entrenador"]
            roles_objs = [Rol(nombre=nom) for nom in roles_nombres]
            db.add_all(roles_objs)
            await db.flush() # flush para obtener los IDs generados sin terminar la transacción

            # Buscamos el ID del rol Administrador para el usuario
            admin_role = next(r for r in roles_objs if r.nombre == "Administrador")

            # Crear Usuario Administrador
            pwd_hash = get_password_hash("admin123")
            admin_user = Usuario(
                email="admin@smartgym.com", 
                password_hash=pwd_hash, 
                rol_id=admin_role.id
            )
            db.add(admin_user)

            # Crear 3 Categorías de Máquinas
            cat_nombres = ["Cardio", "Fuerza", "Flexibilidad"]
            categorias = [CategoriaMaquina(nombre_categoria=nom) for nom in cat_nombres]
            db.add_all(categorias)
            await db.flush()

            # Crear 3 Zonas de Instalación
            zona_nombres = ["Zona 1", "Zona 2", "Zona 3"]
            zonas = [ZonaInstalacion(nombre_zona=nom, capacidad_maxima=50) for nom in zona_nombres]
            db.add_all(zonas)
            await db.flush()
            # Crear 5 Máquinas de ejemplo
            maquinas = [
                Maquina(categoria_id=categorias[0].id, zona_id=zonas[0].id,identificador_interno="MAQ001", nombre="Caminadora Pro",descripcion_tecnica="Caminadora de alta eficiencia"),
                Maquina(categoria_id=categorias[0].id, zona_id=zonas[1].id, identificador_interno="MAQ002", nombre="Bicicleta Estática",descripcion_tecnica="Bicicleta de resistencia"),
                Maquina(categoria_id=categorias[1].id, zona_id=zonas[1].id, identificador_interno="MAQ003", nombre="Prensa de Piernas",descripcion_tecnica="Prensa para ejercicios de piernas"),
                Maquina(categoria_id=categorias[1].id, zona_id=zonas[2].id, identificador_interno="MAQ004", nombre="Rack de Mancuernas",descripcion_tecnica="Rack para almacenamiento de mancuernas"),
                Maquina(categoria_id=categorias[2].id, zona_id=zonas[2].id, identificador_interno="MAQ005", nombre="Banco de Estiramiento",descripcion_tecnica="Banco para ejercicios de estiramiento"),
            ]
            db.add_all(maquinas)

            # Crear 2 Planes de Suscripción
            planes = [
                PlanSuscripcion(nombre_plan="Plan Mensual", costo_actual=30.0, duracion_dias=30),
                PlanSuscripcion(nombre_plan="Plan Anual", costo_actual=300.0, duracion_dias=365)
            ]
            db.add_all(planes)
            categorias_prod = [
                CategoriaProducto(nombre_categoria="Suplementos"),
                CategoriaProducto(nombre_categoria="Ropa"),
                CategoriaProducto(nombre_categoria="Accesorios")]
            db.add_all(categorias_prod)
            await db.flush()
            # Crear 3 Productos
            productos = [
                ProductoTienda(categoria_producto_id=categorias_prod[0].id,nombre_producto="Proteína Whey 1kg", precio_actual=45.0, stock_disponible=20),
                ProductoTienda(categoria_producto_id=categorias_prod[1].id,nombre_producto="Botella de Agua 500ml", precio_actual=1.5, stock_disponible=100),
                ProductoTienda(categoria_producto_id=categorias_prod[2].id,nombre_producto="Toalla de Microfibra", precio_actual=10.0, stock_disponible=50)
            ]
            db.add_all(productos)

            # Finalizar transacción
            await db.commit()
            print("¡Datos semilla cargados exitosamente!")

        except Exception as e:
            print(f"Error durante el seeding: {e}")
            await db.rollback()

