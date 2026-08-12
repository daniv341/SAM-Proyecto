from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.workstation.infrastructure.repositories.sqlalchemy_workstation_repository import SQLAlchemyWorkstationRepository
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

WorkstationRepoDep = Annotated[SQLAlchemyWorkstationRepository, Depends(get_workstation_repository)]
UserRepoDep = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]

def get_create_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep) -> CreateWorkstationUseCase:
    return CreateWorkstationUseCase(repo, repo_user)


def get_get_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep) -> GetWorkstationUseCase:
    return GetWorkstationUseCase(repo, repo_user)


def get_update_workstation_use_case(repo: WorkstationRepoDep, repo_user: UserRepoDep) -> UpdateWorkstationUseCase:
    return UpdateWorkstationUseCase(repo, repo_user)


def get_delete_workstation_use_case(repo: WorkstationRepoDep) -> DeleteWorkstationUseCase:
    return DeleteWorkstationUseCase(repo)
