from ulid import ULID

from src.vulnerabilitie.application.ports.vulnerabilitie_dtos import CreateVulnerabilitieDTO, VulnerabilitieResponseDTO
from src.vulnerabilitie.domain.vulnerabilitie import Vulnerabilitie
from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository

from src.log.domain.log import Log
from src.log.domain.log_repository import LogRepository

class CreateVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository, log_repository: LogRepository):
        self._repo = vulnerabilitie_repository
        self._repo_log = log_repository

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

        log = Log(
            id=str(ULID()),
            action="CREATE",
            entity_type="VULNERABILITIE",
            entity_id=saved.id,
            description=f"Vulnerabilitie {saved.cve} created",
            created_at=saved.created_at
        )
        # llamas a save del repositorio de log
        await self._repo_log.save(log)

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
