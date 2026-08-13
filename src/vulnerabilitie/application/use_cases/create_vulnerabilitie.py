from ulid import ULID

from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import CreateVulnerabilitieDTO, VulnerabilitieResponseDTO
from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository


class CreateVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository):
        self._repo = vulnerabilitie_repository

    async def execute(self, dto: CreateVulnerabilitieDTO) -> VulnerabilitieResponseDTO:
        vulnerabilitie = Vulnerabilitie(
            id=str(ULID()),
            cve=dto.cve,
            description=dto.description,
            severity=dto.severity,
            url=dto.url,
            mitigation=dto.mitigation,
        )

        saved = await self._repo.save(vulnerabilitie)

        return VulnerabilitieResponseDTO(
            id=saved.id,
            cve=saved.cve,
            description=saved.description,
            severity=saved.severity,
            url=saved.url,
            mitigation=saved.mitigation,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
