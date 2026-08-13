from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.vulnerabilitie.infrastructure.repositories.sqlalchemy_vulnerabilitie_repository import SQLAlchemyVulnerabilitieRepository
from src.vulnerabilitie.application.use_cases.create_vulnerabilitie import CreateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.get_vulnerabilitie import GetVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.update_vulnerabilitie import UpdateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.delete_vulnerabilitie import DeleteVulnerabilitieUseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_vulnerabilitie_repository(session: SessionDep) -> SQLAlchemyVulnerabilitieRepository:
    return SQLAlchemyVulnerabilitieRepository(session)


VulnerabilitieRepoDep = Annotated[SQLAlchemyVulnerabilitieRepository, Depends(get_vulnerabilitie_repository)]


def get_create_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep) -> CreateVulnerabilitieUseCase:
    return CreateVulnerabilitieUseCase(repo)


def get_get_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep) -> GetVulnerabilitieUseCase:
    return GetVulnerabilitieUseCase(repo)


def get_update_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep) -> UpdateVulnerabilitieUseCase:
    return UpdateVulnerabilitieUseCase(repo)


def get_delete_vulnerabilitie_use_case(repo: VulnerabilitieRepoDep) -> DeleteVulnerabilitieUseCase:
    return DeleteVulnerabilitieUseCase(repo)
