from abc import ABC, abstractmethod

from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie


class VulnerabilitieRepository(ABC):
    """
    Puerto de salida (driven port).
    Define el contrato que cualquier implementación de repositorio debe cumplir.
    """

    @abstractmethod
    async def save(self, vulnerabilitie: Vulnerabilitie) -> Vulnerabilitie:
        """Persiste un nuevo vulnerabilitie."""
        ...

    @abstractmethod
    async def find_by_id(self, vulnerabilitie_id: str) -> Vulnerabilitie | None:
        """Busca un vulnerabilitie por su ID."""
        ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 20) -> list[Vulnerabilitie]:
        """Devuelve una lista paginada de vulnerabilities."""
        ...

    @abstractmethod
    async def update(self, vulnerabilitie: Vulnerabilitie) -> Vulnerabilitie:
        """Actualiza un vulnerabilitie existente."""
        ...

    @abstractmethod
    async def delete(self, vulnerabilitie_id: str) -> None:
        """Elimina un vulnerabilitie por su ID."""
        ...

    @abstractmethod
    async def find_workstations(self, vulnerabilitie_id: str) -> list[str]:
        """Devuelve una lista de workstations asociadas a una vulnerabilitie."""
        ...