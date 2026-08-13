from abc import ABC, abstractmethod

from src.log.domain.log import Log


class LogRepository(ABC):
    """
    Puerto de salida (driven port).
    Define el contrato que cualquier implementación de repositorio debe cumplir.
    """

    @abstractmethod
    async def save(self, log: Log) -> Log:
        """Persiste un nuevo log."""
        ...

    @abstractmethod
    async def find_by_id(self, log_id: str) -> Log | None:
        """Busca un log por su ID."""
        ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Log]:
        """Devuelve una lista paginada de logs."""
        ...
