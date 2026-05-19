<div align="center">

# 🏋️‍♂️ Plataforma API para Gestión Integral de Gimnasios (SmartGym)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-D71F00?style=flat&logo=python&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24%2B-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![JWT](https://img.shields.io/badge/PyJWT-2.8%2B-000000?style=flat&logo=jsonwebtokens&logoColor=white)](https://pyjwt.readthedocs.io/)
[![GitHub last commit](https://img.shields.io/github/last-commit/laboratorio-1-2026-1/lab1-proyecto-2026-1-31401043-31271481-30803393?color=red)](https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-31401043-31271481-30803393)

*API robusta para la gestión integral de un gimnasio, con enfoque en calidad, buenas prácticas y despliegue sencillo.*

</div>

---

## 📑 Tabla de Contenidos
- 🎯 Descripción del Proyecto
- 👥 Integrantes del equipo
- ✨ Funcionalidades Principales
- ⚙️ Requisitos Previos
- 🛠️ Stack Tecnológico
- 🚀 Instalación y Ejecución
- 📚 Documentación Swagger/OpenAPI
- 🌱 Datos Semilla
- 🏗️ Arquitectura del Proyecto

---

## 🎯 Descripción del Proyecto

Es una aplicación backend desarrollada para administrar usuarios, roles, máquinas, productos de tienda, membresías, reservas y más.  
Incluye documentación Swagger/OpenAPI y datos semilla para pruebas automáticas al iniciar el sistema.

---

## 👥 Integrantes del equipo

| Nombre | Cédula |
| :--- | :--- |
| **Carlos Romero** | C.I: 31.401.043 |
| **Nickoll Pérez** | C.I: 30.803.393 |
| **Edwuar Pacheco** | C.I: 31.271.481 |

---

## ✨ Funcionalidades Principales

- ✅ CRUD de usuarios, roles, máquinas, productos, membresías, reservas, etc.
- ✅ Documentación Swagger/OpenAPI autogenerada (`/api-docs`).
- ✅ Seeders automáticos: usuario admin, roles, categorías, máquinas, planes y productos.
---

## ⚙️ Requisitos Previos

- Python 3.8+
- Docker y Docker Compose (opcional, recomendado)
- Git
- PostgreSQL (Motor de base de datos relacional)
- Docker y Docker Compose (Opcional, pero altamente recomendado para levantar la base de datos de forma aislada).
---
## 🛠️ Stack Tecnológico

Este proyecto está construido aprovechando el ecosistema asíncrono más moderno de Python, garantizando alto rendimiento y seguridad:

* **Framework Web:** FastAPI (Asíncrono, rápido y basado en estándares OpenAPI).
* **ORM y Datos:** SQLAlchemy (en modo asíncrono `asyncio`) + PostgreSQL.
* **Validación y Serialización:** Pydantic.
* **Seguridad:** Autenticación basada en JSON Web Tokens (JWT) y control de acceso por Roles (RBAC).
* **Calidad de Código (Tooling):** Entorno virtual aislado (`.venv`).
---
## 🚀 Instalación y Ejecución

### Opción 1: Docker (recomendado)
```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
docker-compose up --build
```
La API estará disponible en: http://localhost:8000

### Opción 2: Manual
```bash
python -m venv .venv
# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
---

## 📚 Documentación Swagger/OpenAPI

- Accede a la documentación interactiva en: `http://localhost:8000/api-docs`

---

## 🌱 Datos Semilla

Al iniciar el proyecto por primera vez, se crean automáticamente:
- 1 usuario administrador
- Roles fundamentales
- 3 categorías de máquinas y 5 máquinas de ejemplo
- 2 planes de suscripción
- 3 productos en la tienda

---

## 🏗️ Arquitectura del Proyecto

Esta API está construida sobre **FastAPI** implementando una **Arquitectura Multicapa orientada al Dominio**. El diseño prioriza la asincronía, la separación de responsabilidades y la inyección de dependencias para garantizar que el código sea escalable, altamente testeable y fácil de mantener en equipo.

### 📁 Estructura de Directorios

```text
├── app/
│   ├── core/          # Configuraciones globales, variables de entorno, seguridad y dependencias (Inyección).
│   ├── database/      # Configuración de la infraestructura de BD (Motor asíncrono y Fábrica de Sesiones).
│   ├── middlewares/   # Interceptores globales para peticiones HTTP (CORS, logging, protección).
│   ├── models/        # Entidades ORM (SQLAlchemy) que mapean exactamente las tablas de la base de datos.
│   ├── schemas/       # Modelos Pydantic encargados de la validación estricta de entrada y salida (Filtros).
│   ├── repositories/  # Única capa autorizada para interactuar con la base de datos (Patrón Repositorio).
│   ├── services/      # Corazón de la aplicación: alberga toda la lógica y reglas de negocio.
│   ├── routers/       # Controladores delgados (Endpoints) que solo coordinan el tráfico HTTP.
|   ├── main.py        # Punto de entrada de la aplicación y ensamblaje de los componentes.
│   └── seed.py        # Script de inicialización (Seeder) para poblar la base de datos con datos semilla esenciales.
├── .env               # Archivo local de variables de entorno (claves secretas, credenciales de BD).
├── .gitignore         # Archivos y carpetas excluidos del control de versiones (como .venv).
├── README.md          # Documentación principal y guía de inicio rápido
└── requirements.txt   # Lista de dependencias y librerías del proyecto con sus versiones exactas.
---

> Para dudas o problemas, contacta a los autores o revisa la documentación incluida.
