from ulid import ULID

from src.shared.exceptions.domain_exceptions import EntityNotFoundException
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class GetWorkstationVulnerabilitiesUseCase:
    def __init__(self, workstation_repository: WorkstationRepository, vulnerabilitie_repository: VulnerabilitieRepository, log_repository: LogRepository):
        self._repo = workstation_repository
        self._repo_vulnerabilitie = vulnerabilitie_repository
        self._repo_log = log_repository

    async def execute(self, workstation_id: str):
        workstation = await self._repo.find_by_id(workstation_id)

        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        vulnerabilitie_ids = await self._repo.find_vulnerabilities(workstation_id)

        vulnerabilities = []

        for vulnerabilitie_id in vulnerabilitie_ids:
            vulnerabilitie = await self._repo_vulnerabilitie.find_by_id(vulnerabilitie_id)

            if vulnerabilitie:
                vulnerabilities.append(vulnerabilitie)

        log = Log(
            id=str(ULID()),
            action="GETALL",
            entity_type="WORKSTATION",
            entity_id=workstation.id,
            description=f"Workstation {workstation.id} from User {workstation.user} geted all historial vulnerabilties"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

        return vulnerabilities