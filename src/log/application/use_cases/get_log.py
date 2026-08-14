from src.log.application.ports.log_dtos import LogResponseDTO, LogListResponseDTO, LogFiltersDTO
from src.log.domain.log_repository import LogRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class GetLogUseCase:
    def __init__(self, log_repository: LogRepository):
        self._repo = log_repository

    async def execute_by_id(self, log_id: str) -> LogResponseDTO:
        log = await self._repo.find_by_id(log_id)
        if not log:
            raise EntityNotFoundException("Log", log_id)

        return LogResponseDTO(
            id=log.id,
            action=log.action,
            entity_type=log.entity_type,
            entity_id=log.entity_id,
            description=log.description,
            created_at=log.created_at
        )

    # debes ponerlo en la funcion, None es por si no agregas ningun filtro
    async def execute_all(self, filters: LogFiltersDTO | None = None, skip: int = 0, limit: int = 20) -> LogListResponseDTO:
        # los demas parametros que no sean los argumentos claves deben ir primeros
        logs = await self._repo.find_all(filters, skip=skip, limit=limit)

        log_dtos = [
            LogResponseDTO(
                id=l.id,
                action=l.action,
                entity_type=l.entity_type,
                entity_id=l.entity_id,
                description=l.description,
                created_at=l.created_at
            )
            for l in logs
        ]

        return LogListResponseDTO(
            logs=log_dtos,
            total=len(log_dtos),
            skip=skip,
            limit=limit,
        )
