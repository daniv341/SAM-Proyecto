from ulid import ULID

from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class DeleteVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository, log_repository: LogRepository):
        self._repo = vulnerabilitie_repository
        self._repo_log = log_repository

    async def execute(self, vulnerabilitie_id: str) -> None:
        vulnerabilitie = await self._repo.find_by_id(vulnerabilitie_id)
        if not vulnerabilitie:
            raise EntityNotFoundException("Vulnerabilitie", vulnerabilitie_id)

        await self._repo.delete(vulnerabilitie_id)

        log = Log(
            id=str(ULID()),
            action="DELETE",
            entity_type="VULNERABILITIE",
            entity_id=vulnerabilitie.id,
            description=f"Vulnerabilitie {vulnerabilitie.cve} deleted"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)
