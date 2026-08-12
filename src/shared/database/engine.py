from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.shared.config.settings import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, #si pones true hatr que se imprima en pantalla la configuracion que este haciendo alchemy
    future=True,
    poolclass=NullPool # abre una nueva conexion a la base de datos por cada request, no la reutiliza, es IMPORTANTE PARA LOS TEST, EN PRODUCCION QUITARLO PARA MAYOR RENDIMIENTO
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def create_db_and_tables() -> None:
    """Crea las tablas si no existen (solo para desarrollo rápido)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI para inyectar la sesión de base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
