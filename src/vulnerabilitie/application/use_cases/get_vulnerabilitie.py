from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import VulnerabilitieResponseDTO, VulnerabilitieListResponseDTO
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class GetVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository):
        self._repo = vulnerabilitie_repository

    async def execute_by_id(self, vulnerabilitie_id: str) -> VulnerabilitieResponseDTO:
        vulnerabilitie = await self._repo.find_by_id(vulnerabilitie_id)
        if not vulnerabilitie:
            raise EntityNotFoundException("Vulnerabilitie", vulnerabilitie_id)

        return VulnerabilitieResponseDTO(
            id=vulnerabilitie.id,
            cve=vulnerabilitie.cve,
            description=vulnerabilitie.description,
            severity=vulnerabilitie.severity,
            url=vulnerabilitie.url,
            mitigation=vulnerabilitie.mitigation,
            created_at=vulnerabilitie.created_at,
            updated_at=vulnerabilitie.updated_at,
        )

    async def execute_all(self, skip: int = 0, limit: int = 20) -> VulnerabilitieListResponseDTO:
        vulnerabilities = await self._repo.find_all(skip=skip, limit=limit)

        vulnerabiliitie_dtos = [
            VulnerabilitieResponseDTO(
                id=v.id,
                cve=v.cve,
                description=v.description,
                severity=v.severity,
                url=v.url,
                mitigation=v.mitigation,
                created_at=v.created_at,
                updated_at=v.updated_at,
            )
            for v in vulnerabilities
        ]

        return VulnerabilitieListResponseDTO(
            vulnerabilities=vulnerabiliitie_dtos,
            total=len(vulnerabiliitie_dtos),
            skip=skip,
            limit=limit,
        )
