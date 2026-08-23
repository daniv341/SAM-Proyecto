from abc import ABC, abstractmethod

from src.workstation.domain.workstation import Workstation
from src.workstation.application.ports.workstation_dtos import WorkstationFilterDTO

from src.user.domain.user import User

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
    async def find_by_user_id(self, user_id: str) -> User | None:
        """Busca un workstation por su ID de User."""
        ...

    @abstractmethod
    async def find_all(self, filters: WorkstationFilterDTO | None = None, skip: int = 0, limit: int = 20) -> list[Workstation]:
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

# metodos para manejar la relacion many to many entre workstation y vulnerabilidades
    @abstractmethod
    async def add_vulnerabilitie(self, workstation_id: str, vulnerabilitie_id: str) -> None:
        """Añade una vulnerabilidad a un workstation."""
        ...

    @abstractmethod
    async def vulnerabilitie_exists(self, workstation_id: str, vulnerabilitie_id: str) -> bool:
        """Comprueba que la relacion entre una Vulnerabilitie y un Workstation no exista ya"""

    @abstractmethod
    async def remove_vulnerabilitie(self, workstation_id: str, vulnerabilitie_id: str) -> None:
        """Elimina una vulnerabilidad de un workstation."""
        ...

    @abstractmethod
    async def find_vulnerabilities(self, workstation_id: str) -> list[str]:
        """Devuelve una lista de vulnerabilities asociadas a un workstation."""
        ...
