from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository
from src.log.infrastructure.repositories.log_mapper import LogMapper
from src.log.infrastructure.repositories.log_model import LogModel

from src.log.application.ports.log_dtos import LogFiltersDTO

class SQLAlchemyLogRepository(LogRepository):
    """
    Adaptador de salida (driven adapter).
    Implementación concreta del repositorio usando SQLAlchemy + SQLModel.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, log: Log) -> Log:
        model = LogMapper.to_model(log)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return LogMapper.to_domain(model)

    async def find_by_id(self, log_id: str) -> Log | None:
        result = await self._session.execute(
            select(LogModel).where(LogModel.id == log_id)
        )
        model = result.scalar_one_or_none()
        return LogMapper.to_domain(model) if model else None

    # debes ponerlo en la funcion, None es por si no agregas ningun filtro
    async def find_all(self, filters: LogFiltersDTO | None = None, skip: int = 0, limit: int = 20) -> list[Log]:
        statement = select(LogModel)

        # de esta forma el trabajo lo hace la bd y no el sistema, es para ahorrar rendimiento
        if filters:
            if filters.action:
                statement = statement.where(LogModel.action == filters.action)
            if filters.entity_type:
                statement = statement.where(LogModel.entity_type == filters.entity_type)
            if filters.entity_id:
                statement = statement.where(LogModel.entity_id == filters.entity_id)
            if filters.created_at:
                statement = statement.where(LogModel.created_at >= filters.created_at)


        result = await self._session.execute(
            statement.offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [LogMapper.to_domain(m) for m in models]
