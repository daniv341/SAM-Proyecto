from src.workstation.application.ports.workstation_dtos import WorkstationResponseDTO, WorkstationListResponseDTO
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.user.domain.user_repository import UserRepository

from src.user.application.ports.user_dtos import UserResponseShort

from src.workstation.application.services.workstation_validator import _to_workstation_validator, _to_workstation_response

class GetWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository, user_repository: UserRepository):
        self._repo = workstation_repository
        self._repo_user = user_repository

    async def execute_by_id(self, workstation_id: str) -> WorkstationResponseDTO:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        user = await _to_workstation_validator(workstation, self._repo_user)

        return WorkstationResponseDTO(
            id=workstation.id,
            user=UserResponseShort(
                id=user.id,
                name=user.name,
            ),
            description=workstation.description,
            status=workstation.status,
            type=workstation.type,
            area=workstation.area,
            created_at=workstation.created_at,
            updated_at=workstation.updated_at,
        )

    async def execute_all(self, skip: int = 0, limit: int = 20) -> WorkstationListResponseDTO:
        workstations = await self._repo.find_all(skip=skip, limit=limit)

        workstation_dtos = [
            await _to_workstation_response(w, self._repo_user)
            for w in workstations
        ]

        return WorkstationListResponseDTO(
            workstations=workstation_dtos,
            total=len(workstation_dtos),
            skip=skip,
            limit=limit,
        )
