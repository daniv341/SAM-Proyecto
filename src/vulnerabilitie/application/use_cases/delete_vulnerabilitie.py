from src.vulnerabilitie.domain.vulnerabilitie_repository import VulnerabilitieRepository
from src.shared.exceptions.domain_exceptions import EntityNotFoundException


class DeleteVulnerabilitieUseCase:
    def __init__(self, vulnerabilitie_repository: VulnerabilitieRepository):
        self._repo = vulnerabilitie_repository

    async def execute(self, vulnerabilitie_id: str) -> None:
        vulnerabilitie = await self._repo.find_by_id(vulnerabilitie_id)
        if not vulnerabilitie:
            raise EntityNotFoundException("Vulnerabilitie", vulnerabilitie_id)

        await self._repo.delete(vulnerabilitie_id)
