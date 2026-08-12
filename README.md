# 🎮 eSports Championship API

Backend para la gestión de activos de seguridad construido con **FastAPI**, **PostgreSQL**, **SQLModel** y **Arquitectura Hexagonal**.

---

## 📋 Requisitos previos

Antes de empezar necesitás tener instalado en tu máquina:

- **Python 3.11 o superior** → [python.org/downloads](https://www.python.org/downloads/)
- **PostgreSQL** corriendo localmente con una base de datos llamada `eSports`

Para verificar que los tenés:
```bash
python --version    # debe mostrar 3.11.x o superior
psql --version      # debe mostrar la versión de PostgreSQL
```

---

## 🐍 Entorno virtual

python -m venv .venv

---

## 🚀 Instalación y configuración

Todos los pasos siguientes asumen que el entorno virtual está activo.

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Abrí el archivo .env y completá segun tu configuracion


El nombre de la base de datos es case-sensitive

### 3. Aplicar migraciones

```bash
# Genera el archivo de migración detectando los modelos del código
alembic revision --autogenerate -m "initial tables"

# Revisá el archivo generado en alembic/versions/ para confirmar que sea correcto
# Luego aplicá la migración
alembic upgrade head
```

### 4. Levantar el servidor

```bash
uvicorn src.main:app --reload
```

El flag --reload hace que el servidor se reinicie automáticamente cada vez que guardás un archivo.

---

## Verificar que todo funciona

Con el servidor corriendo, abrí en el navegador:

- http://localhost:8000/health  →  debe retornar {"status": "ok"}
- http://localhost:8000/docs    →  documentación interactiva (Swagger UI)
- http://localhost:8000/redoc   →  documentación alternativa (ReDoc)

---

## 🧪 Correr los tests

```bash
# Todos los tests
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 📡 Endpoints disponibles

### Players
| Método | Ruta | Descripción |
|--------|------|-------------|


---

## 🏗️ Estructura del proyecto

```
src/
├── main.py
├── shared/
│   ├── config/settings.py
│   ├── database/engine.py
│   └── exceptions/
├── personal/

alembic/
tests/
requirements.txt
.env.example
```

Cada módulo sigue la misma estructura de Arquitectura Hexagonal:
```
modulo/
├── domain/          → entidad pura + interfaz del repositorio (sin frameworks)
├── application/     → casos de uso + DTOs
└── infrastructure/  → SQLModel + repositorio concreto + router FastAPI
```
