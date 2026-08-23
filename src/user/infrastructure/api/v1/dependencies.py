from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.workstation.infrastructure.repositories.sqlalchemy_workstation_repository import SQLAlchemyWorkstationRepository
from src.log.infrastructure.repositories.sqlalchemy_log_repository import SQLAlchemyLogRepository
from src.user.application.use_cases.create_user import CreateUserUseCase
from src.user.application.use_cases.get_user import GetUserUseCase
from src.user.application.use_cases.update_user import UpdateUserUseCase
from src.user.application.use_cases.delete_user import DeleteUserUseCase
from src.user.application.use_cases.login_user import LoginUserUseCase
from src.user.application.use_cases.logout_user import LogoutUserUseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_repository(session: SessionDep) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)

def get_workstation_repository(session: SessionDep) -> SQLAlchemyWorkstationRepository:
    return SQLAlchemyWorkstationRepository(session)

# debes agregar el repositorio del log en las dependenias, esto para cada caso de uso donde uses el log
def get_log_repository(session: SessionDep) -> SQLAlchemyLogRepository:
    return SQLAlchemyLogRepository(session)


UserRepoDep = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]
WorkstationRepoDep = Annotated[SQLAlchemyWorkstationRepository, Depends(get_workstation_repository)]
LogRepoDep = Annotated[SQLAlchemyLogRepository, Depends(get_log_repository)]


def get_create_user_use_case(repo: UserRepoDep, repo_log: LogRepoDep) -> CreateUserUseCase:
    return CreateUserUseCase(repo, repo_log)


# obtiene el repositorio de usuarios y retorna una instancia de LoginUserUseCase
def get_login_use_case(repo: UserRepoDep, repo_log: LogRepoDep):
    return LoginUserUseCase(repo, repo_log)
#repo=Depends(get_user_repository)

def get_logout_use_case():
    return LogoutUserUseCase()

def get_get_user_use_case(repo: UserRepoDep, repo_log: LogRepoDep) -> GetUserUseCase:
    return GetUserUseCase(repo, repo_log)


def get_update_user_use_case(repo: UserRepoDep, repo_workstation: WorkstationRepoDep, repo_log: LogRepoDep) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo, repo_workstation, repo_log)


def get_delete_user_use_case(repo: UserRepoDep, repo_log: LogRepoDep) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo, repo_log)
