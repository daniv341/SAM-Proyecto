from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import (
    CreateVulnerabilitieDTO,
    UpdateVulnerabilitieDTO,
    VulnerabilitieResponseDTO,
    VulnerabilitieListResponseDTO,
)
from src.vulnerabilitie.application.use_cases.create_vulnerabilitie import CreateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.get_vulnerabilitie import GetVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.update_vulnerabilitie import UpdateVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.delete_vulnerabilitie import DeleteVulnerabilitieUseCase
from src.vulnerabilitie.application.use_cases.get_vulnerabilitie_workstation import GetVulnerabilitieWorkstationsUseCase
from src.vulnerabilitie.infrastructure.api.v1.dependencies import (
    get_create_vulnerabilitie_use_case,
    get_get_vulnerabilitie_use_case,
    get_update_vulnerabilitie_use_case,
    get_delete_vulnerabilitie_use_case,
    get_get_vulnerabilitie_workstations_use_case
)

from src.workstation.application.ports.workstation_dtos import WorkstationResponseShortDTO

# esta libreria hace que debas estar autenticado para acceder a un endpoint
from src.shared.config.auth_dependencies import CurrentUser

router = APIRouter(prefix="/vulnerabilities", tags=["Vulnerabilities"])


@router.post(
    "/",
    response_model=VulnerabilitieResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo vulnerabilitie",
)
async def create_vulnerabilitie(
    dto: CreateVulnerabilitieDTO,
    use_case: Annotated[CreateVulnerabilitieUseCase, Depends(get_create_vulnerabilitie_use_case)],
    current_user: CurrentUser,
) -> VulnerabilitieResponseDTO:
    return await use_case.execute(dto)


@router.get(
    "/",
    response_model=VulnerabilitieListResponseDTO,
    summary="Listar todos los vulnerabilities",
)
async def list_vulnerabilities(
    use_case: Annotated[GetVulnerabilitieUseCase, Depends(get_get_vulnerabilitie_use_case)],
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> VulnerabilitieListResponseDTO:
    return await use_case.execute_all(skip=skip, limit=limit)


@router.get(
    "/{vulnerabilitie_id}",
    response_model=VulnerabilitieResponseDTO,
    summary="Obtener un vulnerabilitie por ID",
)
async def get_vulnerabilitie(
    vulnerabilitie_id: str,
    use_case: Annotated[GetVulnerabilitieUseCase, Depends(get_get_vulnerabilitie_use_case)],
    current_user: CurrentUser,
) -> VulnerabilitieResponseDTO:
    return await use_case.execute_by_id(vulnerabilitie_id)


@router.patch(
    "/{vulnerabilitie_id}",
    response_model=VulnerabilitieResponseDTO,
    summary="Actualizar datos de un vulnerabilitie",
)
async def update_vulnerabilitie(
    vulnerabilitie_id: str,
    dto: UpdateVulnerabilitieDTO,
    use_case: Annotated[UpdateVulnerabilitieUseCase, Depends(get_update_vulnerabilitie_use_case)],
    current_user: CurrentUser,
) -> VulnerabilitieResponseDTO:
    return await use_case.execute(vulnerabilitie_id, dto)


@router.delete(
    "/{vulnerabilitie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un vulnerabilitie",
)
async def delete_vulnerabilitie(
    vulnerabilitie_id: str,
    use_case: Annotated[DeleteVulnerabilitieUseCase, Depends(get_delete_vulnerabilitie_use_case)],
    current_user: CurrentUser,
) -> None:
    await use_case.execute(vulnerabilitie_id)


@router.get(
    "/{vulnerabilitie_id}/workstations",
    response_model=list[WorkstationResponseShortDTO],
    summary="Listar todos los workstations asociadas a la vulnerabilitie",
)
async def get_vulnerabilitie_workstations(
    vulnerabilitie_id: str,
    use_case: Annotated[GetVulnerabilitieWorkstationsUseCase, Depends(get_get_vulnerabilitie_workstations_use_case)],
    current_user: CurrentUser,
):
    return await use_case.execute(vulnerabilitie_id)