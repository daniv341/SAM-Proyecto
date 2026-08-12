from src.workstation.domain.workstation_repository import WorkstationRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class DeleteWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository):
        self._repo = workstation_repository

    async def execute(self, workstation_id: str) -> None:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        await self._repo.delete(workstation_id)
