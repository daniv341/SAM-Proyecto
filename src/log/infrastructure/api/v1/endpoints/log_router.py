from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.log.application.ports.log_dtos import (
    LogResponseDTO,
    LogListResponseDTO,
    LogFilterDTO
)
from src.log.application.use_cases.get_log import GetLogUseCase
from src.log.infrastructure.api.v1.dependencies import (
    get_get_log_use_case,
)
from src.log.domain.log import AuditAction, EntityType

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get(
    "/",
    response_model=LogListResponseDTO,
    summary="Listar todos los logs",
)
async def list_logs(
    use_case: Annotated[GetLogUseCase, Depends(get_get_log_use_case)],
    skip: int = 0,
    limit: int = 20,
    action: AuditAction | None = None, # debes añadirlos al endpoint si quieres que salgan en Swagger
    entity_type: EntityType | None = None,
    entity_id: str | None = None,
    created_at: datetime | None = None,
) -> LogListResponseDTO:
    filters = LogFilterDTO( # aqui asignas los valores que ingresaste en el swagger
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=created_at,
    )
    return await use_case.execute_all(filters, skip=skip, limit=limit)


@router.get(
    "/{log_id}",
    response_model=LogResponseDTO,
    summary="Obtener un log por ID",
)
async def get_log(
    log_id: str,
    use_case: Annotated[GetLogUseCase, Depends(get_get_log_use_case)],
) -> LogResponseDTO:
    return await use_case.execute_by_id(log_id)

