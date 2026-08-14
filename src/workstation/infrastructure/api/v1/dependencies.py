from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.workstation.infrastructure.repositories.sqlalchemy_workstation_repository import SQLAlchemyWorkstationRepository
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository
from src.workstation.application.use_cases.create_workstation import CreateWorkstationUseCase
from src.workstation.application.use_cases.get_workstation import GetWorkstationUseCase
from src.workstation.application.use_cases.update_workstation import UpdateWorkstationUseCase
from src.workstation.application.use_cases.delete_workstation import DeleteWorkstationUseCase

from src.user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_workstation_repository(session: SessionDep) -> SQLAlchemyWorkstationRepository:
    return SQLAlchemyWorkstationRepository(session)

def get_user_repository(session: SessionDep) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)

def get_log_repository(session: SessionDep) -> SQLAlchemyLogRepository:
    return SQLAlchemyLogRepository(session)


WorkstationRepoDep = Annotated[SQLAlchemyWorkstationRepository, Depends(get_workstation_repository)]
UserRepoDep = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]
LogRepoDep = Annotated[SQLAlchemyLogRepository, Depends(get_log_repository)]


def get_create_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> CreateWorkstationUseCase:
    return CreateWorkstationUseCase(repo, repo_user, repo_log)


def get_get_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> GetWorkstationUseCase:
    return GetWorkstationUseCase(repo, repo_user, repo_log)


def get_update_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep, repo_log: LogRepoDep) -> UpdateWorkstationUseCase:
    return UpdateWorkstationUseCase(repo, repo_user, repo_log)


def get_delete_workstation_use_case(repo: WorkstationRepoDep, repo_log: LogRepoDep) -> DeleteWorkstationUseCase:
    return DeleteWorkstationUseCase(repo, repo_log)
