from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.workstation.infrastructure.repositories.sqlalchemy_workstation_repository import SQLAlchemyWorkstationRepository
from src.user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository
from src.vulnerabilitie.infrastructure.repositories.sqlalchemy_vulnerabilitie_repository import SQLAlchemyVulnerabilitieRepository

from src.workstation.application.use_cases.create_workstation import CreateWorkstationUseCase
from src.workstation.application.use_cases.get_workstation import GetWorkstationUseCase
from src.workstation.application.use_cases.update_workstation import UpdateWorkstationUseCase
from src.workstation.application.use_cases.delete_workstation import DeleteWorkstationUseCase
from src.workstation.application.use_cases.add_vulnerabilitie_to_workstation import AddvulnerabilitieToWorkstationUseCase
from src.workstation.application.use_cases.remove_vulnerabiltie_from_workstation import RemovevulnerabilitieFromWorkstationUseCase
from src.workstation.application.use_cases.get_workstation_vulnerabilitie import GetWorkstationVulnerabilitiesUseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_workstation_repository(session: SessionDep) -> SQLAlchemyWorkstationRepository:
    return SQLAlchemyWorkstationRepository(session)

def get_user_repository(session: SessionDep) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)

def get_log_repository(session: SessionDep) -> SQLAlchemyLogRepository:
    return SQLAlchemyLogRepository(session)

def get_vulnerabilitie_repository(session: SessionDep) -> SQLAlchemyVulnerabilitieRepository:
    return SQLAlchemyVulnerabilitieRepository(session)


WorkstationRepoDep = Annotated[SQLAlchemyWorkstationRepository, Depends(get_workstation_repository)]
UserRepoDep = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]
LogRepoDep = Annotated[SQLAlchemyLogRepository, Depends(get_log_repository)]
VulnerabilitieRepoDep = Annotated[SQLAlchemyVulnerabilitieRepository, Depends(get_vulnerabilitie_repository)]


def get_create_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> CreateWorkstationUseCase:
    return CreateWorkstationUseCase(repo, repo_user, repo_log)


def get_get_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> GetWorkstationUseCase:
    return GetWorkstationUseCase(repo, repo_user, repo_log)


def get_update_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> UpdateWorkstationUseCase:
    return UpdateWorkstationUseCase(repo, repo_user, repo_log)


def get_delete_workstation_use_case(repo: WorkstationRepoDep, repo_log: LogRepoDep) -> DeleteWorkstationUseCase:
    return DeleteWorkstationUseCase(repo, repo_log)

def get_add_vulnerabilitie_workstation_use_case(repo: WorkstationRepoDep, repo_vulnerabilitie: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> AddvulnerabilitieToWorkstationUseCase:
    return AddvulnerabilitieToWorkstationUseCase(repo, repo_vulnerabilitie, repo_log)

def get_remove_vulnerabilitie_from_workstation_use_case(repo: WorkstationRepoDep, repo_vulnerabilitie: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> RemovevulnerabilitieFromWorkstationUseCase:
    return RemovevulnerabilitieFromWorkstationUseCase(repo, repo_vulnerabilitie, repo_log)

def get_get_workstation_vulnerabilities_use_case(repo: WorkstationRepoDep, repo_vulnerabilitie: VulnerabilitieRepoDep, repo_log: LogRepoDep) -> GetWorkstationVulnerabilitiesUseCase:
    return GetWorkstationVulnerabilitiesUseCase(repo, repo_vulnerabilitie, repo_log)
