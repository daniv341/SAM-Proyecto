from ulid import ULID

from src.workstation.domain.workstation_repository import WorkstationRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class DeleteWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository,  log_repository: LogRepository):
        self._repo = workstation_repository
        self._repo_log = log_repository

    async def execute(self, workstation_id: str) -> None:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        await self._repo.delete(workstation_id)

        log = Log(
            id=str(ULID()),
            action="DELETE",
            entity_type="WORKSTATION",
            entity_id=workstation.id,
            description=f"Workstation {workstation.type} from User {workstation.user} deleted"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)
