# SAM API

Backend para la gestión de usuarios, estaciones de trabajo, vulnerabilidades y auditoría de eventos, desarrollado con FastAPI, SQLModel y PostgreSQL.

La aplicación sigue una estructura basada en arquitectura hexagonal, separando dominio, casos de uso e infraestructura para facilitar mantenimiento, extensión y pruebas.

## Características principales

- API REST con FastAPI
- Autenticación y autorización con JWT
- Gestión de usuarios con roles y estados
- Administración de estaciones de trabajo
- Registro y relación de vulnerabilidades con estaciones
- Registro de auditoría/logs de acciones del sistema
- Persistencia con PostgreSQL y SQLModel
- Migraciones con Alembic
- Documentación automática con Swagger UI y Redoc
- Soporte para tests automatizados con pytest

## Tecnologías y dependencias utilizadas

### Backend y API
- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic y Pydantic Settings
- SQLModel
- SQLAlchemy

### Base de datos y migraciones
- PostgreSQL
- asyncpg
- Alembic

### Seguridad y autenticación
- python-jose
- bcrypt
- JWT

### Utilidades
- python-ulid
- email-validator
- httpx

### Testing
- pytest
- pytest-asyncio
- pytest-cov

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.11 o superior
- PostgreSQL 12+ o superior
- Git
- Un cliente HTTP opcional como Postman / curl para pruebas manuales

Verifica la instalación:

```bash
python --version
psql --version
```

## Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd SAM
```

### 2. Crear un entorno virtual

```bash
python -m venv .venv
```

Activa el entorno virtual:

En Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

En Windows (CMD):

```cmd
.venv\Scripts\activate.bat
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido de ejemplo:

```env
APP_NAME=SAM API
APP_VERSION=0.1.0
DEBUG=true
SECRET_KEY=cambia-esta-clave-por-una-mas-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/sam_db
HOST=0.0.0.0
PORT=8000
```

Asegúrate de que la base de datos PostgreSQL exista y que el usuario y contraseña coincidan con los valores configurados.

### 5. Crear la base de datos PostgreSQL

Ejemplo:

```sql
CREATE DATABASE sam_db;
```

### 6. Ejecutar migraciones

```bash
alembic upgrade head
```

Si aún no existe una migración inicial o necesitas generarla desde los modelos:

```bash
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

### 7. Crear usuario administrador

El proyecto incluye un script para crear un administrador inicial:

```bash
python -m src.shared.config.create_admin
```

Se te pedirá ingresar:
- email del administrador
- contraseña
- confirmación de contraseña

### 8. Iniciar la API

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

La documentación interactiva estará disponible en:

- Swagger: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Guía rápida de uso

### Verificar estado del servicio

```bash
curl http://localhost:8000/ok
```

Respuesta esperada:

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### Registrar un usuario

```bash
curl -X POST "http://localhost:8000/api/v1/users/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana",
    "email": "ana@example.com",
    "password": "Secret123!",
    "date_of_birth": "1998-04-15T00:00:00Z",
    "role": "USER"
  }'
```

> Este endpoint requiere autenticación de administrador según la implementación actual del proyecto.

### Iniciar sesión

```bash
curl -X POST "http://localhost:8000/api/v1/users/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "your_password"
  }'
```

Respuesta típica:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

### Consumir endpoints protegidos

```bash
curl -X GET "http://localhost:8000/api/v1/workstations/" \
  -H "Authorization: Bearer <token>"
```

## Endpoints principales

La API expone módulos agrupados por dominio:

- `/api/v1/users` — gestión de usuarios y autenticación
- `/api/v1/workstations` — gestión de estaciones de trabajo
- `/api/v1/vulnerabilities` — gestión de vulnerabilidades
- `/api/v1/logs` — consulta de auditoría y eventos del sistema

La aplicación incluye además rutas para:
- registro de usuarios
- login/logout
- consulta de perfil actual
- listado y filtrado por distintos campos
- creación de relaciones entre estaciones y vulnerabilidades
- consulta de auditoría

## Estructura de carpetas

```text
SAM/
├── alembic/                          # Migraciones de base de datos
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── src/                             # Código fuente principal
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── models.py
│   ├── log/                        # Módulo de logs/auditoría
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── shared/                     # Utilidades compartidas
│   │   ├── config/
│   │   ├── database/
│   │   └── exceptions/
│   ├── user/                       # Módulo de usuarios
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── vulnerabilitie/             # Módulo de vulnerabilidades
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   └── workstation/                # Módulo de estaciones de trabajo
│       ├── domain/
│       ├── application/
│       └── infrastructure/
├── tests/                           # Casos de prueba
│   ├── user/
│   ├── workstation/
│   ├── vulnerabilitie/
│   └── log/
├── .env                             # Variables de entorno locales
├── alembic.ini                      # Configuración de Alembic
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Documentación del proyecto
└── src/__init__.py
```

## Ejecutar pruebas

```bash
pytest -q
```

Con cobertura:

```bash
pytest --cov=src --cov-report=term-missing
```

## Buenas prácticas recomendadas

- No commitear archivos `.env` con datos reales
- Usar contraseñas fuertes y claves secretas distintas por entorno
- En producción, ajustar CORS y activar configuración segura
- Mantener las migraciones con Alembic como fuente de verdad del esquema
- Usar roles y permisos de forma explícita para cada endpoint

El proyecto está diseñado para ser una API de gestión de activos y vulnerabilidades con un enfoque profesional, modular y escalable.
