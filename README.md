<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=200&section=header&text=SmartGym%20API&fontSize=60&fontColor=e94560&fontAlignY=38&desc=Plataforma%20de%20Gestión%20Integral%20para%20Gimnasios&descAlignY=60&descColor=a8b2d8&animation=fadeIn" width="100%"/>

<br/>

<!-- Shields -->
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://pyjwt.readthedocs.io/)

<br/>

[![GitHub last commit](https://img.shields.io/github/last-commit/laboratorio-1-2026-1/lab1-proyecto-2026-1-31401043-31271481-30803393?color=e94560&style=flat-square&label=Último%20Commit)](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-31401043-31271481-30803393)
[![License](https://img.shields.io/badge/Licencia-MIT-brightgreen?style=flat-square)](LICENSE)
[![API Docs](https://img.shields.io/badge/Swagger-Docs-85EA2D?style=flat-square&logo=swagger&logoColor=black)](http://localhost:8000/api-docs)

<br/>

> *API backend de alto rendimiento para la gestión integral de gimnasios — construida con las tecnologías asíncronas más modernas de Python.*

<br/>

</div>

---

## 📑 Tabla de Contenidos

| # | Sección |
|---|---------|
| 1 | [🎯 Descripción del Proyecto](#-descripción-del-proyecto) |
| 2 | [👥 Equipo de Desarrollo](#-equipo-de-desarrollo) |
| 3 | [✨ Funcionalidades Principales](#-funcionalidades-principales) |
| 4 | [🛠️ Stack Tecnológico](#️-stack-tecnológico) |
| 5 | [⚙️ Requisitos Previos](#️-requisitos-previos) |
| 6 | [🚀 Instalación y Ejecución](#-instalación-y-ejecución) |
| 7 | [📚 Documentación API](#-documentación-api) |
| 8 | [🌱 Datos Semilla](#-datos-semilla) |
| 9 | [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto) |

---

## 🎯 Descripción del Proyecto

**SmartGym API** es una aplicación backend de alta calidad, diseñada y desarrollada para gestionar todas las operaciones de un gimnasio moderno de forma eficiente y segura.

```
  Gestión de Usuarios  ──►  Roles & Permisos (RBAC)
  Máquinas & Zonas     ──►  Mantenimiento & Reservas
  Planes & Membresías  ──►  Pagos & Accesos
  Tienda de Productos  ──►  Ventas & Categorías
```

### ¿Qué hace esta API?

- 🏃 **Administra** usuarios, entrenadores y clientes con roles diferenciados
- 🏋️ **Controla** máquinas, zonas, disciplinas y sesiones del gimnasio
- 📋 **Gestiona** reservas, evaluaciones físicas y planes de suscripción
- 💳 **Procesa** membresías, pagos y control de accesos
- 🛒 **Opera** una tienda interna con productos y ventas
- 📖 **Documenta** automáticamente todos sus endpoints vía Swagger/OpenAPI
- 🌱 **Inicializa** datos semilla al arrancar, listo para usar desde el primer minuto

---

## 👥 Equipo de Desarrollo

<div align="center">

| 👤 Integrante | 🪪 Cédula | 🔗 Rol |
|:---:|:---:|:---:|
| **Carlos Romero** | C.I: 31.401.043 | Desarrollador |
| **Nickoll Pérez** | C.I: 30.803.393 | Desarrolladora |
| **Edwuar Pacheco** | C.I: 31.271.481 | Desarrollador |

</div>

---

## ✨ Funcionalidades Principales

<table>
<tr>
<td width="50%">

### 🔐 Seguridad & Acceso
- Autenticación con **JWT** (access tokens)
- Control de acceso basado en **Roles (RBAC)**
- Registro de **accesos físicos** al gimnasio
- Middleware de **logging** de peticiones HTTP

</td>
<td width="50%">

### 🗄️ Gestión de Datos
- **CRUD completo** para todas las entidades
- Migraciones automáticas con **SQLAlchemy**
- Datos semilla (seeders) ejecutados al inicio
- Motor de base de datos **100% asíncrono**

</td>
</tr>
<tr>
<td width="50%">

### 🏋️ Módulos del Gimnasio
- Usuarios, clientes y entrenadores
- Máquinas, zonas y categorías
- Disciplinas, sesiones y reservas
- Evaluaciones físicas y seguimiento

</td>
<td width="50%">

### 💼 Módulos de Negocio
- Planes de suscripción y membresías
- Control de pagos y vencimientos
- Tienda: productos, categorías y ventas
- Documentación Swagger en `/api-docs`

</td>
</tr>
</table>

---

## 🛠️ Stack Tecnológico

<div align="center">

| Capa | Tecnología | Descripción |
|:----:|:----------:|:------------|
| 🌐 **Framework Web** | FastAPI | Asíncrono, rápido, validación automática con OpenAPI |
| 🗄️ **ORM & Base de Datos** | SQLAlchemy 2.0 + asyncpg | Modo asíncrono `asyncio` con PostgreSQL |
| ✅ **Validación** | Pydantic v2 | Serialización y validación estricta de schemas |
| 🔐 **Seguridad** | PyJWT + Passlib | Tokens JWT + hashing seguro de contraseñas |
| 🐳 **Contenedores** | Docker + Compose | Despliegue aislado y reproducible |
| 📖 **Documentación** | Swagger / ReDoc | Autogenerada desde los tipos de Python |
| 🐘 **Motor de BD** | PostgreSQL 15+ | Relacional, robusto y con soporte asíncrono nativo |

</div>

---

## ⚙️ Requisitos Previos

<table>
<tr>
<td width="50%">

### 🐳 Con Docker *(Recomendado)*
Sólo necesitas instalar:

- ✅ [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) *(incluye Docker Engine y Compose)*
- ✅ **Git**

> Todo lo demás (Python, PostgreSQL, dependencias) corre **dentro de los contenedores**. No necesitas instalar nada más.

</td>
<td width="50%">

### 🖥️ Sin Docker *(Local/Manual)*
Necesitas instalar:

- ✅ **Python 3.8+**
- ✅ **Git**
- ✅ **PostgreSQL 15+** (instalado y corriendo)
- ✅ Crear manualmente la base de datos `gym`

</td>
</tr>
</table>

---

## 🚀 Instalación y Ejecución

### 🐳 Opción 1 — Docker *(Recomendado)*

> **La forma más rápida y sencilla.** Sin instalar Python ni PostgreSQL en tu máquina.

```bash
# ── Paso 1: Clona el repositorio ────────────────────────────────────────────
git clone <url-del-repositorio>
cd <nombre-del-repositorio>

# ── Paso 2: Configura tus variables de entorno ──────────────────────────────
copy .env.example.docker .env      # Windows
# cp .env.example.docker .env      # Mac / Linux

# ── Paso 3 (Opcional): Personaliza el archivo .env ──────────────────────────
# Edita .env y cambia POSTGRES_PASSWORD y SECRET_KEY por valores seguros.
# Los valores por defecto funcionan para desarrollo.

# ── Paso 4: Construye y levanta los contenedores ────────────────────────────
docker compose up --build

# ── Modo silencioso (segundo plano) ─────────────────────────────────────────
docker compose up --build -d
```

<div align="center">

| 🌐 Endpoint | 🔗 URL |
|:---:|:---:|
| **API Base** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

</div>

<details>
<summary>💡 <strong>Comandos útiles de Docker</strong> (clic para expandir)</summary>

```bash
# Ver los logs de la API en tiempo real
docker compose logs -f api

# Ver los logs de la base de datos
docker compose logs -f db

# Detener los contenedores (conserva los datos)
docker compose down

# Detener y ELIMINAR todos los datos de la BD ⚠️
docker compose down -v

# Reconstruir solo la imagen de la API (tras cambios en el código)
docker compose up --build api

# Ver el estado de los contenedores
docker compose ps
```

</details>

---

### 🖥️ Opción 2 — Local / Manual

> Requiere tener **Python 3.8+** y **PostgreSQL** instalados y configurados en tu máquina.

```bash
# ── Paso 1: Clona el repositorio ────────────────────────────────────────────
git clone <url-del-repositorio>
cd <nombre-del-repositorio>

# ── Paso 2: Crea y activa el entorno virtual ────────────────────────────────
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Mac / Linux:
source .venv/bin/activate

# ── Paso 3: Instala las dependencias ────────────────────────────────────────
pip install -r requirements.txt

# ── Paso 4: Configura tus variables de entorno ──────────────────────────────
copy .env.example.local .env      # Windows
# cp .env.example.local .env      # Mac / Linux

# ── Paso 5: Edita el archivo .env ───────────────────────────────────────────
# Ajusta DATABASE_URL con tu usuario, contraseña y nombre de BD de PostgreSQL.
# Asegúrate de haber creado la base de datos 'gym' previamente.

# ── Paso 6: Inicia la API ───────────────────────────────────────────────────
uvicorn app.main:app --reload
```

> ✅ Al iniciar, la API crea las tablas automáticamente y carga los datos semilla.

<div align="center">

| 🌐 Endpoint | 🔗 URL |
|:---:|:---:|
| **API Base** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |

</div>

---

## 📚 Documentación API

La documentación interactiva es generada automáticamente desde el código. Accede en:

🔗 **`http://localhost:8000/zdocs`**

### 🔑 Cómo autenticarse en Swagger

```
1. 📨  Haz una petición POST a  /api/v1/auth/login
       con las credenciales del usuario admin (ver sección Datos Semilla).

2. 📋  Copia el valor del campo  access_token  de la respuesta.

3. 🔓  Haz clic en el botón  [ Authorize 🔒 ]
       en la esquina superior derecha de Swagger UI.

4. 📝  Pega el token en el campo  Value  y presiona  Authorize.
       Swagger añadirá automáticamente el prefijo  Bearer  en cada petición.
```

> 💡 El token expira según el valor de `ACCESS_TOKEN_EXPIRE_MINUTES` en tu `.env` (por defecto: 30 minutos).

---

## 🌱 Datos Semilla

Al iniciar el proyecto **por primera vez**, se crean automáticamente los siguientes datos de prueba:

<div align="center">

| 🌱 Entidad | 📦 Datos creados |
|:---:|:---|
| 👤 **Administrador** | `admin@smartgym.com` / contraseña: `admin123` |
| 🎭 **Roles** | Roles fundamentales del sistema (admin, cliente, entrenador, etc.) |
| 🏋️ **Categorías de máquinas** | 3 categorías de equipamiento |
| 🤸 **Máquinas** | 5 máquinas de ejemplo con zona asignada |
| 📋 **Planes** | 2 planes de suscripción (mensual / anual) |
| 🛒 **Productos** | 3 productos en la tienda interna |

</div>

> ⚡ Los seeders son **idempotentes**: corren en cada inicio pero solo insertan datos si no existen previamente.

---

## 🏗️ Arquitectura del Proyecto

Esta API implementa una **Arquitectura Multicapa orientada al Dominio**, priorizando:

- ⚡ **Asincronía total** — motor de base de datos y endpoints 100% `async/await`
- 🧩 **Separación de responsabilidades** — cada capa tiene un único propósito
- 💉 **Inyección de dependencias** — desacoplamiento y fácil testing
- 📐 **Patrón Repositorio** — única capa autorizada para acceder a la BD

### Flujo de una petición HTTP

```
Cliente HTTP
    │
    ▼
┌─────────────────────┐
│   Router / Controller│  ← Valida entrada, coordina el flujo
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│      Service        │  ← Lógica de negocio y reglas del dominio
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│    Repository       │  ← Única capa que toca la base de datos
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  PostgreSQL (async) │  ← Motor de base de datos
└─────────────────────┘
```

### 📁 Estructura de Directorios

```
smartgym-api/
│
├── 📂 app/
│   ├── 📂 core/            → Configuración global, settings, seguridad JWT, dependencias DI
│   ├── 📂 database/        → Motor asíncrono SQLAlchemy, fábrica de sesiones
│   ├── 📂 middlewares/     → CORS, logging de peticiones HTTP, protecciones globales
│   ├── 📂 models/          → Entidades ORM que mapean las tablas de PostgreSQL
│   ├── 📂 schemas/         → Modelos Pydantic: validación de entrada y salida (DTOs)
│   ├── 📂 repositories/    → Capa de acceso a datos (Patrón Repositorio)
│   ├── 📂 services/        → Lógica de negocio y reglas del dominio
│   ├── 📂 routers/         → Controladores HTTP (Endpoints delgados)
│   ├── 📄 main.py          → Punto de entrada, ensamblaje de la aplicación
│   └── 📄 seed.py          → Seeder: inicializa datos esenciales al arrancar
│
├── 📄 .env                 → ⚠️  Variables activas (NO incluir en git)
├── 📄 .env.example.local   → 📋 Plantilla para entorno LOCAL
├── 📄 .env.example.docker  → 📋 Plantilla para entorno DOCKER
├── 📄 Dockerfile           → 🐳 Imagen Docker de la API
├── 📄 docker-compose.yml   → 🐳 Orquestación: API + PostgreSQL
├── 📄 .gitignore           → Archivos excluidos del repositorio
├── 📄 requirements.txt     → Dependencias y versiones exactas
└── 📄 README.md            → Esta documentación
```

---

## 🔐 Variables de Entorno

| Variable | Descripción | Ejemplo |
|:---------|:------------|:--------|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL | `postgresql+asyncpg://user:pass@host/db` |
| `SECRET_KEY` | Clave secreta para firmar tokens JWT | `09d25e094faa6ca...` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de vida del token (minutos) | `30` |
| `POSTGRES_USER` | Usuario de PostgreSQL *(solo Docker)* | `postgres` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL *(solo Docker)* | `mi_contraseña_segura` |
| `POSTGRES_DB` | Nombre de la base de datos *(solo Docker)* | `gym` |

> 📝 Consulta los archivos `.env.example.local` y `.env.example.docker` para instrucciones detalladas.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,50:16213e,100:0f3460&height=100&section=footer&animation=fadeIn" width="100%"/>

**SmartGym API** • Laboratorio 1 — 2026-1

*Desarrollado con ❤️ por Carlos Romero · Nickoll Pérez · Edwuar Pacheco*

[![Ask Me Anything](https://img.shields.io/badge/Preguntas-Bienvenidas-e94560?style=flat-square)](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-31401043-31271481-30803393/issues)

</div>