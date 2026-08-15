from ulid import ULID

from src.shared.exceptions.domain_exceptions import EntityNotFoundException
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class GetVulnerabilitieWorkstationsUseCase:
    def __init__(self,vulnerabilitie_repository: VulnerabilitieRepository, workstation_repository: WorkstationRepository, log_repository: LogRepository):
        self._repo = vulnerabilitie_repository
        self._repo_workstation = workstation_repository
        self._repo_log = log_repository

    async def execute(self, vulnerabilitie_id: str):
        vulnerabilitie = await self._repo.find_by_id(vulnerabilitie_id)

        if not vulnerabilitie:
            raise EntityNotFoundException("Workstation", vulnerabilitie_id)

        workstation_ids = await self._repo.find_workstations(vulnerabilitie_id)

        workstations = []

        for workstation_id in workstation_ids:
            workstation =  await self._repo_workstation.find_by_id(workstation_id)

            if workstation:
                workstations.append(workstation)

        log = Log(
            id=str(ULID()),
            action="GETALL",
            entity_type="VULNERABILITIE",
            entity_id=vulnerabilitie.id,
            description=f"Vulnerabilitie {vulnerabilitie.cve} geted all historial workstations affected"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

        return workstations