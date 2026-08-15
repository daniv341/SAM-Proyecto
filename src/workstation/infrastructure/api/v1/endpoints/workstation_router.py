from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.workstation.application.ports.workstation_dtos import (
    CreateWorkstationDTO,
    UpdateWorkstationDTO,
    WorkstationResponseDTO,
    WorkstationListResponseDTO,
    WorkstationFilterDTO
)
from src.workstation.application.use_cases.create_workstation import CreateWorkstationUseCase
from src.workstation.application.use_cases.get_workstation import GetWorkstationUseCase
from src.workstation.application.use_cases.update_workstation import UpdateWorkstationUseCase
from src.workstation.application.use_cases.delete_workstation import DeleteWorkstationUseCase
from src.workstation.application.use_cases.add_vulnerability_to_workstation import AddVulnerabilityToWorkstationUseCase
from src.workstation.application.use_cases.remove_vulnerabiltie_from_workstation import RemoveVulnerabilityFromWorkstationUseCase
from src.workstation.application.use_cases.get_workstation_vulnerabilitie import GetWorkstationVulnerabilitiesUseCase
from src.workstation.infrastructure.api.v1.dependencies import (
    get_create_workstation_use_case,
    get_get_workstation_use_case,
    get_update_workstation_use_case,
    get_delete_workstation_use_case,
    get_add_vulnerabilitie_workstation_use_case,
    get_remove_vulnerabilitie_from_workstation_use_case,
    get_get_workstation_vulnerabilities_use_case
)
from src.workstation.domain.workstation import WorkstationStatus, Type, Area

from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import VulnerabilitieResponseShortDTO

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
    user: str | None = None,
    status: WorkstationStatus | None = None,
    type: Type | None = None,
    area: Area | None = None,
    created_at: datetime | None = None,
) -> WorkstationListResponseDTO:
    filters = WorkstationFilterDTO(
        user=user,
        status=status,
        type=type,
        area=area,
        created_at=created_at,
    )
    return await use_case.execute_all(filters, skip=skip, limit=limit)


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


@router.post(
    "/{workstation_id}/vulnerabilities/{vulnerability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Añadir una vulnerabilitie a un workstation",
)
async def add_vulnerability_to_workstation(
    workstation_id: str,
    vulnerability_id: str,
    use_case: Annotated[AddVulnerabilityToWorkstationUseCase, Depends(get_add_vulnerabilitie_workstation_use_case)],
) -> None:
    await use_case.execute(workstation_id=workstation_id, vulnerability_id=vulnerability_id)


@router.delete(
    "/{workstation_id}/vulnerabilities/{vulnerability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una vulnerabilitie de un workstation",
)
async def remove_vulnerability_from_workstation(
    workstation_id: str,
    vulnerability_id: str,
    use_case: Annotated[RemoveVulnerabilityFromWorkstationUseCase, Depends(get_remove_vulnerabilitie_from_workstation_use_case)],
) -> None:
    await use_case.execute(workstation_id=workstation_id, vulnerability_id=vulnerability_id)


@router.get(
    "/{workstation_id}/vulnerabilities",
    response_model=list[VulnerabilitieResponseShortDTO],
    summary="Listar todos las vulnerabilities asociadas al workstation",
)
async def get_workstation_vulnerabilities(
    workstation_id: str,
    use_case: Annotated[GetWorkstationVulnerabilitiesUseCase, Depends(get_get_workstation_vulnerabilities_use_case)],
):
    return await use_case.execute(workstation_id)