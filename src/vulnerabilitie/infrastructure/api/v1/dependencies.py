from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.vulnerabilitie.infrastructure.repositories.sqlalchemy_vulnerabilitie_repository import SQLAlchemyVulnerabilitieRepository
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository
from src.vulnerabilitie.application.use_cases.create_vulnerabilitie import CreateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.get_vulnerabilitie import GetVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.update_vulnerabilitie import UpdateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.delete_vulnerabilitie import DeleteVulnerabilitieUseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_vulnerabilitie_repository(session: SessionDep) -> SQLAlchemyVulnerabilitieRepository:
    return SQLAlchemyVulnerabilitieRepository(session)

def get_log_repository(session: SessionDep) -> SQLAlchemyLogRepository:
    return SQLAlchemyLogRepository(session)


VulnerabilitieRepoDep = Annotated[SQLAlchemyVulnerabilitieRepository, Depends(get_vulnerabilitie_repository)]
LogRepoDep = Annotated[SQLAlchemyLogRepository, Depends(get_log_repository)]


def get_create_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> CreateVulnerabilitieUseCase:
    return CreateVulnerabilitieUseCase(repo, repo_log)


def get_get_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> GetVulnerabilitieUseCase:
    return GetVulnerabilitieUseCase(repo, repo_log)


def get_update_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> UpdateVulnerabilitieUseCase:
    return UpdateVulnerabilitieUseCase(repo, repo_log)


def get_delete_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> DeleteVulnerabilitieUseCase:
    return DeleteVulnerabilitieUseCase(repo, repo_log)
