from ulid import ULID

from src.workstation.application.ports.workstation_dtos import WorkstationResponseDTO, WorkstationListResponseDTO, WorkstationFilterDTO
from src.workstation.domain.workstation_repository import WorkstationRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException

from src.user.domain.user_repository import UserRepository

from src.user.application.ports.user_dtos import UserResponseShort

from src.workstation.application.services.workstation_validator import _to_workstation_validator, _to_workstation_response

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class GetWorkstationUseCase:
    def __init__(self, workstation_repository: WorkstationRepository, user_repository: UserRepository, log_repository: LogRepository):
        self._repo = workstation_repository
        self._repo_user = user_repository
        self._repo_log = log_repository

    async def execute_by_id(self, workstation_id: str) -> WorkstationResponseDTO:
        workstation = await self._repo.find_by_id(workstation_id)
        if not workstation:
            raise EntityNotFoundException("Workstation", workstation_id)

        user = await _to_workstation_validator(workstation, self._repo_user)

        log = Log(
            id=str(ULID()),
            action="GET",
            entity_type="WORKSTATION",
            entity_id=workstation.id,
            description=f"Workstation {workstation.type} from User {workstation.user} get"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

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

    async def execute_all(self, filters: WorkstationFilterDTO | None = None, skip: int = 0, limit: int = 20) -> WorkstationListResponseDTO:
        workstations = await self._repo.find_all(filters, skip=skip, limit=limit)

        workstation_dtos = [
            await _to_workstation_response(w, self._repo_user)
            for w in workstations
        ]

        log = Log(
            id=str(ULID()),
            action="GETALL",
            entity_type="WORKSTATION",
            entity_id="None",
            description=f"Get All ejecuted"
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log) 

        return WorkstationListResponseDTO(
            workstations=workstation_dtos,
            total=len(workstation_dtos),
            skip=skip,
            limit=limit,
        )
