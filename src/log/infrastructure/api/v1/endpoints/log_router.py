from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.log.application.ports.log_dtos import (
    CreateLogDTO,
    LogResponseDTO,
    LogListResponseDTO,
)
from src.log.application.use_cases.get_log import GetLogUseCase
from src.log.infrastructure.api.v1.dependencies import (
    get_get_log_use_case,
)

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
) -> LogListResponseDTO:
    return await use_case.execute_all(skip=skip, limit=limit)


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

