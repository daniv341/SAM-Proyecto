from ulid import ULID

from src.workstation.application.ports.workstation_dtos import CreateWorkstationDTO, WorkstationResponseDTO
from src.workstation.domain.workstation import Workstation
from src.workstation.domain.workstation_repository import WorkstationRepository

from src.user.domain.user_repository import UserRepository

from src.user.application.ports.user_dtos import UserResponseShort

from src.workstation.application.services.workstation_validator import _to_workstation_validator

class CreateWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository, user_repository: UserRepository):
        self._repo = workstation_repository
        self._repo_user = user_repository

    async def execute(self, dto: CreateWorkstationDTO) -> WorkstationResponseDTO:

        user = await _to_workstation_validator(dto, self._repo_user)

        workstation = Workstation(
            id=str(ULID()),
            user=dto.user,
            description=dto.description,
            area=dto.area,
        )

        saved = await self._repo.save(workstation)

        return WorkstationResponseDTO(
                id=saved.id,
                user=UserResponseShort(
                    id=user.id,
                    name=user.name,
                ),
                description=saved.description,
                status=saved.status,
                type=saved.type,
                area=saved.area,
                created_at=saved.created_at,
                updated_at=saved.updated_at,
            )
