from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.shared.config.settings import settings
from src.shared.database.engine import create_db_and_tables
from src.shared.exceptions.domain_exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
    InvalidValueException,
    DomainException,
)
from src.shared.exceptions.handlers import (
    entity_not_found_handler,
    entity_already_exists_handler,
    invalid_value_handler,
    domain_exception_handler,
)

# Routers
#from src.player.infrastructure.api.v1.endpoints.player_router import router as player_router
from src.user.infrastructure.api.v1.endpoints.user_router import router as user_router
from src.workstation.infrastructure.api.v1.endpoints.workstation_router import router as workstation_router
from src.vulnerabilitie.infrastructure.api.v1.endpoints.vulnerabilitie_router import router as vulnerabilitie_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: crear tablas (solo para desarrollo; en producción usar Alembic)
    if settings.DEBUG:
        await create_db_and_tables()
    yield
    # Shutdown: aquí puedes cerrar conexiones, etc.


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend para la gestion de activos de seguridad",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(EntityNotFoundException, entity_not_found_handler)
app.add_exception_handler(EntityAlreadyExistsException, entity_already_exists_handler)
app.add_exception_handler(InvalidValueException, invalid_value_handler)
app.add_exception_handler(DomainException, domain_exception_handler)

# Routers — API v1
API_PREFIX = "/api/v1"
#app.include_router(player_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
app.include_router(workstation_router, prefix=API_PREFIX)
app.include_router(vulnerabilitie_router, prefix=API_PREFIX)

# sirve para ver que todo este bien jeje
@app.get("/ok", tags=["OK"])
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
