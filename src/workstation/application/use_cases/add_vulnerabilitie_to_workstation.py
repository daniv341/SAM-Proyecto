from ulid import ULID

from src.shared.exceptions.domain_exceptions import EntityNotFoundException, InvalidValueException
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class AddvulnerabilitieToWorkstationUseCase:

    def __init__(self, workstation_repository: WorkstationRepository, vulnerabilitie_repository: VulnerabilitieRepository, log_repository: LogRepository):
        self._repo = workstation_repository
        self._repo_vulnerabilitie = vulnerabilitie_repository
        self._repo_log = log_repository

    async def execute(self, workstation_id: str, vulnerabilitie_id: str) -> None:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        vulnerabilitie = await self._repo_vulnerabilitie.find_by_id(vulnerabilitie_id)
        if not vulnerabilitie:
            raise EntityNotFoundException("vulnerabilitie", vulnerabilitie_id)

        exists = await self._repo.vulnerabilitie_exists(workstation_id, vulnerabilitie_id)
        if exists:
            raise InvalidValueException("La workstation ingresada ya está asociada a esta vulnerabilitie")

        workstation.ban()

        await self._repo.update(workstation)

        await self._repo.add_vulnerabilitie(workstation_id, vulnerabilitie_id)

        log = Log(
            id=str(ULID()),
            action="ALERT",
            entity_type="WORKSTATION",
            entity_id=workstation.id,
            description=f"Workstation {workstation.id} from User {workstation.user} was banned from the system due to the threat {vulnerabilitie.cve}"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)