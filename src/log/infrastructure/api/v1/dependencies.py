from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository
from src.log.application.use_cases.get_log import GetLogUseCase


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_log_repository(session: SessionDep) -> SQLAlchemyLogRepository:
    return SQLAlchemyLogRepository(session)


LogRepoDep = Annotated[SQLAlchemyLogRepository, Depends(get_log_repository)]


def get_get_log_use_case(repo: LogRepoDep) -> GetLogUseCase:
    return GetLogUseCase(repo)

