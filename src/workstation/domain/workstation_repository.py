from abc import ABC, abstractmethod

from src.workstation.domain.workstation import Workstation


class WorkstationRepository(ABC):
    """
    Puerto de salida (driven port).
    Define el contrato que cualquier implementación de repositorio debe cumplir.
    """

    @abstractmethod
    async def save(self, workstation: Workstation) -> Workstation:
        """Persiste un nuevo workstation."""
        ...

    @abstractmethod
    async def find_by_id(self, workstation_id: str) -> Workstation | None:
        """Busca un workstation por su ID."""
        ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Workstation]:
        """Devuelve una lista paginada de workstations."""
        ...

    @abstractmethod
    async def update(self, workstation: Workstation) -> Workstation:
        """Actualiza un workstation existente."""
        ...

    @abstractmethod
    async def delete(self, workstation_id: str) -> None:
        """Elimina un workstation por su ID."""
        ...
