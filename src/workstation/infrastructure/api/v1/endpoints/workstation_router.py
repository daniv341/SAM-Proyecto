from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.workstation.application.ports.workstation_dtos import (
    CreateWorkstationDTO,
    UpdateWorkstationDTO,
    WorkstationResponseDTO,
    WorkstationListResponseDTO,
)
from src.workstation.application.use_cases.create_workstation import CreateWorkstationUseCase
from src.workstation.application.use_cases.get_workstation import GetWorkstationUseCase
from src.workstation.application.use_cases.update_workstation import UpdateWorkstationUseCase
from src.workstation.application.use_cases.delete_workstation import DeleteWorkstationUseCase
from src.workstation.infrastructure.api.v1.dependencies import (
    get_create_workstation_use_case,
    get_get_workstation_use_case,
    get_update_workstation_use_case,
    get_delete_workstation_use_case,
)

router = APIRouter(prefix="/workstations", tags=["Workstations"])


@router.post(
    "/",
    response_model=WorkstationResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo workstation",
)
async def create_workstation(
    dto: CreateWorkstationDTO,
    use_case: Annotated[CreateWorkstationUseCase, Depends(get_create_workstation_use_case)],
) -> WorkstationResponseDTO:
    return await use_case.execute(dto)


@router.get(
    "/",
    response_model=WorkstationListResponseDTO,
    summary="Listar todos los workstations",
)
async def list_workstations(
    use_case: Annotated[GetWorkstationUseCase, Depends(get_get_workstation_use_case)],
    skip: int = 0,
    limit: int = 20,
) -> WorkstationListResponseDTO:
    return await use_case.execute_all(skip=skip, limit=limit)


@router.get(
    "/{workstation_id}",
    response_model=WorkstationResponseDTO,
    summary="Obtener un workstation por ID",
)
async def get_workstation(
    workstation_id: str,
    use_case: Annotated[GetWorkstationUseCase, Depends(get_get_workstation_use_case)],
) -> WorkstationResponseDTO:
    return await use_case.execute_by_id(workstation_id)


@router.patch(
    "/{workstation_id}",
    response_model=WorkstationResponseDTO,
    summary="Actualizar datos de un workstation",
)
async def update_workstation(
    workstation_id: str,
    dto: UpdateWorkstationDTO,
    use_case: Annotated[UpdateWorkstationUseCase, Depends(get_update_workstation_use_case)],
) -> WorkstationResponseDTO:
    return await use_case.execute(workstation_id, dto)


@router.delete(
    "/{workstation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un workstation",
)
async def delete_workstation(
    workstation_id: str,
    use_case: Annotated[DeleteWorkstationUseCase, Depends(get_delete_workstation_use_case)],
) -> None:
    await use_case.execute(workstation_id)
