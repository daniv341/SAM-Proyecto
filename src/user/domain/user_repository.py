from abc import ABC, abstractmethod

from src.user.domain.user import User


class UserRepository(ABC):
    """
    Puerto de salida (driven port).
    Define el contrato que cualquier implementación de repositorio debe cumplir.
    """

    @abstractmethod
    async def save(self, user: User) -> User:
        """Persiste un nuevo user."""
        ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        """Busca un user por su ID."""
        ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[User]:
        """Devuelve una lista paginada de users."""
        ...

    @abstractmethod
    async def update(self, user: User) -> User:
        """Actualiza un user existente."""
        ...

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        """Elimina un user por su ID."""
        ...
