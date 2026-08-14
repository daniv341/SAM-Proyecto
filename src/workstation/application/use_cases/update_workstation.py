from ulid import ULID

from src.workstation.application.ports.workstation_dtos import UpdateWorkstationDTO, WorkstationResponseDTO
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.user.domain.user_repository import UserRepository

from src.user.application.ports.user_dtos import UserResponseShort

from src.workstation.application.services.workstation_validator import _to_update_workstation_validator

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class UpdateWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = workstation_repository
        self._repo_user = user_repository
        self._repo_log = log_repository

    async def execute(self, workstation_id: str, dto: UpdateWorkstationDTO) -> WorkstationResponseDTO:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        user = await self._repo_user.find_by_id(dto.user)
        if not user:
            raise EntityNotFoundException("User", dto.user)
        
        user = await _to_update_workstation_validator(workstation, self._repo_user)

        if dto.user is not None:
            workstation.user = dto.user
        if dto.description is not None:
            workstation.description = dto.description
        if dto.status is not None:
            workstation.status = dto.status
        if dto.type is not None:
            workstation.type = dto.type
        if dto.area is not None:
            workstation.area = dto.area

        workstation._touch()
        updated = await self._repo.update(workstation)

        user = await self._repo_user.find_by_id(updated.user)

        log = Log(
            id=str(ULID()),
            action="UPDATE",
            entity_type="WORKSTATION",
            entity_id=workstation.id,
            description=f"Workstation {workstation.type} from User {workstation.user} updated"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

        return WorkstationResponseDTO(
            id=updated.id,
            user=UserResponseShort(
                id=user.id,
                name=user.name,
            ),
            description=updated.description,
            status=updated.status,
            type=updated.type,
            area=updated.area,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
