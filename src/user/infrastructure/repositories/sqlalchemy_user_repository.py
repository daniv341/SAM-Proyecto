from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository
from src.user.infrastructure.repositories.user_mapper import UserMapper
from src.user.infrastructure.repositories.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """
    Adaptador de salida (driven adapter).
    Implementación concreta del repositorio usando SQLAlchemy + SQLModel.
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def find_by_id(self, user_id: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def find_all(self, skip: int = 0, limit: int = 20) -> list[User]:
        result = await self._session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [UserMapper.to_domain(m) for m in models]

    async def update(self, user: User) -> User:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()
        if not model:
            raise ValueError(f"UserModel con id \"{user.id}\" no encontrado.")

        model.name = user.name
        model.status = user.status
        model.bio = user.bio
        model.image_url = user.image_url
        model.updated_at = user.updated_at

        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def delete(self, user_id: str) -> None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
