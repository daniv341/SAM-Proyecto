from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database.engine import get_session
from src.user.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.user.application.use_cases.create_user import CreateUserUseCase
from src.user.application.use_cases.get_user import GetUserUseCase
from src.user.application.use_cases.update_user import UpdateUserUseCase
from src.user.application.use_cases.delete_user import DeleteUserUseCase

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_repository(session: SessionDep) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


UserRepoDep = Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)]


def get_create_user_use_case(repo: UserRepoDep) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


def get_get_user_use_case(repo: UserRepoDep) -> GetUserUseCase:
    return GetUserUseCase(repo)


def get_update_user_use_case(repo: UserRepoDep) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)


def get_delete_user_use_case(repo: UserRepoDep) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)
