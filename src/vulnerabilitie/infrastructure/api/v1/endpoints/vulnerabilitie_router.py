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
from src.vulnerabilitie.infrastructure.api.v1.dependencies import (
    get_create_vulnerabilitie_use_case,
    get_get_vulnerabilitie_use_case,
    get_update_vulnerabilitie_use_case,
    get_delete_vulnerabilitie_use_case,
)

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
) -> VulnerabilitieResponseDTO:
    return await use_case.execute(dto)


@router.get(
    "/",
    response_model=VulnerabilitieListResponseDTO,
    summary="Listar todos los vulnerabilities",
)
async def list_vulnerabilities(
    use_case: Annotated[GetVulnerabilitieUseCase, Depends(get_get_vulnerabilitie_use_case)],
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
) -> None:
    await use_case.execute(vulnerabilitie_id)
