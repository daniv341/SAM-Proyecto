from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import UpdateVulnerabilitieDTO, VulnerabilitieResponseDTO
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class UpdateVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository):
        self._repo = vulnerabilitie_repository

    async def execute(self, vulnerabilitie_id: str, dto: UpdateVulnerabilitieDTO) -> VulnerabilitieResponseDTO:
        vulnerabilitie = await self._repo.find_by_id(vulnerabilitie_id)
        if not vulnerabilitie:
            raise EntityNotFoundException("Vulnerabilitie", vulnerabilitie_id)

        if dto.description is not None:
            vulnerabilitie.description = dto.description
        if dto.mitigation is not None:
            vulnerabilitie.mitigation = dto.mitigation

        vulnerabilitie._touch()
        updated = await self._repo.update(vulnerabilitie)

        return VulnerabilitieResponseDTO(
            id=updated.id,
            cve=updated.cve,
            description=updated.description,
            severity=updated.severity,
            url=updated.url,
            mitigation=updated.mitigation,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
