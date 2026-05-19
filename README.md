<div align="center">

# 🏋️‍♂️ Plataforma API para Gestión Integral de Gimnasios (SmartGym)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Testing: pytest](https://img.shields.io/badge/testing-pytest-blue.svg)](https://docs.pytest.org/)

*API robusta para la gestión integral de un gimnasio, con enfoque en calidad, buenas prácticas y despliegue sencillo.*

</div>

---

## 📑 Tabla de Contenidos
- 🎯 Descripción del Proyecto
- 👥 Integrantes del equipo
- ✨ Funcionalidades Principales
- ⚙️ Requisitos Previos
- 🚀 Instalación y Ejecución
- 🧪 Pruebas
- 📚 Documentación Swagger/OpenAPI
- 🌱 Datos Semilla

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
- ✅ Pruebas unitarias con Pytest.

---

## ⚙️ Requisitos Previos

- Python 3.8+
- Docker y Docker Compose (opcional, recomendado)
- Git

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

## 🧪 Pruebas

Para ejecutar los tests unitarios:
```bash
pytest
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

> Para dudas o problemas, contacta a los autores o revisa la documentación incluida.
